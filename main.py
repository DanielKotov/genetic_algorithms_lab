import random
import time
import itertools
import pandas as pd
import matplotlib.pyplot as plt

# Настройки варианта
A_MAX = 2**20
LENGTH = 24
POPULATION_SIZE = 100
CHROME_LEN = 24
CROSS_PROB = 0.5
MUT_PROB = 0.1
random.seed(100)

# Генерация одной хромосомы
def rand_generation(length):
    return ''.join(str(random.randint(0, 1)) for _ in range(length))

# Генерация популяции
def pop_generation(vector, weight):
    return {rand_generation(CHROME_LEN): fitness(rand_generation(CHROME_LEN), vector, weight) for _ in range(POPULATION_SIZE)}

# Подсчет фитнесс-функции
def fitness(chromosome, vector, weight):
    total = sum(int(chromosome[i]) * vector[i] for i in range(len(vector)))
    return abs(weight - total)

# Кроссинговер двух хромосом
def crossingover(ch1, ch2):
    point = random.randint(0, CHROME_LEN)
    return ch1[:point] + ch2[point:], ch2[:point] + ch1[point:]

# Мутация хромосомы
def mutation(chromosome):
    idx = random.randint(0, CHROME_LEN-1)
    ch_list = list(chromosome)
    ch_list[idx] = str(1 - int(ch_list[idx]))
    return ''.join(ch_list)

# Репродукция
def reproduction(pop):
    sorted_pop = sorted(pop.items(), key=lambda item: item[1])
    probs = [round((i+1)*200/(len(sorted_pop)*(len(sorted_pop)+1)), 2) for i in range(len(sorted_pop))]
    chrom1 = random.choices([item[0] for item in sorted_pop], weights=probs)[0]
    chrom2 = random.choices([item[0] for item in sorted_pop], weights=probs)[0]
    while chrom1 == chrom2:
        chrom2 = random.choices([item[0] for item in sorted_pop], weights=probs)[0]
    return crossingover(chrom1, chrom2)

# Проверка условий выхода
def check_out(count, min_fit, elapsed_time):
    return count == 100 or min_fit == 0 or elapsed_time > 10

# Генетический алгоритм
def genetic(vector, weight):
    population = pop_generation(vector, weight)
    child_pop = {}
    num_gen = 0
    count = 0
    min_fit = float('inf')
    start_time = time.perf_counter()

    while True:
        num_gen += 1
        current_min = min(population.values())
        if current_min == min_fit:
            count += 1
        else:
            count = 0
        min_fit = current_min

        for _ in range(POPULATION_SIZE):
            ch1, ch2 = reproduction(population)
            if random.random() < CROSS_PROB:
                child_pop[ch1] = fitness(ch1, vector, weight)
                child_pop[ch2] = fitness(ch2, vector, weight)

        for ch in list(child_pop.keys()):
            if random.random() < MUT_PROB:
                mutated = mutation(ch)
                child_pop[mutated] = fitness(mutated, vector, weight)

        combined = {**population, **child_pop}
        population = dict(sorted(combined.items(), key=lambda item: item[1])[:POPULATION_SIZE])
        child_pop.clear()

        elapsed_time = time.perf_counter() - start_time
        if check_out(count, min_fit, elapsed_time):
            break

    return elapsed_time, min_fit, num_gen

# Генерация вектора
def vector_gen():
    vec = [random.randint(1, A_MAX) for _ in range(LENGTH)]
    vec.sort()
    return vec

# Генерация задач
def backpack_task(vector):
    part = random.randint(3, 12)
    weight = sum(random.sample(vector, k=part))
    return weight, part

# Полный перебор
def full_enumeration(vector, weight):
    count = 0
    beg = time.perf_counter()
    first_time = -1
    for l in range(1, LENGTH+1):
        for subset in itertools.combinations(vector, l):
            if sum(subset) == weight:
                count += 1
                if count == 1:
                    first_time = time.perf_counter() - beg
    total_time = time.perf_counter() - beg
    return first_time, total_time, count

# Функции для сохранения таблиц

def save_vectors(vectors):
    df = pd.DataFrame({
        'Номер вектора': list(range(1, len(vectors)+1)),
        'Вектор': vectors,
        'Amax': [A_MAX]*len(vectors)
    })
    df.to_excel('Вектора.xlsx', index=False)

def save_tasks(tasks):
    df = pd.DataFrame({
        'Номер задачи': list(range(1, len(tasks)+1)),
        'Номер вектора': [(i//10)+1 for i in range(len(tasks))],
        'Целевой вес': [task[0] for task in tasks],
        'Доля предметов': [task[1] for task in tasks]
    })
    df.to_excel('Задачи.xlsx', index=False)

def save_full_enumeration(results):
    df = pd.DataFrame({
        'Номер задачи': list(range(1, len(results)+1)),
        'Время нахождения первого решения': [res[0] for res in results],
        'Время нахождения всех решений': [res[1] for res in results],
        'Число решений': [res[2] for res in results]
    })
    df.to_excel('Решения_перебор.xlsx', index=False)

def save_genetic(results):
    reasons = []
    for res in results:
        if res[1] == 0:
            reasons.append('Фитнесс функция')
        elif res[0] > 10:
            reasons.append('Превышено время')
        else:
            reasons.append('Неизменяемость поколений')
    df = pd.DataFrame({
        'Номер задачи': list(range(1, len(results)+1)),
        'Время работы алгоритма': [res[0] for res in results],
        'Достигнутый минимум фитнесс-функции': [res[1] for res in results],
        'Причина остановки алгоритма': reasons,
        'Номер последнего поколения': [res[2] for res in results]
    })
    df.to_excel('Решения_генетика.xlsx', index=False)

# Главная программа
if __name__ == "__main__":
    vectors = [vector_gen() for _ in range(50)]
    save_vectors(vectors)

    backpacks = []
    for vector in vectors:
        for _ in range(10):
            backpacks.append(backpack_task(vector))
    save_tasks(backpacks)

    #полный перебор
    full_en_results = []
    for i, vector in enumerate(vectors):
        for j in range(10):
            weight = backpacks[10*i + j][0]
            full_en_results.append(full_enumeration(vector, weight))
    save_full_enumeration(full_en_results)

    # генетический алгоритм
    genetic_results = []
    for i, vector in enumerate(vectors):
        for j in range(10):
            weight = backpacks[10*i + j][0]
            genetic_results.append(genetic(vector, weight))
    save_genetic(genetic_results)

    print("\nГотово! Все таблицы сохранены.")
