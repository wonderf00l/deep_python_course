import unittest
from hw5_LRUCache import LRUCache


class MyTestCase(unittest.TestCase):
    def test_cache(self):
        inst = LRUCache(3)
        inst['k1'] = 'val1'
        self.assertEqual(inst.cache, {'k1': 'val1'})
        inst['k2'] = 'val2'
        inst['k3'] = 'val3'
        val_1 = inst['k2']
        self.assertEqual(list(inst.cache.keys()), ['k1', 'k3', 'k2'])
        inst[2] = True
        self.assertEqual(list(inst.cache.keys()), ['k3', 'k2', 2])
        inst[2] = 'smth'
        self.assertEqual(list(inst.cache.keys()), ['k3', 'k2', 2])
        val_2 = inst['k3']
        self.assertEqual(list(inst.cache.keys()), ['k2', 2, 'k3'])
        
    def test_cache_edited(self):
        inst = LRUCache(1)
        inst["k1"] = "val1"
        inst["k2"] = "val2"
        self.assertEqual([inst["k1"], inst["k2"]], [None, "val2"])

        inst_1 = LRUCache(3)
        inst_1[1] = '1'
        inst_1[2] = '2'
        inst_1[3] = '3'
        inst_1[1] = "new_val"
        inst_1[4] = '4'
        self.assertEqual(inst_1[2], None)


if __name__ == '__main__':
    unittest.main()
