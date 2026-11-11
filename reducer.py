#!/usr/bin/env python3
import sys

current_day = None
current_day_revenue = 0.0

# Переменные для метода наименьших квадратов (МНК)
n = 0
sum_x = 0.0
sum_y = 0.0
sum_xx = 0.0
sum_xy = 0.0

def add_day_to_ols(day, revenue):
    global n, sum_x, sum_y, sum_xx, sum_xy
    x = float(day)
    y = float(revenue)
    n += 1
    sum_x += x
    sum_y += y
    sum_xx += x * x
    sum_xy += x * y

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    try:
        day_str, amount_str = line.split('\t', 1)
        day = int(day_str)
        amount = float(amount_str)
    except ValueError:
        continue

    # Так как Hadoop сортирует ключи перед подачей в Reducer, 
    # все записи за один день идут строго подряд
    if current_day == day:
        current_day_revenue += amount
    else:
        if current_day is not None:
            # День закончился — добавляем его итоговую выручку в формулу МНК
            add_day_to_ols(current_day, current_day_revenue)
        current_day = day
        current_day_revenue = amount

# Не забываем учесть самый последний день после окончания цикла
if current_day is not None:
    add_day_to_ols(current_day, current_day_revenue)

# Финальный расчет коэффициентов прямой Y = a*X + b
if n > 0:
    numerator_a = (n * sum_xy) - (sum_x * sum_y)
    denominator_a = (n * sum_xx) - (sum_x ** 2)
    
    if denominator_a != 0:
        a = numerator_a / denominator_a
        b = (sum_y - (a * sum_x)) / n
        
        print("="*45)
        print("РЕЗУЛЬТАТЫ РАСПРЕДЕЛЕННОЙ ОБРАБОТКИ (HADOOP):")
        print(f"Обработано дней (n): {n}")
        print(f"Уравнение тренда: Y = {a:.4f} * X + {b:.2f}")
        print(f"Скорость роста (a): {a:.2f} руб./день")
        print(f"Стартовая выручка (b): {b:.2f} руб.")
        print("="*45)
    else:
        print("Ошибка: деление на ноль при расчете.")
