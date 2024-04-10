import pandas as pd
import glob

# Получение списка файлов Excel в текущей директории
excel_files = glob.glob('offers/*.xlsx')

# Чтение всех файлов Excel и объединение их в один DataFrame
dfs = []
for file in excel_files:
    dfs.append(pd.read_excel(file))

merged_df = pd.concat(dfs, ignore_index=True)

# Сохранение объединенной таблицы в новый файл Excel
merged_df.to_excel('merged.xlsx', index=False)
