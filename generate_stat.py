import csv
import random

TOTAL_DAYS = 3652  
ORDERS_PER_DAY = 5000  # Теперь здесь может быть любое число!

BASE_SALES = 10000  
TREND_PER_DAY = 300 

output_file = "sales_logs.csv"
order_id = 1

print("Генерация данных запущена (исправленная версия)...")

with open(output_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    for day in range(1, TOTAL_DAYS + 1):
        # 1. Сначала считаем точную целевую выручку дня с учетом тренда
        target_day_revenue = BASE_SALES + (TREND_PER_DAY * (day - 1))
        
        # 2. Добавляем случайный шум к выручке ВСЕГО дня (а не к каждому заказу)
        # Шум центрирован относительно нуля и не уведет выручку в минус
        day_noise = random.uniform(-2000, 2000) 
        actual_day_revenue = max(1000, target_day_revenue + day_noise)
        
        # 3. Делим полученную выручку дня на ORDERS_PER_DAY частей
        # Создаем случайные веса, чтобы заказы были разными по сумме
        weights = [random.uniform(0.5, 1.5) for _ in range(ORDERS_PER_DAY)]
        total_weight = sum(weights)
        
        # Записываем заказы
        for w in weights:
            # Пропорционально выделяем долю от общей выручки дня для этого заказа
            order_amount = round((w / total_weight) * actual_day_revenue, 2)
            
            writer.writerow([order_id, day, order_amount])
            order_id += 1
            
        if day % 500 == 0:
            print(f"Сгенерировано дней: {day}/{TOTAL_DAYS}...")

print(f"Готово! Сгенерирован правильный файл {output_file}.")
