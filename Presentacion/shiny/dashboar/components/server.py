from shiny import reactive, render, ui
from shared import df
from components.moneyFormat import money_format
import plotly.express as px
from shinywidgets import render_widget
import locale
from ipyleaflet import Map, GeoJSON, LayersControl,Popup
from pathlib import Path
import matplotlib.pyplot as plt
import json
from ipywidgets import HTML
import pandas as pd

locale.setlocale(locale.LC_ALL, '') 
app_dir = Path(__file__).parent
geojson_path = app_dir / "../data/cartagena.geojson"

# Remplazo en estrato del float por int
remplazosInt = {
    "5.0": 5,
    "4.0": 4,
    "3.0": 3,
    "2.0": 2,
}

# Realiza el reemplazo en la columna 'estrato' y convierte a int
df['estrato'] = df['estrato'].replace(remplazosInt).astype(int)

# Función que se ejecuta al hacer clic en un polígono
# Función que se ejecuta al hacer clic en un polígono
def on_click(event, feature, data):
    # Extraemos las propiedades del polígono clicado
    properties = feature['properties']
    nombre = properties.get("NOMBRE", "Desconocido")
    precio_promedio = properties.get("precio", "Desconocido")
    maximo = properties.get("PE", "Desconocido")  # Si el máximo está en 'PE' o como corresponda
    minimo = properties.get("POB_BARRIO", "Desconocido")  # Si el mínimo está en 'POB_BARRIO' o como corresponda

    # Crear contenido HTML para el Popup
    popup_content = HTML(f"""
        <div>
            <h3>{nombre}</h3>
            <p><strong>Precio Promedio:</strong> {money_format(precio_promedio)}</p>
            <p><strong>Máximo:</strong> {maximo}</p>
            <p><strong>Mínimo:</strong> {minimo}</p>
        </div>
    """)

    # Crear el popup en la ubicación del centro del polígono
    popup = Popup(
        location=event['coordinates'],
        child=popup_content,
        close_button=True,
        auto_close=True
    )
    # Se agrega el popup al mapa

    return popup

def get_color(precio, min_precio, max_precio):
    """Calcula un color basado en el precio usando una escala lineal."""
    # Asegurarse de que precio, min_precio y max_precio no sean None
    if precio is None or min_precio is None or max_precio is None:
        return 'rgba(255, 255, 255, 0)'  # Color blanco transparente (o un valor por defecto)

    normalized = (precio - min_precio) / (max_precio - min_precio)
    cmap = plt.cm.Blues  # Escala de colores
    rgba = cmap(normalized)  # Color RGBA normalizado
    return f'rgba({int(rgba[0]*255)}, {int(rgba[1]*255)}, {int(rgba[2]*255)}, {rgba[3]})'

