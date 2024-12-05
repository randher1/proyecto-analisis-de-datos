import seaborn as sns
import pandas as pd
from shiny import App, render, ui

# Cargar el CSV
df1 = pd.read_csv("penguins.csv")

# Obtener las columnas numéricas que se pueden graficar
numeric_columns = df1.select_dtypes(include='number').columns.tolist()

# Obtener nombres únicos de especies como strings para el hue
species_series = df1['island'].unique().astype(str).tolist()

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "var", "Select variable", choices=numeric_columns
        ),
        ui.input_switch("island", "Group by species", value=True),
        ui.input_switch("show_rug", "Show Rug", value=True),
    ),
    ui.output_plot("hist"),
    title="DASHBOARD",
)

# Función de servidor para renderizar el gráfico
def server(input, output, session):
    @render.plot
    def hist():
        hue = "island" if input.island() else None
        sns.kdeplot(data=df1, x=input.var(), hue=hue)
        if input.show_rug():
            sns.rugplot(data=df1, x=input.var(), hue=hue, color="black", alpha=0.25)

# Ejecutar la aplicación
app = App(app_ui, server).run()
