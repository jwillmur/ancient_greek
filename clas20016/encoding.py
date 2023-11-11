a = [913, 945, 8048, 8049]
a.extend([*range(7936,7952)])
a.extend([*range(8064,8080)])
a.extend([*range(8112,8125)])
e = [917, 949, 8050, 8051, 8136, 8137]
e.extend([*range(7952,7966)])
h = [919, 951, 8052, 8053]
h.extend([*range(7968,7984)])
h.extend([*range(8080,8096)])
h.extend([*range(8130,8136)])
h.extend([*range(8138,8141)])
i = [921, 953, 8054, 8055]
i.extend([*range(7984,8000)])
i.extend([*range(8144,8156)])
o = [927, 959, 8056, 8057, 8184, 8185]
o.extend([*range(8000,8014)])
u = [933, 965, 8058, 8059]
u.extend([*range(8016,8032)])
u.extend([*range(8160,8164)])
u.extend([*range(8166,8172)])
w = [937, 969, 8060, 8061, 8186, 8197, 8188]
w.extend([*range(8032,8048)])
w.extend([*range(8096,8112)])
w.extend([*range(8178,8184)])

dictionary = {'a': a,\
    'b': [914, 946],\
    'g': [915, 947],\
    'd': [916, 948],\
    'e': e,\
    'z': [918, 950],\
    'h': h,\
    'q': [920, 952],\
    'i': i,\
    'k': [922, 954],\
    'l': [923, 955],\
    'm': [924, 956],\
    'n': [925, 957],\
    'c': [926, 958],\
    'o': o,\
    'p': [928, 960],\
    'r': [929, 961, 8164, 8165, 8172],\
    's': [931, 962, 963],\
    't': [932, 964],\
    'u': u,\
    'f': [934, 966],\
    'x': [935, 967],\
    'y': [936, 968],\
    'w': w\
}

def decode(word):
    uncoded = []
    for letter in word:
        for key in dictionary.keys():
            if ord(letter) in dictionary[key]:
                uncoded.append(key)
    return ''.join(uncoded)
