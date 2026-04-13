import random

# Равномерное распределение от 0 до 1  
def uniform_distribution(n, x):
    weight_cost = []
    for i in range(n):
        weight_cost.append({"index":i, "weight": random.uniform(0, 1),
                             "price": items_cost(x)})  
    return weight_cost

# Нормальное распределение с математическим ожиданием 0.5 и стандартным отклонением 0.4
def normal_distribution(n, x):
    weight_cost = []
    mat_expectation = 0.5
    std_dev = 0.4
    while len(weight_cost) < n:
        weightN = random.gauss(mat_expectation, std_dev)
        if 0 < weightN < 1:
            weight_cost.append({"index": len(weight_cost),"weight": weightN,
                                 "price": items_cost(x)})
    return weight_cost

# Стоимость отдельного предмета
def items_cost(x):
    return random.uniform(1, x)