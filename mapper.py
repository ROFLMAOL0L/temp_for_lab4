#!/usr/bin/env python3
import sys

# Локальный словарь для частичной агрегации (работает как Combiner)
# Это критически ускорит работу кластера и снизит нагрузку на сеть между Worker-нодами
local_daily_sales = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    parts = line.split(',')
    # Пропускаем заголовок, если он есть, или битые строки
    if len(parts) != 3 or parts[0] == "order_id":
        continue
        
    try:
        day = int(parts[1])
        amount = float(parts[2])
        local_daily_sales[day] = local_daily_sales.get(day, 0.0) + amount
    except ValueError:
        continue

# Выводим промежуточные итоги по дням в стандартный вывод для Reducer
for day, total_amount in local_daily_sales.items():
    print(f"{day}\t{total_amount}")
