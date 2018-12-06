import json

file_name='test.json'
def write_json():
    global file_name

    person = {'color': 'green', 'age': '23'}
    with open(file_name, 'w') as o:
        json.dump(person, o)

def read_json():
    global file_name
    with open(file_name) as file:
        datas = json.load(file)
        for data in datas :
            print(data, datas[data])

write_json()
read_json()