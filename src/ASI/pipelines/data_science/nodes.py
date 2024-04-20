import logging
import pandas as pd
from pycaret.classification import *
from sklearn.model_selection import train_test_split
from typing import Union, Any, List

def split_data(model_input: pd.DataFrame, parameters: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """

    Xy_train, Xy_test = train_test_split(
        model_input,
        test_size=parameters["test_size"],
        stratify=model_input['Class'],
        random_state=parameters["random_state"]
    )

    return Xy_train, Xy_test

def train_model(Xy_train: pd.DataFrame) -> Union[Any, List[Any]]:
    """Trains the linear regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.

    Returns:
        Trained model.
    """
    setup(Xy_train, target = 'Class', session_id = 123)
    best = compare_models()

    return best

def evaluate_model(
    model: Union[Any, List[Any]], Xy_test: pd.DataFrame
) -> pd.DataFrame:
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """

    y_test = Xy_test['Class']
    X_test = Xy_test.drop('Class', axis=1)
    prediction = predict_model(model, data = X_test)
    prediction = pd.concat([prediction, y_test], axis=1)
    prediction = prediction[['Class', 'prediction_label']]
    # Replace 'depressive' with 1 and 'control' with 0 in both columns
    prediction.replace({'depressive': 1, 'control': 0}, inplace=True)
    pd.set_option('display.max_rows', None)
    logger = logging.getLogger(__name__)
    logger.info(f"{(prediction['Class'] == prediction['prediction_label']).sort_values().count()/prediction.shape[0]*100}%")
    
    return prediction