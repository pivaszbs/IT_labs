import numpy as np
from typing import List
import os

def encode(s):
    buffer = ''
    phrases = {}
    ans = []
    for i in range(len(s)):
        c = chr(s[i])
        if phrases.get(buffer + c) != None:
            buffer += c
        else:
            key = phrases.get(buffer)
            if key == None:
                key = 0
            ans.append((key, c))
            phrases[buffer + c] = len(phrases) + 1
            buffer = ''
    return ans

def left(n):
    def leftLen(n):
        if (n == 0):
            return 1
        else:
            return np.ceil(np.log2(n))
    
    s = "{0:b}".format(n)

    while (len(s) < leftLen(n)):
        s = '0' + s

    return s

def encodeInBinary(encoded):
    ans = ''
    s = ''
    for node in encoded:
        right = str("{0:b}".format(ord(node[1])))
        # right = '0' if node[1] == 'a' else '1'
        s += left(node[0]) + right  + ''
    return s

def decodeFromBinary(s):
    a = s.strip().split(' ')
    ans = []
    for node in a:
        right = chr(int(node[-7:], 2))
        left = int(node[:-7], 2)
        ans.append((left, right))
    return decode(ans)   

def decode(encoded):
    phrases = ['']
    ans = ""
    for node in encoded:
        key = phrases[node[0]]
        if not key:
            key = ''
        word = key + node[1]
        ans += word
        phrases.append(word)
    return ans

def compress_file(filename: str) -> List[tuple]:
    """
    Calculate the entropy of the file
    :param filename: name of file
    :return:
    """
    with open(filename, "rb") as f:
        return encodeInBinary(encode(f.read()))   

def compressed_filename(save_prefix, delim, path):
    ans = save_prefix + delim + path
    dotidx = ans.rfind('.')
    return ans[:dotidx] + 'Compressed' + ans[dotidx:]

def compress_files(file_names: List[str], prefix: str, save_prefix: str):
    """
    :param file_names:
    :return:
    """
    delim = '/'
    for path in file_names:
        filename = prefix + delim + path
        s = compress_file(filename)
        f = open(compressed_filename(save_prefix, delim, path), 'wb')
        f.write(bytes(int(s[i : i + 8], 2) for i in range(0, len(s), 8)))

def decompress_file(filename: str) -> List[tuple]:
    """
    Calculate the entropy of the file
    :param filename: name of file
    :return:
    """
    with open(filename, "rb") as f:
        return decodeFromBinary(decode(f.read()))   

def decompress_files(file_names: List[str], prefix: str):
    """
    :param file_names:
    :return:
    """

    def decompressed_filename(prefix, delim, path):
        ans = prefix + delim + path
        dotidx = ans.rfind('.')
        return ans[:dotidx] + 'Decompressed' + ans[dotidx:]

    delim = '/'
    for path in file_names:
        filename = prefix + delim + path
        s = decompress_file(compressed_filename(prefix, delim, path))
        f = open(decompressed_filename(prefix, delim, path), 'wb')
        f.write(bytes(int(s[i : i + 8], 2) for i in range(0, len(s), 8)))


if __name__ == '__main__':
    dir = './dataset'
    compressDir = './AntonKrylovOutputs'
    dirs = os.listdir(dir)
    delim = '/'
    for d in dirs:
        path = dir + delim + d
        save_path = compressDir + delim + d
        files = os.listdir(path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # compress_files(files, path, save_path)
        decompress_files(files, save_path)
        