# Proyecto Análisis de Datos Talento TECH UTB

La actual base de datos, es tomada de la página web [METRO CUADRADO](https://www.metrocuadrado.com), y refleja el precio de la vivienda en la ciudad de Cartagena para una muestra de mas de 1.500 inmuebles

## ¿Como inicializar el proyecto?

1. Crear un entorno virtual de ```python```

```bash
python3 -m venv nombre_del_entorno

-- ejemplo

python3 -m venv .env
```
2. Inicializar entorno virtual

```bash
source nombre_del_entorno/bin/activate

-- ejemplo

source .env/bin/activate
```

3. Instalar los paquetes necesarios

```python
pip install -r requirements.txt
```

## Ya esta listo para ver el proyecto
El proyecto consta de diferentes archivos de ```JupiterNoteBook``` para la limpieza, análisis y visualización de los datos.

Los [Datos iniciales](Data/db/Originales/inmuebles_dommies.csv), constan de la data Scrapeada de [METRO CUADRADO](https://www.metrocuadrado.com) y se limpian en el el entorno de ```JupiterNoteBook``` llamado [clear_data](Scripts/clear_data.ipynb) y los resultados de la limpieza de esos datos estan en [Datos limpios](Data/db/Procesados/data_limpia.csv)
