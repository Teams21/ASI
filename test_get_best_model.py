from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine

def _get_current_model_version() -> int:

    # Pobierz dane z credentials.yaml
    connection_string = os.getenv('POSTGRES_CONNECTION_STRING')

    # Stworz polaczenie do bazy danych
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = """
    SELECT model_id, MAX(accuracy) 
    FROM modelinfo.model_info 
    ORDER BY model_id 
    LIMIT 1
    """

    result = session.execute(text(query)).fetchone()
    session.close()

    if result is None:
        return 0

    # Kolumna model_id z bazy danych
    return = result[0]

