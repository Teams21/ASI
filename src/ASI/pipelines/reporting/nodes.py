import logging
import pandas as pd
from pycaret.classification import predict_model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import wandb


def evaluate_model_remote(
    prediction_labels_test: pd.DataFrame
):
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """

    run = wandb.init(project='ASI', config={"learning_rate": 0.01, "epochs": 10})
    try:
        # Calculating metrics
        accuracy = accuracy_score(prediction_labels_test['Class'], prediction_labels_test['prediction_label'])
        precision = precision_score(prediction_labels_test['Class'], prediction_labels_test['prediction_label'])
        recall = recall_score(prediction_labels_test['Class'], prediction_labels_test['prediction_label'])
        f1 = f1_score(prediction_labels_test['Class'], prediction_labels_test['prediction_label'])
        confusion_matrix = pd.crosstab(
            prediction_labels_test['Class'],
            prediction_labels_test['prediction_label'],
            rownames=['Actual'],
            colnames=['Predicted']
        )

        logger = logging.getLogger(__name__)
        logger.info(f"confusion matrix: {confusion_matrix}")

        # Log metrics
        wandb.log({"conf_mat": wandb.plot.confusion_matrix(probs=None, y_true=prediction_labels_test['Class'].values,
                                                           preds=prediction_labels_test['prediction_label'].values,
                                                           class_names=['control', 'depressive']),
                   "accuracy": accuracy,
                   "precision": precision,
                   "recall": recall,
                   "f1_score": f1})

        # return pd.DataFrame({
        #     'accuracy': [accuracy],
        #     'precision': [precision],
        #     'recall': [recall],
        #     'f1_score': [f1]
        # }), confusion_matrix

    except KeyError as e:
        print(f"KeyError: {e}. Ensure 'Class' and 'prediction_label' are in prediction_labels_test.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        run.finish()
