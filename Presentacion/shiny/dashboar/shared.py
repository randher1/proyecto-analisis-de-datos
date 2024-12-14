from pathlib import Path
import geopandas as gpd
import pandas as pd
import json
from ipyleaflet import GeoJSON

# Directorio de la aplicación
app_dir = Path(__file__).parent

# Data Frame
df = pd.read_csv(app_dir / "../../../Data/db/Procesados/data_limpia.csv")

