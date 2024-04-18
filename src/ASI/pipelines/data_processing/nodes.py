import pandas as pd

def _squash_rows(rows: pd.DataFrame) -> dict[str, str]:
    '''
    Squash data from rows to columns (dummyfication)
    Turn for example two rows - happy, sad - for person 'A' into one row with extra columns 'A happy', 'A sad'
    '''
    drop_rows = ["Trial", "Stimulus", "Export End Trial Time [ms]", "Participant", "Color", "Class"]
    result = {}
    for row in drop_rows:
        result[row] = rows[row].iloc[0]
        
    t = rows.drop(drop_rows, axis=1)
    # Adding AOI details
    for _, row in rows.iterrows():
        for col in list(t.drop(['AOI Name'], axis=1).columns):
            result[f"{col} {row['AOI Name']}"] = row[col]

    return result

def _anonymize_sort(frame: pd.DataFrame) -> pd.DataFrame:
    # Replace participant with an index to make sure everyone is anonmyous
    for idx, name in enumerate(frame['Participant'].sort_values().unique()):
        frame.replace({'Participant': {f'{name}': idx}}, inplace=True)

    # Sort all rows in participant then trial order
    frame.sort_values(by=['Participant', 'Trial'], inplace=True)

    # There are rows with values that cause a conversion error when saving csv -> parquet, this is a fix
    frame = _fix_parquet_save_error(frame)

    return frame

def _fix_parquet_save_error(frame: pd.DataFrame) -> pd.DataFrame:
    # hack to avoid issues with inferred parquet data type mismatch
    for c in frame.columns:
        frame[c] = frame[c].astype(str)

    return frame

def combine_aoi(aoi_depressive_1: pd.DataFrame, aoi_depressive_2: pd.DataFrame, aoi_control_1: pd.DataFrame) -> pd.DataFrame:

    # concat aoi_depressive_1 and aoi_depressive_2 datasets
    aoi_depressive = pd.concat([aoi_depressive_1, aoi_depressive_2])

    # add class column for classification
    aoi_depressive['Class'] = 'depressive'

    # add class column for classification
    aoi_control_1['Class'] = 'control'

    # concat aoi_depressive and aoi_control_1 datasets
    aoi_full = pd.concat([aoi_depressive, aoi_control_1])

    # There are rows with values that cause a conversion error when saving csv -> parquet, this is a fix
    aoi_full = _fix_parquet_save_error(aoi_full)

    return aoi_full

def combine_event(event_depressive_1: pd.DataFrame, event_depressive_2: pd.DataFrame, event_control_1: pd.DataFrame) -> pd.DataFrame:

    # concat event_depressive_1, event_depressive_2 and event_control_1 datasets
    event_full = pd.concat([event_depressive_1, event_depressive_2, event_control_1])

    # There are rows with values that cause a conversion error when saving csv -> parquet, this is a fix
    event_full = _fix_parquet_save_error(event_full)
    
    return event_full

def aoi_data_eng(combined_aoi: pd.DataFrame, parameters: dict[str, int]) -> pd.DataFrame:
    
    # drop dataframe columns with only one distinct value
    combined_aoi = combined_aoi[[c for c
            in list(combined_aoi)
            if len(combined_aoi[c].unique()) > 1]]

    # remove all rows where column contains richtext.jpg
    combined_aoi.to_csv('test.csv', index=False)
    combined_aoi = combined_aoi[combined_aoi['Stimulus'] != 'richtext.jpg']

    # few values in 'AOI Name' column are wrong, this is a fix
    combined_aoi.replace(to_replace='happy (1)', value='happy', inplace=True)

    # Find locations of '-'
    combined_aoi.replace('-', 0, inplace=True)

    # sort by Participant then Trial
    combined_aoi.sort_values(by=['Participant', 'Trial'], inplace=True, ignore_index=True)

    rows_list = []
    dataset_start = parameters['dataset_start']
    squash_count = parameters['squash_count']
    dataset_end = combined_aoi.shape[0]

    # squash 5 rows into one for all rows in the dataset
    for row_border in range (dataset_start, dataset_end, squash_count):
        rows = combined_aoi.iloc[row_border:row_border + squash_count]
        squashed_row = _squash_rows(rows)
        rows_list.append(squashed_row)

    # Create dataframe from list
    combined_aoi = pd.DataFrame.from_records(rows_list)

    # Check for any NaN values in the dataframe
    combined_aoi.columns[combined_aoi.isna().any()].tolist()

    # Run few aggregated methods that fixes issues with the dataset
    combined_aoi = _anonymize_sort(combined_aoi)

    

    return combined_aoi

def event_data_eng(combined_event: pd.DataFrame) -> pd.DataFrame:

    # drop dataframe columns with only one distinct value
    combined_event = combined_event[[c for c
            in list(combined_event)
            if len(combined_event[c].unique()) > 1]]

    # remove all rows where column contains richtext.jpg
    combined_event = combined_event[combined_event['Stimulus'] != 'richtext.jpg']

    # sort by Participant then Trial
    combined_event.sort_values(by=['Participant', 'Trial'], inplace=True, ignore_index=True)

    # Find locations of '-'
    combined_event.replace('-', 0, inplace=True)

    # Run few aggregated methods that fixes issues with the dataset
    combined_event = _anonymize_sort(combined_event)

    return combined_event

def merge_aoi_w_events(combined_aoi: pd.DataFrame, combined_event: pd.DataFrame) -> pd.DataFrame:

    # Concat aoi and event
    merged = pd.concat([combined_aoi, combined_event], axis=1)
    merged = merged.loc[:, ~merged.columns.duplicated()]

    # There are rows with values that cause a conversion error when saving csv -> parquet, this is a fix
    merged = _fix_parquet_save_error(merged)

    return merged
