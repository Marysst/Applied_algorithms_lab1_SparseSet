import random
import time
import matplotlib.pyplot as plt

#Реалізація структури данних, що буде тестуватись
class SparseSet:
    def __init__(self, maxVal, capacity):
        self.maxVal = maxVal  # Максимальне значення елементу
        self.capacity = capacity  # Максимальна потужність множини
        self.n = 0 # Поточний розмір
        self.dense = [0] * capacity # Зберігає поточні елементи
        self.sparse = [0] * (maxVal + 1)  # Зберігає індекси елементів у масиві dense

    def __repr__(self):
        return f"SparseSet(n={self.n}, dense={self.dense}, sparse={self.sparse})"

    def search(self, x):
        if x>self.maxVal:
            return -1
        if self.sparse[x]<self.n and self.dense[self.sparse[x]]==x:
            return self.sparse[x]
        else:
            return -1
    
    def insert(self, x):
        if x>self.maxVal:
            return "error"
        if self.n>=self.capacity:
            return "error"
        if self.search(x)==-1:
            self.dense[self.n]=x
            self.sparse[x]=self.n
            self.n+=1

    def delete(self, x):
        if self.search(x)==-1:
            return "error"
        tmp=self.dense[self.n-1]
        self.dense[self.sparse[x]]=tmp
        self.sparse[tmp]=self.sparse[x]
        self.n-=1

    def clear(self):
        self.n=0
	
    # Time Complexity-O(n1+n2)
    def union(self, set2):
        # Capacity і maxVal результуючей множини
        unionCapacity = self.n + set2.n
        unionMaxVal = max(self.maxVal, set2.maxVal)

        # Ініціалізація порожньої множини для зберігання об'єднання
        union_set = SparseSet(unionMaxVal, unionCapacity)

	# Вставляємо всі елементи з першої множини в множину об'єднання
        for i in range(self.n):
            union_set.insert(self.dense[i]) # Операція insert містить в собі перевірку на наявність цього елемента в множині

        # Вставляємо всі елементи з другої множини в множину об'єднання
        for i in range(set2.n):
            union_set.insert(set2.dense[i]) # Операція insert містить в собі перевірку на наявність цього елемента в множині
    
        return union_set

    def intersection(self, set2):
        # Capacity і maxVal результуючей множини
        intersectionCapacity = min(self.n, set2.n)
        intersectionMaxVal = max(set2.maxVal, self.maxVal)

    	# Ініціалізація порожньої множини для зберігання перетину
        intersection_set = SparseSet(intersectionMaxVal, intersectionCapacity)

        # Шукаємо меншу з двох множин
    	# Якщо ця множина менша
        if self.n < set2.n:
    	    # Шукаємо кожен елемент цієї множини в set2
    	    # Якщо знайшли, додаємо його до множини перетину
            for i in range(self.n):
                 if set2.search(self.dense[i]) != -1:
                      intersection_set.insert(self.dense[i])
        else:   
	    # Шукаємо кожен елемент set2 у цій множині
	    # Якщо знайшли, додаємо його до множини перетину
             for i in range(set2.n):
                 if self.search(set2.dense[i]) != -1:
                      intersection_set.insert(set2.dense[i])
        return intersection_set
    
    def setDifferens(self, set2):
        # Capacity і maxVal результуючей множини
        setDifferensCapacity = self.n
        setDifferensMaxVal = self.maxVal

        # Ініціалізація порожньої множини для зберігання різниці
        setDifferens_set = SparseSet(setDifferensMaxVal, setDifferensCapacity)

    	# Шукаємо кожен елемент цієї множини в set2
    	# Якщо не знаходимо, додаємо його до результату
        for i in range(self.n):
             if set2.search(self.dense[i]) == -1:
                  setDifferens_set.insert(self.dense[i])
    
        return setDifferens_set

    def symDifferens(self, set2):
        # Capacity і maxVal результуючей множини
        symDifferensCapacity = self.n + set2.n
        symDifferensMaxVal = max(self.maxVal, set2.maxVal)

        # Ініціалізація порожньої множини для зберігання симетричной різниці
        symDifferens_set = SparseSet(symDifferensMaxVal, symDifferensCapacity)

    	# Шукаємо кожен елемент цієї множини в set2
    	# Якщо не знаходимо, додаємо його до результату
        for i in range(self.n):
             if set2.search(self.dense[i]) == -1:
                  symDifferens_set.insert(self.dense[i])

        # Шукаємо кожен елемент set2 у цій множині
        # Якщо не знаходимо, додаємо його до результату
        for i in range(set2.n):
             if self.search(set2.dense[i]) == -1:
                  symDifferens_set.insert(set2.dense[i])
    
        return symDifferens_set

    def isSubset(self, set2):
        # Якщо поточний розмір цієї множини більше за set2, вивід "no"
        if self.n > set2.n:
            return "no"
        
    	# Шукаємо кожен елемент цієї множини в set2
	# Якщо не знаходимо, вивід "no"
        for i in range(self.n):
             if set2.search(self.dense[i]) == -1:
                  return "no"
             
        return "yes"
    

