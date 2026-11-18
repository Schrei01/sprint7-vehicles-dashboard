"""Dashboard interactivo de anuncios de vehículos usados (Sprint 7)."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).resolve().parent / "vehicles_us.csv"

st.set_page_config(
    page_title="Explorador de vehículos usados",
    page_icon="🚗",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Carga los anuncios de vehículos desde el CSV del proyecto."""
    data = pd.read_csv(DATA_PATH)
    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data["odometer"] = pd.to_numeric(data["odometer"], errors="coerce")
    return data


car_data = load_data()

st.title("🚗 Explorador de anuncios de vehículos usados")
st.write(
    "Panel interactivo para explorar precios y kilometraje de vehículos "
    "anunciados en Estados Unidos. Los gráficos son descriptivos y no "
    "demuestran relaciones causales."
)

st.sidebar.header("Filtros")
vehicle_types = sorted(car_data["type"].dropna().unique().tolist())
vehicle_type = st.sidebar.selectbox(
    "Tipo de vehículo", ["Todos"] + vehicle_types
)

if vehicle_type == "Todos":
    filtered_data = car_data.copy()
else:
    filtered_data = car_data.loc[car_data["type"] == vehicle_type].copy()

if filtered_data.empty:
    st.warning("No hay anuncios que cumplan los filtros seleccionados.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Anuncios", f"{len(filtered_data):,}")
col2.metric("Precio mediano", f"USD {filtered_data['price'].median():,.0f}")
col3.metric(
    "Kilometraje mediano",
    f"{filtered_data['odometer'].median():,.0f} millas",
)

st.divider()
st.header("Visualizaciones")

show_histogram = st.checkbox("Mostrar histograma de kilometraje", value=True)
if show_histogram:
    histogram_data = filtered_data.dropna(subset=["odometer"])
    st.caption(
        f"El histograma utiliza {len(histogram_data):,} anuncios con kilometraje "
        "disponible. Los valores ausentes no se sustituyen por valores inventados."
    )
    fig_hist = px.histogram(
        histogram_data,
        x="odometer",
        nbins=50,
        title="Distribución del kilometraje",
        labels={"odometer": "Kilometraje (millas)", "count": "Número de anuncios"},
    )
    fig_hist.update_layout(yaxis_title="Número de anuncios", bargap=0.04)
    st.plotly_chart(fig_hist, use_container_width=True)

show_scatter = st.checkbox("Mostrar dispersión: precio vs. kilometraje", value=True)
if show_scatter:
    scatter_data = filtered_data.dropna(subset=["price", "odometer"]).copy()
    original_count = len(scatter_data)
    # El muestreo mantiene fluida la visualización en navegadores modestos.
    if original_count > 5_000:
        scatter_data = scatter_data.sample(n=5_000, random_state=42)
        st.caption(
            f"Gráfico con una muestra reproducible de 5.000 de "
            f"{original_count:,} anuncios completos."
        )
    else:
        st.caption(f"Gráfico con {original_count:,} anuncios completos.")

    fig_scatter = px.scatter(
        scatter_data,
        x="odometer",
        y="price",
        color="condition",
        opacity=0.5,
        render_mode="webgl",
        title="Relación entre precio y kilometraje",
        labels={
            "odometer": "Kilometraje (millas)",
            "price": "Precio anunciado (USD)",
            "condition": "Condición",
        },
        hover_data=["model", "model_year"],
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("Sobre el dataset y sus limitaciones"):
    st.write(
        "El conjunto de datos original contiene 51.525 anuncios. "
        "Incluye valores ausentes (por ejemplo, en odometer y model_year) "
        "y precios extremos. Para evitar alterar los datos, el histograma "
        "excluye solo registros sin kilometraje y el gráfico de dispersión "
        "excluye registros sin precio o kilometraje. "
        "Las cifras describen anuncios, no precios de venta efectivos."
    )
    st.write("Datos faltantes por columna para la selección actual:")
    st.dataframe(
        filtered_data.isna().sum().rename("Valores ausentes").to_frame(),
        use_container_width=True,
    )
