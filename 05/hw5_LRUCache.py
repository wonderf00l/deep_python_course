class LRUCache:

    def __init__(self, limit=4):
        self.cache = {}
        self.capacity = limit

    def __getitem__(self, item):
        self.cache[item] = self.cache.pop(item)
        return self.cache[item]

    def __setitem__(self, key, value):
        if len(self.cache) >= self.capacity and key not in self.cache:
            self.cache.pop(list(self.cache.keys())[0])
        self.cache[key] = value

    def __str__(self):
        return str(self.cache)


inst = LRUCache()
inst['k1'] = 'val1'
inst['k2'] = 'val2'
inst['k3'] = 'val3'
a = inst['k2']
print(inst)
inst['k4'] = 'val4'
print(inst)
b = inst['k1']
print(inst)
inst['k5'] = 'val5'
print(inst)
inst['k5'] = 'val5'
print(inst)
inst['k6'] = 'val5'
print(inst)
c = inst['k4']
print(inst)
