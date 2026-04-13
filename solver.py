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
    return 0