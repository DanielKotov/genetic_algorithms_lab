import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные
df_enum = pd.read_excel('Решения_перебор.xlsx')
df_gen = pd.read_excel('Решения_генетика.xlsx')

# Группировка (по сути у нас один amax, так что считаем просто по всем задачам)

# 1. Среднее время нахождения одного решения
mean_first_enum = df_enum['Время нахождения первого решения'].mean()

# 2. Среднее время нахождения всех решений
mean_all_enum = df_enum['Время нахождения всех решений'].mean()

# 3. Среднее время работы ГА на точно решённых задачах
solved_by_ga = df_gen[df_gen['Достигнутый минимум фитнесс-функции'] == 0]
mean_ga_time = solved_by_ga['Время работы алгоритма'].mean()

# 4. Доля точно решённых задач генетическим алгоритмом
success_rate_ga = len(solved_by_ga) / len(df_gen)


# График 1: Время работы полного перебора
plt.figure()
plt.bar(['Первое решение', 'Все решения'], [mean_first_enum, mean_all_enum])
plt.title('Среднее время решения задачи полным перебором')
plt.ylabel('Время (сек.)')
plt.grid(True)
plt.savefig('plot_enum_time.png')

# График 2: Время работы генетического алгоритма
plt.figure()
plt.bar(['Генетический алгоритм'], [mean_ga_time])
plt.title('Среднее время работы генетического алгоритма (точные решения)')
plt.ylabel('Время (сек.)')
plt.grid(True)
plt.savefig('plot_ga_time.png')

# График 3: Доля задач, решённых ГА
plt.figure()
plt.bar(['Точные решения генетическим алгоритмом'], [success_rate_ga])
plt.title('Доля точно решённых задач генетическим алгоритмом')
plt.ylabel('Доля')
plt.grid(True)
plt.savefig('plot_ga_success.png')

print("Графики построены и сохранены.")

