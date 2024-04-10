import pandas as pd

df = pd.read_excel('cleaned.xlsx')

df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

test_size = int(len(df_shuffled) * 0.1)

df_test = df_shuffled.iloc[:test_size]
df_train = df_shuffled.iloc[test_size:]

df_test.to_excel('test.xlsx', index=False)
df_train.to_excel('learn.xlsx', index=False)