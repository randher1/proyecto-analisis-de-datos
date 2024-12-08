from shiny import reactive, render, ui
from shared import df
from components.moneyFormat import money_format
import plotly.express as px
from shinywidgets import render_widget  

def server(input, output, session):
    @reactive.Calc
    def filtered_data():
        if input.loc1() and input.loc1() != "Todos":
            filtered = df[df['localizacion'] == input.loc1()]
            filtered = filtered[filtered['estrato'].notnull()]
            return filtered
        return df[df['estrato'].notnull()]


    @reactive.Calc
    def total_price():
        if input.loc1() == "Todos":
            return int(df['precio'].sum())
        else:
            return int(filtered_data()['precio'].sum())

    @reactive.Calc
    def property_count():
        if input.loc1() == "Todos":
            return len(df['localizacion'])
        else:
            return len(filtered_data())

    @output
    @render.ui
    def dynamic_price():
        formatted_number = money_format(total_price())
        title = "Total de todas las casas en venta" if input.loc1() == "Todos" else f"Total de casas en {input.loc1()}"
        return ui.HTML(f"""
            <div>
                <p style="font-size: 16px; font-weight: bold;">{title}</p>
                <span style="font-size: 40px; font-weight: bold; text-align: center;">
                    {formatted_number}
                </span>
            </div>
        """)

    @output
    @render.ui
    def dynamic_casas():
        count = property_count()
        title = "Cantidad de todas las propiedades" if input.loc1() == "Todos" else f"Cantidad de propiedades en {input.loc1()}"
        return ui.HTML(f"""
            <div>
                <p style="font-size: 16px; font-weight: bold;">{title}</p>
                <span style="font-size: 40px; font-weight: bold; text-align: center;">
                    {count}
                </span>
            </div>
        """)

    @output
    @render_widget
    def estrato():
        data = filtered_data()

        # Manejar caso de DataFrame vacío
        if data.empty:
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
            data,
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



