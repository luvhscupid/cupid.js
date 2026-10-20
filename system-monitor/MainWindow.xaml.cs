using System.Windows;
using SystemMonitor.Models;
using SystemMonitor.Services;

namespace SystemMonitor;

public partial class MainWindow : Window
{
    private readonly MetricsSampler _sampler = new(new WindowsMetricsProvider());
    private readonly Queue<double> _cpuHistory = new();
    private readonly Queue<double> _memoryHistory = new();

    public MainWindow()
    {
        InitializeComponent();
        _sampler.SnapshotAvailable += OnSnapshot;
        Loaded += (_, _) => _sampler.Start();
        Closed += async (_, _) => await _sampler.DisposeAsync();
    }

    private void OnSnapshot(MetricsSnapshot snapshot) => Dispatcher.BeginInvoke(new Action(() =>
    {
        CpuValue.Text = snapshot.CpuPercent.ToString("0");
        CpuBar.Value = snapshot.CpuPercent;
        MemoryValue.Text = snapshot.MemoryPercent.ToString("0");
        MemoryBar.Value = snapshot.MemoryPercent;
        MemoryDetail.Text = $"{snapshot.UsedMemoryGb:0.0} / {snapshot.TotalMemoryGb:0.0} GB";
        TemperatureValue.Text = snapshot.TemperatureCelsius?.ToString("0") ?? "—";
        TemperatureNote.Text = snapshot.TemperatureCelsius.HasValue
            ? "Sensor data available"
            : "No temperature sensor exposed by this device. Try running elevated if readings are expected.";
        UpdatedLabel.Text = $"Updated {snapshot.CapturedAt:HH:mm:ss}";
        Push(_cpuHistory, snapshot.CpuPercent);
        Push(_memoryHistory, snapshot.MemoryPercent);
        CpuChart.Values = _cpuHistory.ToArray();
        MemoryChart.Values = _memoryHistory.ToArray();
    }));

    private static void Push(Queue<double> queue, double value)
    {
        if (queue.Count == 60) queue.Dequeue();
        queue.Enqueue(value);
    }
}
