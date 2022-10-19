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


if __name__ == '__main__':
    unittest.main()
