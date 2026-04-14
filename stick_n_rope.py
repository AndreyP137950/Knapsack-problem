def stick_n_rope(Lst, w):
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