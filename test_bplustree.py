from unittest import TestCase
import random
from bplustree import BPlusTree


class TestBPlusTree(TestCase):
    def setUp(self) -> None:
        self.bplustree = BPlusTree()
        self.random_list = random.sample(range(1, 100), 20)
        for i in self.random_list:
            self.bplustree[i] = 'test' + str(i)
        random.shuffle(self.random_list)

    def test_query(self):
        for i in self.random_list:
            self.assertEqual(self.bplustree.query(i), 'test' + str(i))

    def test_change(self):
        self.assertTrue(self.bplustree.change(self.random_list[0], 'try'))
        self.assertEqual(self.bplustree.query(self.random_list[0]), 'try')

    def test_insert(self):
        self.bplustree.show()
        i = random.randint(1, 100)
        print('Insert ' + str(i))
        self.bplustree[i] = 'test' + str(i)
        self.bplustree.show()

    def test_delete(self):
        print(self.random_list)
        for i in self.random_list:
            print('Delete ' + str(i))
            self.bplustree.delete(i)
            self.bplustree.show()


def demo_bplustree():
    print('Initializing B+ tree...')
    bplustree = BPlusTree()

    print('\nB+ tree with 1 item...')
    bplustree.insert('a', 'alpha')
    bplustree.show()

    print('\nB+ tree with 2 items...')
    bplustree.insert('b', 'bravo')
    bplustree.show()

    print('\nB+ tree with 3 items...')
    bplustree.insert('c', 'charlie')
    bplustree.show()

    print('\nB+ tree with 4 items...')
    bplustree.insert('d', 'delta')
    bplustree.show()

    print('\nB+ tree with 5 items...')
    bplustree.insert('e', 'echo')
    bplustree.show()

    for i in range(20):
        print('\nB+ tree with ' + str(i + 5) + ' items...')
        bplustree.insert(str(i), 'foxtrot' + str(i))
        bplustree.show()

    print('\nRetrieving values with key e...')
    print(bplustree.query('e'))


def demo():
    bplustree = BPlusTree()
    print('read file ./partfile.txt')
    keys = []
    with open("partfile.txt", 'rb') as reader:
        bplustree.readfile(reader)

    with open("partfile.txt", 'r') as reader:
        for line in reader:
            s = line.split(maxsplit=1)
            keys += [s[0]]

    for i in range(len(keys)):
        bplustree.delete(keys[i])
        if i % 1000 == 0:
            print('Delete ' + keys[i] + ' item')


if __name__ == '__main__':
    TestBPlusTree()
