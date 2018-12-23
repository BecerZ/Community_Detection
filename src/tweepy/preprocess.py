import pickle
import os
import json

data_path = './data_v2/'
output_path = './processed_v2/'
# data_path = './a/'
# output_path = './a/'


def save_data(filename, data):
    output = open(filename, 'wb')
    pickle.dump(data, output)
    output.close()


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


def preprocess(filename):
    file = open('{0}{1}'.format(data_path, filename), 'rb')
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
    f = open('{0}{1}.txt'.format(output_path, os.path.splitext(filename)[0]), 'w+')

    f.write('#{0} {1} {2}\n'.format(id, edge_count, edge_count > ((id ** 2) * 80) / 100))
    for key, value in processed_data.items():
        if not value:
            continue
        for edge in value:
            f.write('{} {}\n'.format(key, edge))
    # print(id_look_up)

    f.close()

# z = set()
# z.add(6)
# z.add(7)
# z.add(8)
#
# t = set()
#
# t.add(6)
# a = {5: z, 9: t}
# save_data('{0}9.pkl'.format(data_path), a)

count = 1
files = os.listdir(data_path)
for file in files:
    if not os.path.isfile('{0}{1}.txt'.format(output_path, os.path.splitext(file)[0])):
        preprocess(file)
    print('{0} of {1} done'.format(count, len(files)))
    count += 1
