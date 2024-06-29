from kedro.pipeline import Pipeline, node, pipeline

from .nodes import fetch_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=fetch_data,
                inputs=None,
                outputs=["aoi_depressive_1", "aoi_depressive_2", "aoi_control_1", "event_depressive_1", "event_depressive_2", "event_control_1"],
                name="fetch_data_node",
            )
        ]
    )
