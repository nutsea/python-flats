import pandas as pd
import re
from sqlalchemy import create_engine

df = pd.read_excel('merged.xlsx')

# очистка от ненужных столбцов
columns_to_drop = ['Доля', 'Телефоны', 'Описание', 'Окна', 'Санузел', 
                   'Есть телефон', 'Серия дома', 'Лифт', 'Мусоропровод', 
                   'Ссылка на объявление', 'Площадь комнат, м2', 'Балкон']

df.drop(columns=columns_to_drop, inplace=True)


# редактирование цен
def extract_price(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return match.group(1)
    else:
        return None

df['Цена'] = df['Цена'].apply(extract_price)


# редактирование сроков сдачи
def extract_year(text):
    if pd.isnull(text):
        return None
    match = re.search(r'\b(\d{4})\b', str(text))
    if match:
        return match.group(1)
    else:
        return None

df.rename(columns={'Название ЖК': 'Срок сдачи'}, inplace=True)

df['Срок сдачи'] = df['Срок сдачи'].apply(extract_year)


# редактирование количества комнат
def extract_room_count(text):
    if isinstance(text, str):
        match = re.search(r'(\d+)', text)
        if match:
            return match.group(1)
    return None

df['Количество комнат'] = df['Количество комнат'].apply(extract_room_count)


# редактирование новостроек
df.rename(columns={'Тип': 'Новостройка'}, inplace=True)

df['Новостройка'] = df['Новостройка'].apply(lambda x: 1 if 'новостройке' in x.lower() else 0)


# редактирование площадей
df.rename(columns={'Площадь, м2': 'Площадь'}, inplace=True)

df['Площадь'] = df['Площадь'].str.split('/').str[0]


# редактирование этажей и типа дома
df[['Этаж', 'Дом']] = df['Дом'].str.split(',', expand=True)

df['Этаж'] = df['Этаж'].str.strip()
df['Дом'] = df['Дом'].str.strip()


# редактирование парковки
df['Парковка'].fillna(0, inplace=True)

df['Парковка'] = df['Парковка'].apply(lambda x: 1 if x != 0 else 0)


# редактирование ремонта
remont_mapping = {'Без ремонта': 0, 'Косметический': 1, 'Евроремонт': 2, 'Дизайнерский': 2}
df['Ремонт'] = df['Ремонт'].map(remont_mapping).fillna(0).astype(int)


# удаление домов с неизвестным местоположением
df.dropna(subset=['Метро'], inplace=True)


# очистка от дубликатов
df.drop_duplicates(subset=['Адрес', 'Цена'], keep='first', inplace=True)

df.to_excel('cleaned.xlsx', index=False)