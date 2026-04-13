from utils import *
from solver import *
import time

w = 1 # Емкость рюкзака

n = int(input("Введите количество предметов>>"))
x = int(input("Введите максимальную стоимость предмета>>"))

# Списки-словари для равномерного и нормального распределений
itemsUniform = uniform_distribution(n, x)
itemsNormal = normal_distribution(n, x)

'''choiseVar = input()

textVar = {
    "1": "равномерного",
    "2": "нормального"
}
var = {
    "1": itemsUniform,
    "2": itemsNormal
}'''

#print(f"Равномерное распределение {itemsUniform}")
#print(f"Нормальное распределение {itemsNormal}")

#Жадный для равномерного
start = time.perf_counter()
sorted_items, total_v, total_cost = greedy_algo(itemsUniform, w)
end = time.perf_counter()
print("Жадный алгоритм для равномерного распределения:")
print("\n".join(f"Индекс: {i['index']}, Вес: {i['weight']:.5f}, Цена: {i['price']:.5f}" for i in sorted_items))
print(f"\nИтоговый вес: {total_v}")
print(f"Итоговая стоимость: {total_cost}\n")
print(f"Выполнено за: {end - start:.8f} сек.")


#Жадный для нормального
start = time.perf_counter()
sorted_items, total_v, total_cost = greedy_algo(itemsNormal, w)
end = time.perf_counter()
print("Жадный алгоритм для нормального распределения:")
print("\n".join(f"Индекс: {i['index']}, Вес: {i['weight']:.5f}, Цена: {i['price']:.5f}" for i in sorted_items))
print(f"\nИтоговый вес: {total_v}")
print(f"Итоговая стоимость: {total_cost}\n")
print(f"Выполнено за: {end - start:.8f} сек.")