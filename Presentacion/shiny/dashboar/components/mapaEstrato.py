# components/estrato_graph.py
import plotly.express as px

def estrato(filtered_data):
    # Manejar caso de DataFrame vacío
    if filtered_data.empty:
        print("No hay datos para graficar.")
        fig = px.pie(
            names=[],
            title="Sin datos disponibles",
            template="plotly_white"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",  # Fondo general transparente
            plot_bgcolor="rgba(0,0,0,0)"   # Fondo del área del gráfico transparente
        )
        return fig

    # Crear el gráfico
    fig = px.pie(
        filtered_data,
        hole=0.5,
        names='estrato',
        title='Distribución de Estratos',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    # Configurar fondo transparente
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # Fondo general transparente
        plot_bgcolor="rgba(0,0,0,0)"   # Fondo del área del gráfico transparente
    )

    return fig
