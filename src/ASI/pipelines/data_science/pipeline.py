from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["model_input", "params:model_options"],
                outputs=["Xy_train", "Xy_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["Xy_train"],
                outputs="model_output",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["model_output", "Xy_test"],
                outputs="prediction",
                name="evaluate_model_node",
            ),
        ]
    )
