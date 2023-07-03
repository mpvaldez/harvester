import pandas as pd
import harvester

df = pd.read_csv("elecciones_2023.csv")

personas = df['full_name'].unique()

paginas = []
for p in personas:
    paginas.append(harvester.get_pages(p))


recoleccion = []
for p in paginas:
    recoleccion.append(harvester.collect(p))

harvester.download(recoleccion)