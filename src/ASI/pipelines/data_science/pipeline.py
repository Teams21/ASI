from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["input_dataset", "params:model_options"],
                outputs=["train", "test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["train"],
                outputs="model",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["model", "test"],
                outputs="evaluation",
                name="evaluate_model_node",
            ),
        ]
    )
