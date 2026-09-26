"""Habillage Plotly cohérent + quelques constructeurs de graphiques réutilisés par plusieurs vues."""

import plotly.express as px

from config import CHART_SEQUENCE, PALETTE

# Compatibilité entre versions de Plotly : scatter_mapbox/density_mapbox ont été
# renommées scatter_map/density_map dans les versions récentes.
if hasattr(px, "scatter_map"):
    scatter_geo = px.scatter_map
    density_geo = px.density_map
    MAP_STYLE_KEY = "map_style"
else:
    scatter_geo = px.scatter_mapbox
    density_geo = px.density_mapbox
    MAP_STYLE_KEY = "mapbox_style"

MAP_STYLE = "carto-positron"


def themed_layout(fig, height=420, legend=True, title=None):
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(family="Inter, sans-serif", color=PALETTE["text"], size=12),
        title_font=dict(family="Newsreader, serif", size=16, color=PALETTE["navy"]),
        title=title,
        margin=dict(t=40 if title else 20, b=30, l=40, r=20),
        plot_bgcolor=PALETTE["surface"],
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=legend,
        legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=11, color=PALETTE["muted"])),
        colorway=CHART_SEQUENCE,
        xaxis=dict(gridcolor=PALETTE["border"], zeroline=False),
        yaxis=dict(gridcolor=PALETTE["border"], zeroline=False),
    )
    return fig


def region_bar_chart(df, value_col, label, color=None, height=360):
    """Barres horizontales triées par région — pattern répété dans plusieurs vues."""
    color = color or PALETTE["teal"]
    fig = px.bar(
        df.sort_values(value_col), x=value_col, y="region", orientation="h",
        color_discrete_sequence=[color],
    )
    fig = themed_layout(fig, height=height, legend=False)
    fig.update_layout(xaxis_title=label, yaxis_title=None)
    return fig