# Функція для вимірювання часу операцій
def measure_time(func, *args):
    start_time = time.time()
    func(*args)
    finish_time = time.time()
    return finish_time - start_time

# Генерація випадкової множини
def generate_set(size, max_val):
    s = SparseSet(max_val, size)
    for _ in range(size):
        s.insert(random.randint(0, max_val))
    return s

# Функція для проведення одного експерименту
def perform_single_experiment(size, max_val):
    s1 = generate_set(size, max_val)
    s2 = generate_set(size, max_val)

    # Тест операції search для елемента, який є в множині
    random_element_in_set = s1.dense[random.randint(0, s1.n - 1)]
    search_time_in = measure_time(s1.search, random_element_in_set)

    # Тест операції search для елемента, якого немає в множині
    random_element_not_in_set = s1.dense[random.randint(0, s1.n - 1)]
    s1.delete(random_element_not_in_set)
    search_time_not_in = measure_time(s1.search, random_element_not_in_set)

    # Тест операції intersection
    intersection_time = measure_time(s1.intersection, s2)

    return (search_time_in, search_time_not_in, intersection_time)

# Функція для усереднення результатів експериментів
def average_experiment_results(size, max_val, num_experiments):
    total_search_in = 0
    total_search_not_in = 0
    total_intersection = 0

    for _ in range(num_experiments):
        results = perform_single_experiment(size, max_val)
        total_search_in += results[0]
        total_search_not_in += results[1]
        total_intersection += results[2]

    return (
        total_search_in / num_experiments,
        total_search_not_in / num_experiments,
        total_intersection / num_experiments
    )

# Функція для запуску експериментів
def run_experiments():
    sizes = [10000, 20000, 30000, 40000]  # Розміри множин
    max_val = 65536  # Максимальне значення елементів
    num_experiments = 1000  # Кількість експериментів

    search_times_in_set = []
    search_times_not_in_set = []
    intersection_times = []

    # Проходимо по кожному розміру множин
    for size in sizes:
        # Усереднюємо результати для кожного розміру
        averages = average_experiment_results(size, max_val, num_experiments)
        
        search_times_in_set.append(averages[0])
        search_times_not_in_set.append(averages[1])
        intersection_times.append(averages[2])

    # Побудова графіків
    plot_results(sizes, search_times_in_set, search_times_not_in_set, intersection_times)

# Побудова графіків
def plot_results(sizes, search_times_in_set, search_times_not_in_set, intersection_times):
    plt.figure(figsize=(12, 8))

    plt.subplot(1, 3, 1)
    plt.plot(sizes, search_times_in_set, label="Search (in set)")
    plt.xlabel("Розмір множини")
    plt.ylabel("Час виконання (с)")
    plt.title("Search (елемент є в множині)")
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(sizes, search_times_not_in_set, label="Search (not in set)")
    plt.xlabel("Розмір множини")
    plt.ylabel("Час виконання (с)")
    plt.title("Search (елементу немає в множині)")
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(sizes, intersection_times, label="Intersection")
    plt.xlabel("Розмір множини")
    plt.ylabel("Час виконання (с)")
    plt.title("Intersection")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Запуск експериментів
run_experiments()
