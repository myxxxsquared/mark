
import re

re_line_topic = re.compile(r'Topic #([\d]+), freq=([\d\.]+), words: (.+)')

def splititems(it):
    lines = []

    # 0: waiting
    # 1: after "================"
    # 2: reading
    status = 0

    while True:
        try:
            line = next(it)
        except StopIteration:
            if lines:
                yield lines
            break

        line = line.strip()

        if line == "===========================================":
            if status == 2:
                status = 0
                if lines:
                    yield lines
                    lines = []
            status = 1
        else:
            if status == 1:
                if line.startswith("uid: "):
                    status = 2
                else:
                    status = 0
            if status == 2:
                lines.append(line)
    

def readitem(it):
    re_line_topic_local = re_line_topic

    for item in splititems(it):
        assert item[0].startswith('uid: ') and len(item[0]) == 41
        uid = item[0][5:-1]

        itemlen = len(item)

        assert itemlen == 6 or itemlen == 9 or itemlen == 12

        match = re_line_topic_local.match(item[1])
        assert match
        freq = float(match.group(2))
        words = match.group(3)

        assert item[2].startswith("last phrase:")

        assert item[3].startswith("Similarlity = ")
        title1 = item[4]
        detail1 = item[5]

        if itemlen > 6:
            assert item[6].startswith("Similarlity = ")
        title2 = item[7] if itemlen > 7 else ""
        detail2 = item[8] if itemlen > 8 else ""

        if itemlen > 9:
            assert item[9].startswith("Similarlity = ")
        title3 = item[10] if itemlen > 10 else ""
        detail3 = item[11] if itemlen > 11 else ""

        yield uid, freq, words, title1, detail1, title2, detail2, title3, detail3

def readfile(filename):
    f = open(filename)
    f = iter(f)
    return readitem(f)


