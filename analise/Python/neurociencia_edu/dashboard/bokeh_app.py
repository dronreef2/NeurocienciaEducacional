"""
Bokeh Dashboard — visualização interativa para P03 EEG/ERP.

Uso:
    bokeh serve analise/Python/neurociencia_edu/dashboard/bokeh_app.py --port 5006

Diferente do Streamlit (que é Python puro), Bokeh gera um servidor standalone
e produz plots interativos em JavaScript (browser-friendly).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from bokeh.io import curdoc
from bokeh.layouts import column, row, gridplot
from bokeh.models import (
    ColumnDataSource, Select, Slider, HoverTool, Div,
    ColorBar, LinearColorMap, CDSView, BooleanFilter,
)
from bokeh.plotting import figure
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.palettes import Viridis256, Category10

import numpy as np
import pandas as pd

# Paths
PROJETO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RESULTADOS_DIR = PROJETO_ROOT / "resultados"

# ============================================================
# Carregar dados
# ============================================================
def load_csv(name: str) -> pd.DataFrame | None:
    """Carrega CSV se existir."""
    path = RESULTADOS_DIR / name
    if path.exists():
        return pd.read_csv(path)
    return None


# ============================================================
# Layout
# ============================================================
title = Div(
    text="""
    <h1>🧠 Programa de Pesquisa — Dashboard EEG/ERP</h1>
    <p>Visualização interativa dos resultados do P03.</p>
    """,
    width=1000,
)

# Placeholder inicial (dados reais carregados dinamicamente)
placeholder = Div(
    text="<p><em>Execute as análises primeiro para ver dados aqui.</em></p>",
    width=1000,
)

# Métricas dos componentes (gráfico de barras)
def make_metrics_plot():
    """Gera plot de métricas dos componentes ERP."""
    df = load_csv("P03/00_metricas_componentes.csv")
    if df is None or df.empty:
        return None

    components = df["componente"].unique().tolist()
    source = ColumnDataSource(df)

    p = figure(
        x_range=components,
        height=350,
        title="Amplitude Média por Componente ERP",
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )
    p.vbar(
        x="componente",
        top="amplitude_media",
        width=0.7,
        source=source,
        fill_color=factor_cmap("componente", palette=Category10[10], factors=components),
        legend_field="componente",
    )
    p.yaxis.axis_label = "Amplitude (µV)"
    p.xaxis.axis_label = "Componente"
    p.legend.visible = False
    p.add_tools(HoverTool(tooltips=[
        ("Componente", "@componente"),
        ("Condição", "@condicao"),
        ("Amplitude", "@amplitude_media{0.00}"),
        ("Pico", "@amplitude_pico{0.00}"),
        ("Latência (ms)", "@latencia_pico_ms{0.0}"),
    ]))
    return p


def make_topography_plot():
    """Gera plot de topografia (heatmap)."""
    # Topografia sintética (substitua por dados reais)
    np.random.seed(42)
    coords = []
    for x in np.linspace(-1, 1, 20):
        for y in np.linspace(-1, 1, 20):
            coords.append((x, y, np.exp(-(x**2 + y**2) / 0.5)))

    df = pd.DataFrame(coords, columns=["x", "y", "value"])
    source = ColumnDataSource(df)

    p = figure(
        height=400,
        width=400,
        title="Topografia (exemplo)",
        x_range=(-1.1, 1.1),
        y_range=(-1.1, 1.1),
        tools="pan,wheel_zoom,reset,save",
    )
    mapper = linear_cmap(field_name="value", palette=Viridis256, low=0, high=1)
    p.scatter(
        x="x", y="y", size=15, color=mapper, source=source,
        alpha=0.8, marker="circle",
    )
    p.axis.visible = False
    p.grid.visible = False

    color_bar = ColorBar(color_mapper=mapper["transform"], width=8, location=(0, 0))
    p.add_layout(color_bar, "right")
    return p


# Layout
plots = []
metrics_plot = make_metrics_plot()
topo_plot = make_topography_plot()

if metrics_plot and topo_plot:
    plots = [title, row(metrics_plot, topo_plot)]
else:
    plots = [title, placeholder]

# Adicionar instruções
instructions = Div(
    text="""
    <h3>Como usar:</h3>
    <ol>
        <li>Execute o pipeline EEG: <code>poetry run neurociencia-eeg-erp --input dados/processed/P03/ --batch</code></li>
        <li>Recarregue esta página</li>
        <li>Use os tools (pan, zoom, save) para explorar</li>
    </ol>
    <h3>Componentes ERP analisados:</h3>
    <ul>
        <li><strong>N170</strong> (130-210 ms): especialização visual</li>
        <li><strong>N400</strong> (300-500 ms): integração semântica</li>
        <li><strong>P300</strong> (250-450 ms): atenção</li>
        <li><strong>P600</strong> (500-800 ms): reanálise sintática</li>
    </ul>
    """,
    width=1000,
)

plots.append(instructions)

curdoc().add_root(column(*plots))
curdoc().title = "Neurociencia Educacional — EEG/ERP"
