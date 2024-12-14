from shiny import ui
from components.icons import money, home, mean_icon
from shinywidgets import output_widget
from shared import df
from pathlib import Path

# Obtener los valores únicos para los selectores
city_names = list(df['localizacion'].unique())
city_names.insert(0, "Todos") 
localidad_names = ['Histórica y del Caribe Norte']

ui.include_css(
    Path(__file__).parent / "../styles.css"
)

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize(
            "loc1", 
            "Barrio", 
            choices=city_names, 
            selected="Todos"
        ),
        ui.input_selectize(
            "loc2", 
            "Localidad", 
            choices=localidad_names, 
            selected="Histórica y del Caribe Norte"
        ),
        ui.input_dark_mode(mode="dark"),
    ),
    ui.layout_column_wrap(
        # Tarjetas de valor
        ui.value_box(
            ui.output_ui("dynamic_price"),
            ui.HTML('<span style="font-size:24px; font-weight: bold;">2024</span>'),
            showcase=money,
            theme="bg-gradient-indigo-purple",
            style="width: 100%; margin-bottom: 10px;"
        ),
        ui.value_box(
            "",
            ui.output_ui("dynamic_casas"),
            theme="gradient-blue-indigo",
            showcase=home,
            style="width: 100%; margin-bottom: 10px;"
        ),
        ui.value_box(
            ui.output_ui('dynamic_mean'),
            theme="gradient-blue-indigo",
            showcase=mean_icon,
            value="",
            style="width: 100%; margin-bottom: 10px;"
        ),
        fill=False,
    ),
    
    # Layout de tarjetas para mapa, gráfico y estrato
    ui.layout_column_wrap(
        ui.card(
            output_widget("map"),
            style="height: 400px; width: 100%; margin-bottom: 20px;"  # Tarjeta superior con mapa
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Gráfico"),
                ui.div(output_widget("graf")),
            ),
            ui.card(
                ui.card_header("Estratos"),
                ui.div(output_widget("estrato")),
            ),
        ),
        style="width: 100%; margin: 0 auto;"  # Contenedor de las tres tarjetas
    ),
    
    title="DASHBOARD INMOBILIARIA METRO CUADRADO",
    fillable=True,
    class_="bslib-page-dashboard",
)
