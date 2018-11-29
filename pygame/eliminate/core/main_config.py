import json
import os
from os.path import abspath, dirname


def read_json(file_name):
    with open(file_name) as file:
        return json.load(file)


class MainConfig:
    def __init__(self):
        path = dirname(abspath(__file__))
        json_path = os.path.dirname(path)

        self.monsters = read_json(json_path + "/json/monster.json")
        self.grids = read_json(json_path + "/json/grid.json")

    # 格式化输出盘的配置
    def string(self):
        for grids in self.grids:
            print('id =', grids['id'])
            for i in range(int(grids['row'])):
                for j in range(int(grids['col'])):
                    print(grids['data'][j + i * j], end=' ')
                print()
            print()
