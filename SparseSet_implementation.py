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
