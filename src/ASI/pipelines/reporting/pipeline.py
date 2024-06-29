from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model_remote, push_to_aws


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=evaluate_model_remote,
                inputs="evaluation",
                outputs=None,
                name="evaluate_model_remote_node",
            ),
            node(
                func=push_to_aws,
                inputs=["evaluation", "params:aws_params"],
                outputs=None,
                name="push_to_aws_node",
            ),
        ]
    )
