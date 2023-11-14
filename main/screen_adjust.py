import json
from settings import Settings

# 修改JSON中的数据
def multiply_values(data, multiplier):
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], (dict, list)):
                multiply_values(data[key], multiplier)
            elif isinstance(data[key], (int, float)):
                data[key] *= multiplier
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], (dict, list)):
                multiply_values(data[i], multiplier)
            elif isinstance(data[i], (int, float)):
                data[i] *= multiplier

def screen_adjust():
    # 读取JSON文件
    with open('json/surface_2.json', 'r') as f:
        data = json.load(f)

    # 将JSON中的数据乘以1.5
    multiply_values(data,Settings().RATIO_ALL)

    # 写入新的JSON文件
    with open('json/surface_3.json', 'w') as f:
        json.dump(data, f, indent=4)




    with open('json/surface_point.json', 'r') as f:
        data = json.load(f)

# 将每个列表中的每个元素乘以1.5
    for key in data:
        data[key] = [x * Settings().RATIO_ALL for x in data[key]]

# 写入新的JSON文件
    with open('json/surface_point_3.json', 'w') as f:
        json.dump(data, f, indent=4)





    with open('json/surface_point_player.json', 'r') as f:
        data = json.load(f)

# 将每个列表中的每个元素乘以1.5
    for key in data:
        data[key] = [x * Settings().RATIO_ALL for x in data[key]]

# 写入新的JSON文件
    with open('json/surface_point_player_3.json', 'w') as f:
        json.dump(data, f, indent=4)





    with open('json/number_2.json', 'r') as f:
        data = json.load(f)

# 将每个列表中的每个元素乘以1.5

    multiply_values(data,Settings().RATIO_ALL)
  

# 写入新的JSON文件
    with open('json/number_3.json', 'w') as f:
        json.dump(data, f, indent=4)