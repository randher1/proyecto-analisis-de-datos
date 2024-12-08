from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget
import pandas as pd
from components.icons import money, home
from components.moneyFormat import money_format
from shared import df


# Obtener los valores únicos para los selectores
city_names = list(df['localizacion'].unique())
city_names.insert(0, "Todos") 
localidad_names = ['Histórica y del Caribe Norte']

# UI de la aplicación
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize(
            "loc1", 
            "Barrio", 
            choices=city_names, 
            selected="Todos"
        ),
        ui.input_selectize(
            "loc2", "Localidad", 
            choices=localidad_names, 
            selected="Histórica y del Caribe Norte"
        ),
        ui.input_selectize(
            "basemap",
            "Choose a basemap",
            choices=['uno'],
            selected="WorldImagery",
        ),
        ui.input_dark_mode(mode="dark"),
    ),
    ui.layout_column_wrap(
        ui.value_box(
            ui.output_ui("dynamic_price"),
            ui.HTML('<span style="font-size:24px; font-weight: bold;">2024</span>'),
            showcase=money,
            theme="bg-gradient-indigo-purple",
        ),
        ui.value_box(
            "",
            ui.output_ui("dynamic_casas"),
            theme="gradient-blue-indigo",
            showcase=home,
        ),
        fill=False,
    ),
    ui.card(
        ui.card_header("Map (drag the markers to change locations)"),
        output_widget("map"),
    ),
    title="DASHBOARD INMOBILIARIA METRO CUADRADO",
    fillable=True,
    class_="bslib-page-dashboard",
)

# Servidor
def server(input, output, session):
    # Reactive para filtrar el DataFrame según el valor seleccionado en loc1
    @reactive.Calc
    def filtered_data():
        if input.loc1():
            return df[df['localizacion'] == input.loc1()]
        return df  # Retorna todo el DataFrame si no hay selección

    # Suma de precios filtrados
    @reactive.Calc
    def total_price():
        if input.loc1() == "Todos":  # Aquí se corrige el typo y se usa input.loc1() como función
            return int(df['precio'].sum())
        else:
            return int(filtered_data()['precio'].sum())

    # Cantidad de propiedades filtradas
    @reactive.Calc
    def property_count():
        if input.loc1() == "Todos":
            return len(df['localizacion'])
        else:
            return len(filtered_data())

    # Actualizar el valor mostrado en el ValueBox de precio
    @output
    @render.ui
    def dynamic_price():
        formatted_number = money_format(total_price())
        if input.loc1() == "Todos":
            title = "Total de todas las casas en venta"
            return ui.HTML(
            f"""
            <div>
                <p style="font-size: 16px; font-weight: bold;">{title}</p>
                <span style="
                    font-size: 40px; 
                    font-weight: bold; 
                    text-align: center;
                    transition: transform 0.3s ease;
                    display: inline-block;"
                    onmouseover="this.style.transform='scale(1.2)'" 
                    onmouseout="this.style.transform='scale(1)'"
                >
                    {formatted_number}
                </span>
            </div>
            """
        )
        else:
            title = f"Total de casas en {input.loc1()}"
        return ui.HTML(
            f"""
            <div>
                <p style="font-size: 16px; font-weight: bold;">{title}</p>
                <span style="
                    font-size: 40px; 
                    font-weight: bold; 
                    text-align: center;
                    transition: transform 0.3s ease;
                    display: inline-block;"
                    onmouseover="this.style.transform='scale(1.2)'" 
                    onmouseout="this.style.transform='scale(1)'"
                >
                    {formatted_number}
                </span>
            </div>
            """
        )

    # Actualizar el valor mostrado en el ValueBox de cantidad de propiedades
    @output
    @render.ui
    def dynamic_casas():
        if input.loc1() == "Todos":
            title = "Cantidad de todas las propiedades"
            ui.HTML(
            f"""
            <div>
                <p style="font-size: 16px; font-weight: bold;">{title}</p>
                <span style="
                    font-size: 40px; 
                    font-weight: bold; 
                    text-align: center;
                    transition: transform 0.3s ease;
                    display: inline-block;"
                    onmouseover="this.style.transform='scale(1.2)'" 
                    onmouseout="this.style.transform='scale(1)'"
                >
                    {property_count()}
                </span>
            </div>
            """
        )
        else:
            title = f"Cantidad de propiedades en {input.loc1()}"
        return ui.HTML(
            f"""
            <div>
                <p style="font-size: 16px; font-weight: bold;">{title}</p>
                <span style="
                    font-size: 40px; 
                    font-weight: bold; 
                    text-align: center;
                    transition: transform 0.3s ease;
                    display: inline-block;"
                    onmouseover="this.style.transform='scale(1.2)'" 
                    onmouseout="this.style.transform='scale(1)'"
                >
                    {property_count()}
                </span>
            </div>
            """
        )

# Ejecutar la aplicación
app = App(app_ui, server).run()