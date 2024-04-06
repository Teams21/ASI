import pandas as pd

# load parquet files as pandas dataframe
aoi = pd.read_parquet('../../output/aoi_stats.parquet')
event = pd.read_parquet('../../output/event_stats.parquet')

df = pd.concat([aoi, event], axis=1)
duplicate_columns = df.columns[df.columns.duplicated()].unique().values
duplicate_columns

df = df.loc[:, ~df.columns.duplicated()]


from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(df, test_size=0.2, stratify=df['Class'])
X_test.to_parquet('../../output/X_test.parquet')
X_train


X_test.loc[X_test['Class'] == 'control']


from pycaret.classification import *

s = setup(X_train, target = 'Class', session_id = 123)

best = compare_models()

save_model(best, '../../model/model_oczy')

display((prediction['Class'] == prediction['prediction_label']).sort_values())