using System.Windows;
using System.Windows.Media;

namespace SystemMonitor.Controls;

public sealed class Sparkline : FrameworkElement
{
    public static readonly DependencyProperty ValuesProperty = DependencyProperty.Register(
        nameof(Values), typeof(IReadOnlyList<double>), typeof(Sparkline),
        new FrameworkPropertyMetadata(Array.Empty<double>(), FrameworkPropertyMetadataOptions.AffectsRender));
    public Brush LineBrush { get; set; } = new SolidColorBrush(Color.FromRgb(102, 227, 196));
    public IReadOnlyList<double> Values { get => (IReadOnlyList<double>)GetValue(ValuesProperty); set => SetValue(ValuesProperty, value); }

    protected override void OnRender(DrawingContext dc)
    {
        base.OnRender(dc);
        if (Values.Count < 2 || ActualWidth <= 0 || ActualHeight <= 0) return;
        var geometry = new StreamGeometry();
        using (var ctx = geometry.Open())
        {
            var maxIndex = Values.Count - 1;
            Point PointAt(int i) => new(ActualWidth * i / maxIndex, ActualHeight * (1 - Math.Clamp(Values[i], 0, 100) / 100));
            ctx.BeginFigure(PointAt(0), false, false);
            ctx.PolyLineTo(Enumerable.Range(1, maxIndex).Select(PointAt).ToArray(), true, false);
        }
        geometry.Freeze();
        dc.DrawGeometry(null, new Pen(LineBrush, 2), geometry);
    }
}
