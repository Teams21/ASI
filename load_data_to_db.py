import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

### RUN FROM FOLDER WITH ORIGINAL CSV DATASET FILES ###

engine = create_engine('conn string from parameters_data_fetching.yml')

for f in os.listdir():
    fname = Path(f).stem
    fdf = pd.read_csv(f, delimiter='\t')
    fdf.to_sql(fname, con=engine, schema='init', index=False)