import os

import numpy as np

FEAT_SEP = u'￨'


def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read().split('\n')
    return data


def load_txt(filename):
    raw_dataset = []

    if type(filename) is list:
        for f in filename:
            if f:
                print(f)
                raw_dataset.extend(load_file(f))
    elif type(filename) is str:
        print(filename)
        raw_dataset = load_file(filename)
    else:
        raise ValueError('filename must be in str or list')
    return raw_dataset


def print_input_along_feature(input, feature):
    concated = np.concatenate((np.expand_dims(input, axis=0), np.array(feature.tolist())), axis=0).T
    result = []
    for concated_token in concated:
        result.append(FEAT_SEP.join(concated_token))
    return ' '.join(result)
