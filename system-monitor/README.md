# System Monitor (Windows prototype)

A small WPF dashboard for CPU load, memory use, and available temperature sensors.

## Architecture

- **Presentation:** WPF window; updates are marshalled onto the dispatcher.
- **Sampling:** `MetricsSampler` runs once per second on a background task and publishes immutable snapshots.
- **CPU:** `GetSystemTimes` delta sampling (no external performance counter package).
- **Memory:** `GlobalMemoryStatusEx` for total and available physical memory.
- **Temperatures:** optional `LibreHardwareMonitorLib` provider. Sensor availability depends on the hardware/firmware and may require running with elevated privileges. The app reports no reading when none is exposed.

This keeps UI and acquisition independent. Later providers can implement `IMetricsProvider` for GPU, disk, network, or remote metrics without changing the window.

## Run on Windows

Install the .NET 8 SDK, then from this directory:

```powershell
dotnet run
```

To publish a self-contained x64 build:

```powershell
dotnet publish -c Release -r win-x64 --self-contained true
```

## Notes

The current prototype samples every second and retains 60 CPU/memory points in memory for the small history chart. It does not persist data or start automatically with Windows.
