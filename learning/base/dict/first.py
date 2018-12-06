import json
# import MySQLdb

names = {}
alien = {'color': 'green', 'age': '23', 'hobi': ['d', 'f']}
print(alien)


def hi(name, *names, age=0,**s):
    print(name, age)
    for n in names:
        print(n)
    for ss, d in s.items():
        print(ss, d)


hi('d', 23, 34, 45, d=6, sdsd=89)
files = 'test.json'
with open(files, 'w') as o:
    json.dump(alien, o)

# conn = MySQLdb.connect('localhost', 'root', 'mysql1104', 'test', 3306)
# print(conn)