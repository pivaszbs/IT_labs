import numpy as np
from typing import List
import os
import struct

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
    if n == 0:
        return '10000000'
    s = ''
    flag = True
    while n > 0:
        s = '{:7b}'.format(n & 0b01111111) + s
        if flag:
            s = '1' + s
            flag = False
        else:
            s = '0' + s
        n >>= 7
    s = s.replace(' ', '0')
    return s

def encodeInBinary(encoded):
    ans = ''
    s = ''
    for node in encoded:
        right = str("{:8b}".format(ord(node[1]))).replace(' ', '0')
        s += left(node[0]) + right 
    return s

def decodeFromBinary(s):
    a = bytearray(s)
    i = 0
    j = 0
    left = 0
    ans = []
    next_char = False
    while i < len(a):
        if next_char:
            right = chr(a[i])
            ans.append((left, right))
            next_char = False
            left = 0
            j = 0
        elif a[i] & 128 == 128:
            while j >= 0:
                left += (a[i - j] & 127) << (j * 7)
                j -= 1
            j = 0
            next_char = True
        else:
            j+=1
        
        i+=1
    return decode(ans)

def decode(encoded):
    phrases = ['']
    ans = ""
    for node in encoded:
        if node[0] >= len(phrases):
            key = ''
        else:
            key = phrases[node[0]]
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

def decompressed_filename(prefix, delim, path):
    ans = prefix + delim + path
    dotidx = ans.rfind('.')
    return ans[:dotidx] + 'Decompressed' + ans[dotidx:]

def decompress_file(filename: str) -> List[tuple]:
    """
    :param filename: name of file
    :return:
    """
    with open(filename, "rb") as f:
        return decodeFromBinary(f.read())

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
        b = bytearray()
        b.extend(map(ord, s))
        f.write(b)


if __name__ == '__main__':
    dir = './dataset'
    compressDir = './AntonKrylovOutputs'
    dirs = os.listdir(dir)
    delim = '/'
    for d in dirs:
        if d == 'jpg':
            continue
        path = dir + delim + d
        save_path = compressDir + delim + d
        files = os.listdir(path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        compress_files(files, path, save_path)
        decompress_files(files, save_path)
