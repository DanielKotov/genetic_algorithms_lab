import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загружаем данные
df_enum = pd.read_excel('Решения_перебор.xlsx')
df_gen = pd.read_excel('Решения_генетика.xlsx')

# Фильтрация задач, решённых генетическим алгоритмом
df_gen_solved = df_gen[df_gen['Достигнутый минимум фитнесс-функции'] == 0]

# Расчёты для таблицы

# 1. Время нахождения одного решения полным перебором
first_enum_mean = df_enum['Время нахождения первого решения'].mean()
first_enum_var = df_enum['Время нахождения первого решения'].var()
first_enum_std = df_enum['Время нахождения первого решения'].std()

# 2. Время нахождения всех решений полным перебором
all_enum_mean = df_enum['Время нахождения всех решений'].mean()
all_enum_var = df_enum['Время нахождения всех решений'].var()
all_enum_std = df_enum['Время нахождения всех решений'].std()

# 3. Время нахождения точного решения генетическим алгоритмом
ga_mean = df_gen_solved['Время работы алгоритма'].mean()
ga_var = df_gen_solved['Время работы алгоритма'].var()
ga_std = df_gen_solved['Время работы алгоритма'].std()

# 4. Доля задач, точно решённых генетическим алгоритмом
success_rate = len(df_gen_solved) / len(df_gen)

# 5. Количество хромосом в поколении
chromosomes = 100

# Формируем таблицу 5
data = {
    'Показатель': [
        'Время нахождения одного решения полным перебором',
        'Время нахождения всех решений полным перебором',
        'Время нахождения точного решения генетическим алгоритмом',
        'Доля задач, точно решённых генетическим алгоритмом',
        'Количество хромосом в поколении'
    ],
    'Среднее значение': [
        first_enum_mean,
        all_enum_mean,
        ga_mean,
        success_rate,
        chromosomes
    ],
    'Дисперсия': [
        first_enum_var,
        all_enum_var,
        ga_var,
        '',
        ''
    ],
    'Среднее квадратическое отклонение': [
        first_enum_std,
        all_enum_std,
        ga_std,
        '',
        ''
    ]
}

df_summary = pd.DataFrame(data)

# Сохраняем таблицу
df_summary.to_excel('Таблица5_Статистика.xlsx', index=False)

print("Таблица 5 успешно создана!")
