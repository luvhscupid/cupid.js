namespace SystemMonitor.Models;

public sealed record MetricsSnapshot(
    DateTimeOffset CapturedAt,
    double CpuPercent,
    double MemoryPercent,
    double UsedMemoryGb,
    double TotalMemoryGb,
    double? TemperatureCelsius);
