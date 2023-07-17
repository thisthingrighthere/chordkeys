import pandas as pd
import json
import collections

csv_path = "../chordkeys/corpus/all-the-news-2-1.csv"

def chr_freq(column):
    freq_json["chr_freq"].update(column.lower())

freq_json = {}
freq_json["chr_freq"] = collections.Counter()

i = 1
while i <= 5:
    print("\nLoading block", i)
    try:
        df = pd.read_csv(csv_path, header=0, skiprows=[1,10000*i-10000+1], nrows=10000*i, usecols=["title", "article"])
    except Exception as e:
        print(e)
        break

    print("\nGetting frequencies.\n")
    df['text'] = df['title'] + '\n\n' + df['article']

    del df['title']
    del df['article']

    df['text'].dropna(inplace=True)
    df['text'] = df['text'].astype(str)

    df.apply(lambda x: chr_freq(x['text']), axis=1)

    sorted_chr = [x[0] for x in list(sorted(freq_json["chr_freq"].items(), key=lambda x:x[1],reverse=True))]
    print(sorted_chr[:30])

    i += 1

print("\nSaving.")
with open("freq.json", "w", encoding="utf8") as f:
    json.dump(freq_json, f)