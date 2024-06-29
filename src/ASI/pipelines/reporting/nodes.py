import os
import logging
import boto3.session
import wandb
import boto3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine
from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings
from botocore.exceptions import NoCredentialsError
import psycopg2

def _get_current_model_version() -> int:

    # Pobierz dane z credentials.yaml
    connection_string = os.getenv('POSTGRES_CONNECTION_STRING')

    # Stworz polaczenie do bazy danych
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = """
    SELECT model_id 
    FROM modelinfo.model_info 
    ORDER BY model_id DESC 
    LIMIT 1
    """

    result = session.execute(text(query)).fetchone()
    session.close()

    if result is None:
        return 0

    # Kolumna model_id z bazy danych
    incremented_id = result[0] + 1

    return incremented_id

def _upload_model_metadata(evaluation: dict[str, float], s3_path: str):
    # Pobierz dane z credentials.yaml
    connection_string = os.getenv('PSYCOPG_CONNECTION_STRING')
    dbname = connection_string.split(':')[0]
    user = connection_string.split(':')[1]
    password = connection_string.split(':')[2]
    host = connection_string.split(':')[3]
    port = connection_string.split(':')[4]

    # Stworz polaczenie do bazy danych
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = connection.cursor()

    query = f"INSERT INTO modelinfo.model_info (s3_path, accuracy, balanced_accuracy, precision_metric, recall, f1, mcc, roc_auc) VALUES ('{s3_path}', {evaluation['accuracy']}, {evaluation['balanced_accuracy']}, {evaluation['precision']}, {evaluation['recall']}, {evaluation['f1']}, {evaluation['mcc']}, {evaluation['roc_auc']});"
    # Execute the query
    cursor.execute(query)
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

def evaluate_model_remote(evaluation: dict[str, float]):
    """ Calculates and logs the coefficient of determination. """

    wandb.login(key=os.getenv('WANDB_API_KEY'))
    run = wandb.init(project='ASI')
    try:
        # Log metrics
        wandb.log({'accuracy': evaluation['accuracy'],
                  'balanced_accuracy': evaluation['balanced_accuracy'],
                  'precision': evaluation['precision'],
                  'recall': evaluation['recall'],
                  'f1_score': evaluation['f1'],
                  'mcc': evaluation['mcc'],
                  'roc_auc': evaluation['roc_auc']})

    except KeyError as e:
        print(f"KeyError: {e}. Ensure 'Class' and 'prediction_label' are in prediction_labels_test.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        run.finish()

def push_to_aws(evaluation: dict[str, float], parameters: dict[str, str]):

    # Pobierz wersję modelu (dla sciezki S3)
    current_model_version = _get_current_model_version()

    # Stwórz sesję z pomocą profilu asi-s3-write z ~/.aws/credentials
    session = boto3.Session(profile_name=parameters['profile_name'])
    s3 = session.resource('s3')

    # Pobierz nazwe bucketa z konfiguracji
    bucket_name = parameters['bucket_name']

    # Sciezka pliku w bukecie
    key = f'model/{current_model_version}/predictor.pkl'

    logger = logging.getLogger(__name__)
    logger.info(f"current_model_version: {current_model_version}")

    # Wyslij plik i metadane
    try:
        s3.Bucket(bucket_name).upload_file(parameters['model_path'], key)
        _upload_model_metadata(evaluation, f's3://{bucket_name}/{key}')
        print("File and metadata uploaded successfully.")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")
