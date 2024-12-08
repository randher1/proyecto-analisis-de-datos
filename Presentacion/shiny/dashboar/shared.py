from pathlib import Path
import geopandas as gpd
import pandas as pd

app_dir = Path(__file__).parent
#Data Frame
df = pd.read_csv(app_dir / "../../../Data/db/Procesados/data_limpia.csv")
#Shape File
shp = gpd.read_file(app_dir / "../../../Data/shapefiles/Barrios/Barrios.shp")