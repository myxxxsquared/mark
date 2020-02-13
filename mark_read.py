
import re

re_line_uid = re.compile(r'uid: ([a-f0-9\-]+)' + '\n')
re_line_topic = re.compile(r'Topic #([\d]+), freq=([\d\.]+), words: (.+)' + '\n')

def readitem(iter):

    line = next(iter)
    assert line == '===========================================\n'

    line = next(iter)
    if line == '\n':
        return None
    assert line.startswith('uid: ') and line.endswith('\n')
    uid = line[5:-1]

    line = next(iter)
    match = re_line_topic.match(line)
    assert match
    freq = float(match.group(2))
    words = match.group(3)

    line = next(iter)

    line = next(iter)
    line = next(iter)
    title1 = line.strip()
    line = next(iter)
    detail1 = line.strip()

    line = next(iter)
    line = next(iter)
    title2 = line.strip()
    line = next(iter)
    detail2 = line.strip()

    line = next(iter)
    line = next(iter)
    title3 = line.strip()
    line = next(iter)
    detail3 = line.strip()

    return uid, freq, words, title1, detail1, title2, detail2, title3, detail3

def readfile(filename):
    f = open(filename)
    f = iter(f)

    while True:
        item = readitem(f)
        if not item:
            break
        yield item


