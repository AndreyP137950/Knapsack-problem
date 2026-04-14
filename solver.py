# Жадный алгоритм
def greedy_algo(Lst, w):
    # Создаем список с соотношением цена/вес
    grLst = Lst.copy()
    ###grLst = [{"index": item["index"], "multiwp": item["price"]/item["weight"]} for item in Lst]
    
    # Сортировка по цене/весу (убывание)
    grLst.sort(key=lambda x: x["price"]/x["weight"], reverse=True)
    ###grLst.sort(key=lambda x: x["multiwp"], reverse=True)
    rLst = []
    v = cost = 0
    for item in grLst:
        if item["weight"] <= w-v: #проверка, что вес элемента <= остав. объема
            rLst.append(item)
            v += item["weight"]
            cost += item["price"]
    return rLst, v, cost
    '''
    for item in grLst:
        if Lst[item["index"]]["weight"] <= w-v: #проверка, что вес элемента <= остав. объема
            rLst.append(Lst[item["index"]])
            v += Lst[item["index"]]["weight"]
            cost += Lst[item["index"]]["price"]
    return rLst, v, cost'''

# Метод ветвей и границ
def branch_boundary_method(Lst, w):
    # Подготовка массива к использованию
    cLst = Lst.copy()
    
    # список в который посчитаем отношение цена/вес
    cooked_list = []

    # здесь его и считаем
    for item in cLst:
        ratio = float("inf") if item["weight"] == 0 else item["price"] / item["weight"]
        cooked_list.append((item, ratio)) # на выход список кортежей (элемент, отношение цена/вес)
    
    # отсортировали по убыванию отношения цена/вес
    cooked_list.sort(key=lambda x: x[1], reverse=True)
    
    rLts = []
    v = cost = 0
    

    return rLts, v, cost