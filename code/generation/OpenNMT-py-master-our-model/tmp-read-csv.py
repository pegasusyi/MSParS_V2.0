import pandas
import csv

# load dataset
dataframe = pandas.read_csv("../../../data/Tags-uh_subtlf_tagging___asr_resolution.csv",
                            quoting=csv.QUOTE_MINIMAL,
                            sep=',',
                            header=0)

dataset = dataframe.values
print(dataset)
for r in dataset:
    if r[0] == 'sub-TLF: Ask2Repeat':
        print(r[1])
