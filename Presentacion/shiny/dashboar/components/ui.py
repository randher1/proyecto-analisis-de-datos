from shiny import ui
from components.icons import money, home
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
        ui.value_box(
            ui.output_ui("dynamic_price"),
            ui.HTML('<span style="font-size:24px; font-weight: bold;">2024</span>'),
            showcase=money,
            theme="bg-gradient-indigo-purple"
        ),
        ui.value_box(
            "",
            ui.output_ui("dynamic_casas"),
            theme="gradient-blue-indigo",
            showcase=home,
        ),
        ui.value_box(
            id="tres",
            theme="gradient-blue-indigo",
            showcase=home,
            title="hola",
            value="j",
        ),
        fill=False,
    ),
    ui.card(
        ui.card_header("Map"),
        output_widget("map"),
        height="5000px",
        ),
    
    ui.layout_columns(
    ui.card(
        ui.card_header("Grafico"),
        ui.div(output_widget("graf")),
        height="5000px"
    ),
    ui.card(
        ui.card_header("Estratos"),
        ui.div(output_widget("estrato")),
        height="5000px"
    ),
    ),
    title="DASHBOARD INMOBILIARIA METRO CUADRADO",
    fillable=True,
    class_="bslib-page-dashboard",
)
