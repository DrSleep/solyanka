import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Optional

# Style configuration
AXES_FORMATTER = {
    "showline": True,
    "linewidth": 4,
    "linecolor": "black",
    "ticks": "outside",
    "tickwidth": 3,
    "tickcolor": "black",
    "ticklen": 10,
}
LAYOUT_FORMATTER = {
    "margin": {"l": 50, "r": 50, "b": 125, "t": 50, "pad": 10},
    "paper_bgcolor": "#f3f3f3",
    "plot_bgcolor": "#f3f3f3",
    "font": {"family": "Droid, sans", "size": 18, "color": "#1f1f1f"},
}


def save_plot_to_file(file: Path, figure: go.Figure):
    """Create standalone html of the given figure"""
    with open(file, "w") as f:
        f.write(figure.to_html(include_plotlyjs="cdn"))


def plot_scatter(
    data_frame: Optional[pd.DataFrame],
    x: Optional[str],
    y: Optional[str],
    color: Optional[str],
    symbol: Optional[str],
    size: Optional[str],
    save_file: Optional[Path],
    **kwargs
) -> Optional[go.Figure]:
    """Simple scatter plot with some custom styling"""
    fig = px.scatter(
        data_frame=data_frame,
        x=x,
        y=y,
        color=color,
        symbol=symbol,
        size=size,
        **kwargs,
    )
    fig.update_xaxes(**AXES_FORMATTER)
    fig.update_yaxes(**AXES_FORMATTER)
    fig.update_layout(**LAYOUT_FORMATTER)
    if save_file is not None:
        save_plot_to_file(save_file, fig)
    else:
        fig.show()
        return fig


def plot_box(
    data_frame: Optional[pd.DataFrame],
    x: Optional[str],
    y: Optional[str],
    color: Optional[str],
    save_file: Optional[Path],
    **kwargs
) -> Optional[go.Figure]:
    """Simple box plot with some custom styling"""
    fig = px.box(data_frame=data_frame, x=x, y=y, color=color, **kwargs,)
    fig.update_xaxes(**AXES_FORMATTER)
    fig.update_yaxes(**AXES_FORMATTER)
    fig.update_layout(**LAYOUT_FORMATTER)
    if save_file is not None:
        save_plot_to_file(save_file, fig)
    else:
        fig.show()
        return fig


def plot_bar(
    data_frame: Optional[pd.DataFrame],
    x: Optional[str],
    y: Optional[str],
    color: Optional[str],
    save_file: Optional[Path],
    **kwargs
) -> Optional[go.Figure]:
    """Simple bar plot with some custom styling"""
    fig = px.bar(data_frame=data_frame, x=x, y=y, color=color, **kwargs,)
    fig.update_xaxes(**AXES_FORMATTER)
    fig.update_yaxes(**AXES_FORMATTER)
    fig.update_layout(**LAYOUT_FORMATTER)
    if save_file is not None:
        save_plot_to_file(save_file, fig)
    else:
        fig.show()
        return fig
