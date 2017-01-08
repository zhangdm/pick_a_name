# coding=utf-8
"""
@ author: cer
数据预处理
"""
import numpy as np
import os
import cPickle as pickle


def load_training_data():
    """从pkl加载训练数据，无则通过语料生成"""
    unknown_token = "UNKNOWN_TOKEN"
    name_start_token = "NAME_START"
    name_end_token = "NAME_END"

    # 尝试加载pkl
    train_pkl_name = "training_data/train.pkl"
    if os.path.exists(train_pkl_name):
        with open(train_pkl_name, 'rb') as f:
            return pickle.load(f)

    # 读取原始语料文件
    print "Reading PKL Files ..."
    raw_pkl_name = "data/detail_data.pkl"
    with open(raw_pkl_name, 'rb') as f:
        data = pickle.load(f)
    names = []
    chars = set()
    for datum in data:
        names += [[name_start_token] + list(x) + [name_end_token] for x in datum["names"]]
        for name in datum["names"]:
            for one in name:
                chars.add(one)
    print "Parsed %d names." % (len(names))
    # generate char_to_index and index_to_char
    char_to_index = {name_start_token: 0, name_end_token: 1}
    i = 2
    for char in chars:
        char_to_index[char] = i
        i += 1
    index_to_char = dict([(char_to_index[c], c) for c in char_to_index])

    # Create the training data
    X_train = np.asarray([[char_to_index[c] for c in name[:-1]] for name in names])
    y_train = np.asarray([[char_to_index[c] for c in name[1:]] for name in names])

    # 保存到pkl
    all = [X_train, y_train, char_to_index, index_to_char]
    with open(train_pkl_name, "wb") as f:
        pickle.dump(all, f)
    return all


def load_bin_vec(fname, vocab):
    """
    Loads 400x1 word vecs from Google (Mikolov) word2vec
    从GoogleNews-vectors-negative300.bin中加载w2v矩阵。生成w2v。w2v是一个dict，key是word，value是vector。
    """
    word_vecs = {}
    with open(fname, "rb") as f:
        header = f.readline()
        # vocab_size是word的个数, layer1_size是word2vec的维度
        vocab_size, layer1_size = map(int, header.split())
        # binary_len是word2vec的字节数
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in xrange(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    word.append(ch)
            # 只读取数据集中出现的word的word2vec
            if word in vocab:
                word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')
            else:
                f.read(binary_len)
    return word_vecs


def print_train_example():
    """查看部分训练数据"""
    X_train, y_train, char_to_index, index_to_char = load_training_data()
    x_example, y_example = X_train[17], y_train[17]
    print
    print "x:\n%s\n%s" % (" ".join([index_to_char[x] for x in x_example]), x_example)
    print "\ny:\n%s\n%s" % (" ".join([index_to_char[y] for y in y_example]), y_example)

if __name__ == '__main__':
    print_train_example()