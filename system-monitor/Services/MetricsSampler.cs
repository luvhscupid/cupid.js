using SystemMonitor.Models;

namespace SystemMonitor.Services;

public sealed class MetricsSampler(IMetricsProvider provider) : IAsyncDisposable
{
    public event Action<MetricsSnapshot>? SnapshotAvailable;
    private CancellationTokenSource? _stop;
    private Task? _loop;

    public void Start()
    {
        if (_loop is not null) return;
        _stop = new CancellationTokenSource();
        _loop = Task.Run(() => RunAsync(_stop.Token));
    }

    private async Task RunAsync(CancellationToken cancellationToken)
    {
        using var timer = new PeriodicTimer(TimeSpan.FromSeconds(1));
        do
        {
            try { SnapshotAvailable?.Invoke(provider.ReadSnapshot()); }
            catch { /* A missed sample should not stop future updates. */ }
        }
        while (await timer.WaitForNextTickAsync(cancellationToken).ConfigureAwait(false));
    }

    public async ValueTask DisposeAsync()
    {
        _stop?.Cancel();
        if (_loop is not null)
        {
            try { await _loop.ConfigureAwait(false); }
            catch (OperationCanceledException) { }
        }
        _stop?.Dispose();
        provider.Dispose();
    }
}
