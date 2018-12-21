import pickle


def find_index(data, value, index):
    if not data:
        return index
    mid_index = int((len(data) - 1) / 2)
    if value >= data[mid_index]:
        return find_index(data[mid_index + 1:], value, index + mid_index + 1)
    else:
        return find_index(data[:mid_index], value, index)


def insert_sorted_list(data, value):
    index = find_index(data, value, 0)
    data[index:index] = [value]
    pass


file = open('data.pkl', 'rb')
data = pickle.load(file)
file.close()

id_look_up = {}
processed_data = {}
edge_count = 0
id = 1
for x, y in data.items():
    already_exists = True
    if x in id_look_up:
        key = id_look_up[x]
    else:
        key = id
        id_look_up[x] = key
        id += 1
        already_exists = False
    value = []
    if key == 8:
        pass
    for edge in y:
        if edge in id_look_up:
            if already_exists and id_look_up[edge] in processed_data and key in processed_data[id_look_up[edge]]:
                continue
            insert_sorted_list(value, id_look_up[edge])
            edge_count += 1
        else:
            insert_sorted_list(value, id)
            edge_count += 1
            id_look_up[edge] = id
            id += 1
    processed_data[key] = value
f = open('data.txt', 'w+')

f.write('{0} {1} {2}\n'.format(id, edge_count, edge_count > (id * 80) / 100))
for key, value in processed_data.items():
    f.write('{} {}\n'.format(key, ' '.join(str(i) for i in value)))
