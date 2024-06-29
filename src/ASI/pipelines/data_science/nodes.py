import logging
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor

def split_data(input_dataset: pd.DataFrame, parameters: dict[str, int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """ Splits data into features and targets training and test sets. """

    train, test = train_test_split(
        input_dataset,                              # Input dataset
        test_size=parameters['test_size'],          # 25% for testing
        random_state=parameters['random_state'],    # Seed for reproducibility
        stratify=input_dataset['Class']             # Stratify by 'Class' to ensure balanced split
    )

    return train, test

def train_model(train: pd.DataFrame) -> TabularPredictor:
    """ Trains the linear regression model. """

    logger = logging.getLogger(__name__)
    logger.info(f'train_model_node: train.shape: {train.shape}')

    train_data = TabularDataset(train)
    label = 'Class'
    path = os.path.join('data', '05_models', 'model')
    predictor = TabularPredictor(label=label, path=path, verbosity=0).fit(train_data, presets=['optimize_for_deployment', 'medium_quality_faster_train'])
    return predictor

def evaluate_model(predictor: TabularPredictor, test: pd.DataFrame) -> dict[str, float]:
    """Calculates and logs the coefficient of determination. """

    test_data = TabularDataset(test)
    predictor.predict(test_data)
    evaluation = predictor.evaluate(test_data)

    logger = logging.getLogger(__name__)
    logger.info(f'evaluation: {evaluation}')

    return evaluation