def server(input, output, session):
    # Cargar datos GeoJSON dentro del servidor
    if geojson_path.exists():
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
    else:
        raise FileNotFoundError(f"El archivo {geojson_path} no se encontró.")
    
    
            
    
    # Calcular rango de precios
    precios = [feature["properties"]["precio"] for feature in geojson_data["features"]]
    precios = [precio for precio in precios if precio is not None]  # Filtra valores None
    if precios:  # Asegúrate de que la lista no esté vacía
        min_precio = min(precios)
        max_precio = max(precios)
    else:
        min_precio = 0  # O un valor por defecto
        max_precio = 1  # O un valor por defecto

    # Asignar colores a los polígonos según el precio
    for feature in geojson_data["features"]:
        precio = feature["properties"]["precio"]
        color = get_color(precio, min_precio, max_precio)
        feature["properties"]["style"] = {
            "fillColor": color,
            "color": "black",  # Borde del polígono
            "weight": 1,
            "fillOpacity": 0.8
        }

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

    @reactive.Calc
    def total_mean():
        if input.loc1() == "Todos":
            mean = (df['precio'] / df['metros_construidos']).mean()
        else:
            mean = (filtered_data()['precio'] / filtered_data()['metros_construidos']).mean()
        return locale.format_string("%.2f", mean, grouping=True)

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
    @render.ui
    def dynamic_mean():
        mean_value = total_mean()
        title = "Valor promedio de metro cuadrado por barrio" if input.loc1() == "Todos" else f"Valor promedio de metro cuadrado en {input.loc1()}"
        return ui.HTML(
            f"""
            <div>
                <p style="font-size: 16px; font-weight: bold;">{title}</p>
                <span style="font-size: 40px; font-weight: bold; text-align: center;">
                    {mean_value} m²
                </span>
            </div>
        """
        )

    @output
    @render_widget
    def estrato():
        data = filtered_data()

        if data.empty:
            print("No hay datos para graficar.")
            fig = px.pie(
                names=[],
                title="Sin datos disponibles",
                template="plotly_white"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            return fig

        fig = px.pie(
            data,
            hole=0.5,
            names='estrato',
            title='Distribución de Estratos',
            template='plotly_white',
            color_discrete_sequence=px.colors.sequential.Plasma
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        return fig
    
    @reactive.Calc
    def top_10():
        # Agrupar los datos por la columna 'localizacion' y calcular la media del 'precio'
        conteo_localizacion = df.groupby('localizacion')['precio'].mean().reset_index()

        # Ordenar los datos de mayor a menor según 'precio'
        conteo_localizacion = conteo_localizacion.sort_values(by='precio', ascending=False)
        
        # Asegurarte de que 'estrato' exista en el dataframe antes de intentar convertirlo
        if 'estrato' in df.columns:
            conteo_localizacion['estrato'] = df['estrato'].astype('category')  # Asumiendo que 'estrato' está en df
        
        # Seleccionar el top 3 (puedes cambiarlo a 10 si lo necesitas)
        top_10_localizacion = conteo_localizacion.head(15)

        return top_10_localizacion

    
    @output
    @render_widget
    def graf():
        # Llamar al cálculo reactivo para obtener los datos filtrados
        data = top_10()

        # Crear el gráfico de barras horizontal
        fig = px.bar(
            data,
            x='precio',  # El eje X es el precio (ya que será una barra horizontal)
            y='localizacion',  # El eje Y es la localización
            color='estrato',  # Colorear las barras por 'localizacion'
            text_auto=True,  # Mostrar los valores de precio en las barras
            title='Top 10 Localizaciones por Precio Promedio',
            orientation='h',  # Cambiar a barras horizontales
            template='plotly_white'  # Estilo de diseño
        )

        # Personalizar el diseño
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",  # Fondo transparente
            plot_bgcolor="rgba(0,0,0,0)"  # Fondo transparente para el gráfico
        )

        return fig
    
    
    
    @reactive.Calc
    def filtered_data_map():
        # Extraer los datos necesarios del GeoJSON
        data = []
        for feature in geojson_data["features"]:
            # Convertir "NOMBRE" a minúsculas y eliminar espacios
            nombre = feature["properties"].get("NOMBRE", "").strip().lower()
            # Obtener el precio (u otros datos necesarios)
            precio = feature["properties"].get("precio", None)
            # Agregar al listado
            data.append({"NOMBRE": nombre, "precio": precio})
        
        # Crear un DataFrame a partir de los datos extraídos
        df1 = pd.DataFrame(data)
        
        # Normalizar la comparación de nombres
        if input.loc1() != "Todos":
            loc_input = input.loc1().strip().lower()  # Asegúrate de que el input esté normalizado
            filtered = df1[df1['NOMBRE'] == loc_input]
            
            # Depuración: Verificar qué datos se están filtrando
            
            return filtered
        
        return df1  # Devuelve todos los datos si "Todos" está seleccionado


    @output
    @render_widget
    def map():
        # Extraer los datos necesarios del GeoJSON
        data = []
        for feature in geojson_data["features"]:
            # Convertir "NOMBRE" a minúsculas y eliminar espacios
            nombre = feature["properties"].get("NOMBRE", "").strip().lower()
            # Obtener el precio (u otros datos necesarios)
            precio = feature["properties"].get("precio", None)
            # Agregar al listado
            data.append({"NOMBRE": nombre, "precio": precio})
        
        # Crear un DataFrame a partir de los datos extraídos
        df1 = pd.DataFrame(data)
        
        # Decidir qué datos utilizar basándonos en el input
        if input.loc1() == "Todos":
            data_to_plot = df1  # Usar el DataFrame completo
        else:
            data_to_plot = filtered_data_map()  # Usar los datos filtrados
        
        # Verificar que hay datos para graficar
        
        # Crear el mapa de coropletas
        fig = px.choropleth_mapbox(
            data_to_plot,
            geojson=geojson_data,
            color="precio",  # Campo que define el color
            locations="NOMBRE",  # Ubicación de los nombres en los datos
            featureidkey="properties.NOMBRE",  # Clave de identificación en el GeoJSON
            center={"lat": 10.3910, "lon": -75.4792},  # Coordenadas centrales
            mapbox_style="carto-positron",  # Estilo del mapa
            zoom=12  # Nivel de zoom
        )
        
        # Ajustar márgenes
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
