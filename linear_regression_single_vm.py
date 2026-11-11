import csv
import time

input_file = "sales_logs.csv"

# 1. Замеряем время начала работы (важно для отчета по лабораторной)
start_time = time.time()

# Словари для агрегации: ключ — номер дня, значение — сумма продаж за этот день
daily_sales = {}

print("Шаг 1: Чтение файла и последовательная агрегация выручки по дням...")
with open(input_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    
    # Пропускаем заголовок, если он есть в файле
    header = next(reader, None) 
    
    for row in reader:
        if not row:
            continue
        try:
            # Структура: order_id, day_number, amount
            day = int(row[1])
            amount = float(row[2])
            
            # Суммируем выручку для каждого дня
            daily_sales[day] = daily_sales.get(day, 0.0) + amount
        except (ValueError, IndexError):
            # Пропускаем битые строки, если они встретятся
            continue

# 2. Вычисление компонентов метода наименьших квадратов (МНК)
print("Шаг 2: Расчет коэффициентов линейной аппроксимации...")
n = len(daily_sales)  # Количество дней (должно быть ~3652)

sum_x = 0.0
sum_y = 0.0
sum_xx = 0.0
sum_xy = 0.0

# Проходим последовательно по каждому дню в один поток
for day, revenue in daily_sales.items():
    x = float(day)
    y = revenue
    
    sum_x += x
    sum_y += y
    sum_xx += x * x
    sum_xy += x * y

# 3. Финальный расчет коэффициентов по формулам МНК
# Формула прямой: y = a*x + b
# Числитель и знаменатель для коэффициента наклона 'a'
numerator_a = (n * sum_xy) - (sum_x * sum_y)
denominator_a = (n * sum_xx) - (sum_x**2)

if denominator_a == 0:
    print("Ошибка: знаменатель равен нулю, невозможно рассчитать аппроксимацию.")
    exit()

a = numerator_a / denominator_a
b = (sum_y - (a * sum_x)) / n

end_time = time.time()
execution_time = end_time - start_time

# 4. Вывод результатов
print("\n" + "="*40)
print("РЕЗУЛЬТАТЫ ПОСЛЕДОВАТЕЛЬНОЙ ОБРАБОТКИ (1 ВМ):")
print("="*40)
print(f"Уравнение тренда: Y = {a:.4f} * X + {b:.2f}")
print(f"Скорость роста продаж в день (коэффициент a): {a:.2f} руб./день")
print(f"Стартовая выручка в день 1 (коэффициент b): {b:.2f} руб.")
print(f"Время выполнения скрипта: {execution_time:.4f} секунд")
print("="*40)

