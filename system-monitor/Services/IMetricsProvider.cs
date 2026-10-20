using SystemMonitor.Models;

namespace SystemMonitor.Services;

public interface IMetricsProvider : IDisposable
{
    MetricsSnapshot ReadSnapshot();
}
