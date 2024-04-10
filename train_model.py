from clearml import Task
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Инициализируем задачу ClearML
task = Task.init(project_name="предсказание цен на недвижимость", task_name="предсказание цен на недвижимость в clearml")

# Загружаем данные
df = pd.read_excel('cleaned.xlsx')

# Визуализация распределения цен
df['Цена'] = df['Цена'] / 1000000

plt.hist(df['Цена'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Цена (в миллионах)')
plt.ylabel('Количество квартир')
plt.title('Распределение цен квартир (в миллионах)')
plt.grid(True)
plt.show()

# Отправляем данные в ClearML
task.upload_artifact('histogram.png', artifact_object=plt.gcf())

# Зависимость цены от площади
plt.scatter(df['Площадь'], df['Цена'])
plt.xlabel('Площадь')
plt.ylabel('Цена')
plt.title('Зависимость цены от площади')
plt.show()

# Отправляем данные в ClearML
task.upload_artifact('scatter_plot.png', artifact_object=plt.gcf())

# Влияние количества комнат на цену
sns.boxplot(x='Количество комнат', y='Цена', data=df)
plt.xlabel('Количество комнат')
plt.ylabel('Цена')
plt.title('Влияние количества комнат на цену')
plt.show()

# Отправляем данные в ClearML
task.upload_artifact('boxplot.png', artifact_object=plt.gcf())

# Влияние этажа на цену
df['Этаж'] = df['Этаж'].str.extract('(\d+)').astype(float)

sns.kdeplot(data=df, x='Этаж', y='Цена', fill=True)
plt.xlabel('Этаж')
plt.ylabel('Цена')
plt.title('Влияние этажа на цену')
plt.show()

# Отправляем данные в ClearML
task.upload_artifact('kdeplot.png', artifact_object=plt.gcf())

# Матрица корреляции
df['Расстояние до метро (мин)'] = df['Метро'].str.extract('(\d+)').astype(float)

df_numeric = df.select_dtypes(include=['float64', 'int64'])

correlation_matrix = df_numeric.corr()

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Матрица корреляции')
plt.show()

# Отправляем данные в ClearML
task.upload_artifact('correlation_matrix.png', artifact_object=plt.gcf())
# Завершаем задачу ClearML
task.close()