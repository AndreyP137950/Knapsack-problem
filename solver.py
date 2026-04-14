import heapq

# Жадный алгоритм
def greedy_algo(Lst, w):
    # Создаем список с соотношением цена/вес
    grLst = Lst.copy()
    
    # Сортировка по цене/весу (убывание)
    grLst.sort(key=lambda x: x["price"]/x["weight"], reverse=True)
    rLst = [] #результирующий список
    v = cost = 0 #вместимость и суммарная стоимость
    for item in grLst:
        if item["weight"] <= w-v: #проверка, что вес элемента <= остав. объема
            rLst.append(item)
            v += item["weight"]
            cost += item["price"]
    return rLst, v, cost

# Метод ветвей и границ
# Класс для создания узлов
class Node:
    def __init__(self, level, price, weight, bound=0, items_list=None):
        self.level = level #уровень/индекс предмета
        self.price = price #суммарная стоимость предметов в этом узле
        self.weight = weight #суммарный вес предметов в этом узле
        self.bound = bound #максимальный потенциал ветки
        self.items_list = items_list
    def __lt__(self, other): #сравнение параметров узлов bound 
        return self.bound > other.bound  #наибольший bound

# Функция создания хорошего прогноза
def get_bound(node, n, w, items):
    if node.weight >= w:
        return 0
    profit_bound   = node.price#хороший прогноз
    current_weight = node.weight#текущий вес
    j = node.level + 1

    # Жадно забираем самое ценное
    while j<n and current_weight+items[j]["weight"] <= w:
        current_weight += items[j]["weight"]
        profit_bound   += items[j]["price"]
        j += 1
    
    if j < n: #дополняем прогноз кусочком следующего по цена/вес
        profit_bound += (items[j]["price"]/items[j]["weight"])*(w-current_weight)
    return profit_bound

def branch_boundary_method(items, w):
    items.sort(key=lambda x: x["price"]/x["weight"], reverse=True)
    n = len(items)
    queue = [] #создаем список-очередь
    max_profit = 0 #создаем переменную

    # Создаем первый узел (level -1, так как первый предмет будет под индексом 0)
    root = Node(level=-1, price=0, weight=0, bound=0, items_list=[])
    root.bound = get_bound(root, n, w, items)
    heapq.heappush(queue, root) #добавление в очередь queue узла root с учетом приоритета
    while queue:
        current_node = heapq.heappop(queue) #достаем узел с самым большим bound
        # Если профит у узла меньше максимального, скипаем
        if current_node.bound <= max_profit: 
            continue
        next_level = current_node.level + 1
        # Проверка на то, что мы обработали все предметы
        if next_level >= len(items):
            continue

        item = items[next_level]

        # Берем предмет и проверяем, влезет ли он (наследник БЕРЕМ)
        if current_node.weight + item["weight"] <= w:
            # Список предметов для нового узла (старые + текущие)
            new_list = current_node.items_list + [item]

            left_child = Node(
                level=next_level, 
                price=current_node.price + item["price"],
                weight=current_node.weight + item["weight"],
                items_list=new_list
            )

            # Проверяем стала ли текущая стоимость выше рекордной
            if left_child.price > max_profit:
                max_profit = left_child.price
                best_items = left_child.items_list
                total_weight = left_child.weight
            
            # Считаем потенциал ветки БЕРЕМ
            left_child.bound = get_bound(left_child, n, w, items)
            
            # Если потенциал выше рекорда, то добавляем в очередь
            if left_child.bound > max_profit:
                heapq.heappush(queue, left_child)

        # Наследник НЕ берем предмет
        right_child = Node(
            level=next_level, 
            price=current_node.price,
            weight=current_node.weight,
            items_list=current_node.items_list
        )

        # Cчитаем потенциал ветки НЕ берем
        right_child.bound = get_bound(right_child, n, w, items)

        # Если потенциал выше рекорда, то добавляем в очередь
        if right_child.bound > max_profit:
            heapq.heappush(queue, right_child)
    return best_items, total_weight, max_profit
