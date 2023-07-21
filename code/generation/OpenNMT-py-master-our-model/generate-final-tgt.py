import re
import sys

if __name__ == "__main__":
    src_path = sys.argv[1]
    tgt_path = sys.argv[2]

    with open(src_path, 'r') as src, open(tgt_path, 'r') as tgt:
        for line1, line2 in zip(src, tgt):
            try:
                matches = re.findall('<TSP> (.+?) <TSP> (.+?)$', line2)
                if len(matches[0]) != 2:
                    continue
                line2 = re.sub("<e>", matches[0][0], line2, 1)
                line2 = re.sub("<e>", matches[0][1], line2, 1)
                line2 = re.sub(' <TSP>.*', '', line2)
                line1 = re.sub(' <SP>.*', f' <SP> {line2}', line1)
                print(line1.strip())
            except IndexError as e:
                pass
