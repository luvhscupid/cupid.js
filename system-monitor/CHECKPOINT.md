# Windows System Monitor Prototype

**Verification state:** `LOCAL_PENDING`

## Relevant Git commit

Implementation commit: pending.

## Task objective

Design and create a lightweight Windows dashboard prototype for real-time CPU, RAM, and temperature monitoring.

## Approved decisions

- Use .NET 8 WPF for a native, lightweight Windows desktop interface.
- Keep sampling separate from presentation using `IMetricsProvider` and `MetricsSampler`.
- Read CPU and memory through Windows APIs; use LibreHardwareMonitor as a best-effort temperature source.
- Sample once per second and keep a 60-point in-memory history.

## Completed work

- Added a WPF dashboard, CPU and memory history charts, background sampler, metrics provider, and Windows run instructions in this folder.
- Temperature provider startup/read failures do not prevent CPU and memory reporting.

## Test and supporting evidence

- `uname -a` reported a Linux x86_64 environment, not Windows.
- `command -v dotnet` returned no executable; no Windows build or runtime verification was possible.
- `find system-monitor -maxdepth 3 -type f -print | sort` listed the expected project, UI, model, services, and documentation files.
- No application tests or builds were run.

## Unresolved blockers

- WPF compilation and live CPU, memory, and temperature readings remain unverified on Windows.

## Exact next action

On Windows with the .NET 8 SDK, run `dotnet run` from `system-monitor`, confirm the CPU and memory values update once per second, and check temperature behavior on hardware that exposes sensors.
