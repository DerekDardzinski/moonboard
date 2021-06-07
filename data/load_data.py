import numpy as np
import pandas as pd
import json

grade_conv = {
    '6A': 3,
    '6A+': 3,
    '6B': 4,
    '6B+': 4,
    '6C': 5,
    '6C+': 5,
    '7A': 6,
    '7A+': 7,
    '7B': 8,
    '7B+': 8,
    '7C': 9,
    '7C+': 10,
    '8A': 11,
    '8A+': 12,
    '8B': 13,
    '8B+': 14,
    '8C': 15,
}

def get_hold_matrix(moves):
    hold_matrix = np.zeros((18, 11))
    hold_inds = np.array(
        [[int(m[1:]) - 1, ord(m[0].lower()) - 97] for m in moves]
    )
    hold_matrix[hold_inds[:,0], hold_inds[:,1]] = 1

    return hold_matrix
    

with open('./2017.json', 'r') as f:
    data = json.load(f)

for i, d in enumerate(data):
    data[i]['Grade'] = grade_conv[d['Grade']]

with open('./2017_new.json', 'w') as f:
    new_data = json.dumps(data)
    f.write(new_data)

df = pd.read_json('./2017_new.json')
print(df.groupby('Grade').size())
