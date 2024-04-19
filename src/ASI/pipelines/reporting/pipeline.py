from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model_remote


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=evaluate_model_remote,
                inputs="prediction",
                outputs=None,
                name="evaluate_model_remote_node",
            ),
        ]
    )
