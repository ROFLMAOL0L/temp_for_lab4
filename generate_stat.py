import csv
import random

# Константы для 10 лет (учитывая високосные годы)
TOTAL_DAYS = 3652  
# Сколько заказов в среднем происходит за один день (для объема)
ORDERS_PER_DAY = 50  

# Настройки тренда
BASE_SALES = 10000  # Начальная выручка в день 1
TREND_PER_DAY = 300 # На сколько рублей растет общая выручка каждый день

output_file = "sales_logs.csv"
order_id = 1

print("Генерация данных запущена...")

with open(output_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Заголовки (для MapReduce их можно не делать, чтобы не мешались, но оставим для наглядности)
    # Если мешают в коде Hadoop — просто удалите эту строчку
    writer.writerow(["order_id", "day_number", "amount"])
    
    for day in range(1, TOTAL_DAYS + 1):
        # Вычисляем целевую выручку на этот день с учетом тренда
        target_day_revenue = BASE_SALES + (TREND_PER_DAY * (day - 1))
        
        # Распределяем эту выручку на несколько случайных заказов
        accumulated_revenue = 0
        for i in range(ORDERS_PER_DAY):
            # Средний чек одного заказа в этот день
            avg_order_amount = target_day_revenue / ORDERS_PER_DAY
            
            # Добавляем центрированный случайный шум к каждому заказу (от -100 до 100)
            noise = random.uniform(-100, 100)
            order_amount = round(max(10, avg_order_amount + noise), 2)
            
            writer.writerow([order_id, day, order_amount])
            order_id += 1

print(f"Готово! Сгенерирован файл {output_file} со структурой для Hadoop.")
