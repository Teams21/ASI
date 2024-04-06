import pandas as pd
pd.set_option('display.max_columns', None)

df1 = pd.read_csv(f'../../data/rawdata/depresja_2grupy/Event Statistics - Trial Summary.txt', sep='\t')
df2 = pd.read_csv(f'../../data/rawdata/depresja_2grupy/Event Statistics - Trial Summary (1).txt', sep='\t')
df3 = pd.read_csv(f'../../data/rawdata/depresja kontrolni/Event Statistics - Trial Summary (1).txt', sep='\t')

# concat df1 and df2 datasets
df = pd.concat([df1, df2, df3])

# drop dataframe columns with only one distinct value
df = df[[c for c
        in list(df)
        if len(df[c].unique()) > 1]]

# remove all rows where column contains richtext.jpg
df = df[df.Stimulus != 'richtext.jpg']

# sort by Participant then Trial
df.sort_values(by=['Participant', 'Trial'], inplace=True, ignore_index=True)

# Find locations of '-'
df.replace('-', 0, inplace=True)

# hack to avoid issues with inferred parquet data type mismatch
for c in df.columns:
    df[c] = df[c].astype(str)


    # Replace participant with an index to make sure everyone is anonmyous
for idx, name in enumerate(df['Participant'].sort_values().unique()):
    df.replace({'Participant': {f'{name}': idx}}, inplace=True)

df.sort_values(by=['Participant', 'Trial'], inplace=True)

df.to_parquet('../../output/event_stats.parquet')