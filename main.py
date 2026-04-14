from utils import *
from solver import *

import sys
from PyQt5.QtWidgets import QApplication
from visualizer import MainWindow 

def main():
    # Создаем экземпляр приложения PyQt5
    app = QApplication(sys.argv)
    
    # Создаем и показываем главное окно
    window = MainWindow()
    window.show()
    
    # Запускаем цикл обработки событий
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

#w = 1 - Емкость рюкзака
'''
n = int(input("Введите количество предметов>>"))
x = int(input("Введите максимальную стоимость предмета>>"))


# Списки-словари для равномерного и нормального распределений
itemsUniform = uniform_distribution(n, x)
itemsNormal = normal_distribution(n, x)

#items = normal_distribution(n, x)
        

choiseVar = input()

textVar = {
    "1": "равномерного",
    "2": "нормального"
}
var = {
    "1": itemsUniform,
    "2": itemsNormal
}

#print(f"Равномерное распределение {itemsUniform}")
#print(f"Нормальное распределение {itemsNormal}")

# Жадный для равномерного
start = time.perf_counter()
sorted_items, total_v, total_cost = greedy_algo(itemsUniform, w)
end = time.perf_counter()
print("Жадный алгоритм для равномерного распределения:")
print("\n".join(f"Индекс: {i['index']}, Вес: {i['weight']:.5f}, Цена: {i['price']:.5f}" for i in sorted_items))
print(f"\nИтоговый вес: {total_v}")
print(f"Итоговая стоимость: {total_cost}\n")
print(f"Выполнено за: {end - start:.8f} сек.")


# Жадный для нормального
start = time.perf_counter()
sorted_items, total_v, total_cost = greedy_algo(itemsNormal, w)
end = time.perf_counter()
print("Жадный алгоритм для нормального распределения:")
print("\n".join(f"Индекс: {i['index']}, Вес: {i['weight']:.5f}, Цена: {i['price']:.5f}" for i in sorted_items))
print(f"\nИтоговый вес: {total_v}")
print(f"Итоговая стоимость: {total_cost}\n")
print(f"Выполнено за: {end - start:.8f} сек.")

# Ветвей и границ для равномерного
start = time.perf_counter()
sorted_items, total_v, total_cost = branch_boundary_method(itemsUniform, 1)
end = time.perf_counter()
print("\nМетод ветвей и границ для нормального распределения:")
print("\n".join(f"Индекс: {i['index']}, Вес: {i['weight']:.5f}, Цена: {i['price']:.5f}" for i in sorted_items))
print(f"\nИтоговый вес: {total_v}")
print(f"Итоговая стоимость: {total_cost}\n")
print(f"Выполнено за: {end - start:.8f} сек.\n")

# Ветвей и границ для нормального
start = time.perf_counter()
sorted_items, total_v, total_cost = branch_boundary_method(itemsNormal, 1)
end = time.perf_counter()
print("\nМетод ветвей и границ для нормального распределения:")
print("\n".join(f"Индекс: {i['index']}, Вес: {i['weight']:.5f}, Цена: {i['price']:.5f}" for i in sorted_items))
print(f"\nИтоговый вес: {total_v}")
print(f"Итоговая стоимость: {total_cost}\n")
print(f"Выполнено за: {end - start:.8f} сек.\n")'''