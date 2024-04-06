import pandas as pd
pd.set_option('display.max_columns', None)

def squash_rows(rows):
    '''
    Squash data from rows to columns (dummyfication)
    Turn for example two rows - happy, sad - for person A into one row with extra columns 'A happy', 'A sad'
    '''
    drop_rows = ["Trial", "Stimulus", "Export End Trial Time [ms]", "Participant", "Color", "Class"]
    result = {}
    for row in drop_rows:
        result[row] = rows[row].iloc[0]
        
    t = rows.drop(drop_rows, axis=1)
    # Adding AOI details
    for index, row in rows.iterrows():
        for col in list(t.drop(['AOI Name'], axis=1).columns):
            result[f"{col} {row['AOI Name']}"] = row[col]

    return result


# open depressive files
df1 = pd.read_csv(f'../../data/rawdata/depresja_2grupy/AOI Statistics - Trial Summary (AOI).txt', sep='\t')
df2 = pd.read_csv(f'../../data/rawdata/depresja_2grupy/AOI Statistics - Trial Summary (AOI) (2).txt', sep='\t')

# concat df1 and df2 datasets
df = pd.concat([df1, df2])

# add class column for classification
df['Class'] = 'depressive'

# open control group file
df3 = pd.read_csv(f'../../data/rawdata/depresja kontrolni/AOI Statistics - Trial Summary (AOI) (1).txt', sep='\t')

# add class column for classification
df3['Class'] = 'control'
# concat df and df3 datasets
df = pd.concat([df, df3])

# Feauture engineering

# drop dataframe columns with only one distinct value
df = df[[c for c
        in list(df)
        if len(df[c].unique()) > 1]]

# remove all rows where column contains richtext.jpg
df = df[df.Stimulus != 'richtext.jpg']

# few values in 'AOI Name' column are wrong, this is a fix
df.replace(to_replace='happy (1)', value='happy', inplace=True)

# Find locations of '-'
df.replace('-', 0, inplace=True)

# hack to avoid issues with inferred parquet data type mismatch
for c in df.columns:
    df[c] = df[c].astype(str)

# sort by Participant then Trial
df.sort_values(by=['Participant', 'Trial'], inplace=True, ignore_index=True)


rows_list = []

dataset_start = 0
dataset_end = df.shape[0]
squash_count = 5

# squash 5 rows into one for all rows in the dataset
for row_border in range (dataset_start, dataset_end, squash_count):
    squashed_row = squash_rows(df.iloc[row_border:row_border + 5])
    rows_list.append(squashed_row)

df = pd.DataFrame.from_records(rows_list)


# Check for any NaN values in the dataframe
df.columns[df.isna().any()].tolist()


# Replace participant with an index to make sure everyone is anonmyous
for idx, name in enumerate(df['Participant'].sort_values().unique()):
    df.replace({'Participant': {f'{name}': idx}}, inplace=True)

df.sort_values(by=['Participant', 'Trial'], inplace=True)
df.to_parquet('../../output/aoi_stats.parquet')