import json

def readfile(filename):
    f = open(filename, encoding='utf-8')
    f = json.load(f)
    com = f['comment']
    fun = f['function']
    keys = com.keys()
    sortedkeys = sorted(map(int, com.keys()))
    assert sortedkeys == list(range(len(keys)))
    return [(com[k], fun[k]) for k in keys]
