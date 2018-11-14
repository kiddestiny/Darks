import pan
import random
from faker import Faker


class DataGenerator():
    def __init__(self):
        pass
    
    def gen_d_json(self):
        f = Faker('zh_CN')
        add = f.address()
        print('gen.. d json '+add)
        pass

    def gen_lines_json(self):
        print('gen.. lines json')
        pass



if __name__ == '__main__':
    o = DataGenerator()
    o.gen_d_json()
    o.gen_lines_json()
