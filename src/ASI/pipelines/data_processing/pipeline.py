from kedro.pipeline import Pipeline, node, pipeline

from .nodes import merge_aoi_w_events, combine_aoi, aoi_data_eng, combine_event, event_data_eng


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=combine_aoi,
                inputs=["aoi_depressive_1", "aoi_depressive_2", "aoi_control_1"],
                outputs="combined_aoi",
                name="combine_aoi_node",
            ),
            node(
                func=aoi_data_eng,
                inputs=["combined_aoi", "params:dummy_loop_options"],
                outputs="combined_aoi_ready",
                name="aoi_data_eng_node",
            ),
            node(
                func=combine_event,
                inputs=["event_depressive_1", "event_depressive_2", "event_control_1"],
                outputs="combined_event",
                name="combine_event_node",
            ),
            node(
                func=event_data_eng,
                inputs=["combined_event"],
                outputs="combined_event_ready",
                name="event_data_eng_node",
            ),
            node(
                func=merge_aoi_w_events,
                inputs=["combined_aoi_ready", "combined_event_ready"],
                outputs="input_dataset",
                name="merge_aoi_w_events_node",
            )
        ]
    )
