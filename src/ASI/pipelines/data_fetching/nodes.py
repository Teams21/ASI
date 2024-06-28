import os
import pandas as pd
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings


def fetch_data() -> list[pd.DataFrame]:

    # Wczytaj postgres connection string z credentials.yml
    conf_path = str(Path(r'./') / settings.CONF_SOURCE)
    conf_loader = OmegaConfigLoader(conf_source=conf_path)
    connection_string = os.getenv('POSTGRES_CONNECTION_STRING')

    # Stworz polaczenie do bazy danych
    engine = create_engine(connection_string)

    # Tabele z bazy danych
    columns = ['aoi_depresja_1', 'aoi_depresja_2', 'aoi_kontrolni_1', 'event_depresja_1', 'event_depresja_2', 'event_kontrolni_1']

    # Zwracana lista
    data = []

    with Session(engine) as session:
        for col in columns:
            result = session.execute(text(f'SELECT * FROM init.{col}'))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            data.append(df)

    return data