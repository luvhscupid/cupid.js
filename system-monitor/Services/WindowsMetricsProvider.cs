using System.Runtime.InteropServices;
using LibreHardwareMonitor.Hardware;
using SystemMonitor.Models;

namespace SystemMonitor.Services;

/// <summary>Windows CPU and RAM APIs plus optional LibreHardwareMonitor temperatures.</summary>
public sealed class WindowsMetricsProvider : IMetricsProvider
{
    private readonly Computer _computer;
    private readonly object _sensorLock = new();
    private ulong _previousIdle, _previousKernel, _previousUser;
    private bool _hasCpuSample;
    private bool _hardwareOpened;

    public WindowsMetricsProvider()
    {
        _computer = new Computer
        {
            IsCpuEnabled = true,
            IsGpuEnabled = true,
            IsMotherboardEnabled = true,
            IsMemoryEnabled = true
        };
        try
        {
            _computer.Open();
            _hardwareOpened = true;
        }
        catch
        {
            // Sensor access is optional; CPU and memory use Windows APIs directly.
        }
    }

    public MetricsSnapshot ReadSnapshot()
    {
        var cpu = ReadCpuPercent();
        var memory = new MemoryStatus { Length = (uint)Marshal.SizeOf<MemoryStatus>() };
        if (!GlobalMemoryStatusEx(ref memory))
            throw new InvalidOperationException("Windows could not read memory status.");

        var total = memory.TotalPhys / 1024d / 1024d / 1024d;
        var available = memory.AvailPhys / 1024d / 1024d / 1024d;
        var used = Math.Max(0, total - available);
        var memoryPercent = total > 0 ? used / total * 100 : 0;

        return new MetricsSnapshot(DateTimeOffset.Now, cpu, memoryPercent, used, total, ReadTemperature());
    }

    private double ReadCpuPercent()
    {
        if (!GetSystemTimes(out var idle, out var kernel, out var user))
            return 0;
        var idleNow = ToUInt64(idle);
        var kernelNow = ToUInt64(kernel);
        var userNow = ToUInt64(user);
        if (!_hasCpuSample)
        {
            _previousIdle = idleNow;
            _previousKernel = kernelNow;
            _previousUser = userNow;
            _hasCpuSample = true;
            return 0;
        }

        var idleDelta = idleNow - _previousIdle;
        var totalDelta = (kernelNow - _previousKernel) + (userNow - _previousUser);
        _previousIdle = idleNow;
        _previousKernel = kernelNow;
        _previousUser = userNow;
        return totalDelta == 0 ? 0 : Math.Clamp(100d * (totalDelta - idleDelta) / totalDelta, 0, 100);
    }

    private double? ReadTemperature()
    {
        if (!_hardwareOpened) return null;
        lock (_sensorLock)
        {
            try
            {
                float? hottest = null;
                foreach (var hardware in _computer.Hardware)
                {
                    UpdateAndFind(hardware, ref hottest);
                }
                return hottest;
            }
            catch
            {
                // Temperature is best-effort. Keep CPU and memory available if a driver fails.
                return null;
            }
        }
    }

    private static void UpdateAndFind(IHardware hardware, ref float? hottest)
    {
        hardware.Update();
        foreach (var sensor in hardware.Sensors)
        {
            if (sensor.SensorType == SensorType.Temperature && sensor.Value is float value &&
                (!hottest.HasValue || value > hottest.Value))
                hottest = value;
        }
        foreach (var subHardware in hardware.SubHardware)
            UpdateAndFind(subHardware, ref hottest);
    }

    private static ulong ToUInt64(System.Runtime.InteropServices.ComTypes.FILETIME time) =>
        ((ulong)(uint)time.dwHighDateTime << 32) | (uint)time.dwLowDateTime;

    public void Dispose()
    {
        if (_hardwareOpened) _computer.Close();
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
    private struct MemoryStatus
    {
        public uint Length, MemoryLoad;
        public ulong TotalPhys, AvailPhys, TotalPageFile, AvailPageFile, TotalVirtual, AvailVirtual, AvailExtendedVirtual;
    }

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool GlobalMemoryStatusEx(ref MemoryStatus buffer);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool GetSystemTimes(out System.Runtime.InteropServices.ComTypes.FILETIME idle,
        out System.Runtime.InteropServices.ComTypes.FILETIME kernel,
        out System.Runtime.InteropServices.ComTypes.FILETIME user);
}
