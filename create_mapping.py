import json
from itertools import combinations
import unicodedata

key_priority = [
                "fjdksla;",
                #"fjdksla;'tyruieowpq"
                #"fjdksla;'#]bnvmc,x.z/" + "\\"
                ]

remove = []
key_map = {}
other_maps = {}

print("Creating character order list.")
with open("freq.json", encoding="utf8") as f:
    freq = json.load(f)["chr_freq"]

ch_order = [x[0] for x in list(sorted(freq.items(), key=lambda x:x[1],reverse=True))]

print("Removing unwanted characters.")
# Remove accented characters (will add a mapping for these later)
#accented_table = []
with open('accents.txt', newline='\n', encoding="utf8") as f:
    text = [l.replace("\n", "").replace("\r", "") for l in f.readlines()][1:]

    #for l in text[1:]:
    #    accented_table.append(l.split(","))

    for row in text:
        remove += [c for c in row.split(",")[1:] if c and c != " "]


with open('chr_settings.txt', newline='\n', encoding="utf8") as f:
    text = [l.replace("\n","").replace("\r","") for l in f.readlines()]

    # Remove characters
    i = text.index("### remove ###") + 1
    j = i + 1
    while j < len(text):
        if "###" in text[j]:
            break
        else:
            j += 1

    for l in text[i:j]:
        l = l.split("#")[0].strip()

        if not l:
            continue

        if "-" in l:
            a = int(l.split("-")[0].strip(), 16)
            b = int(l.split("-")[1].strip(), 16)

            while a <= b:
                remove.append(chr(a))
                a += 1
        elif l:
            remove.append(chr(int(l, 16)))

    # Create custom maps

    i = text.index("### custom maps ###") + 1
    j = i + 1
    while j < len(text):
        if "###" in text[j]:
            break
        else:
            j += 1

    for l in text[i:j]:
        l = l.split("#")[0]

        if l:
            if ":" not in l:
                print("Bad line")
                continue

            m, k = l.split(":")

            m = "".join(sorted(m.strip()))

            k = k.strip()

            if k == "hsh":
                k = "#"
            elif k == "cur":
                k = "$"
            elif k == "cln":
                k = ":"

            # Add custom mappings to key map
            key_map[m] = k

            if k in ch_order:
                ch_order.remove(k)

# Add numbers to remove
remove += list("1234567890")

# Remove characters in remove
for c in remove:
    assert len(c) == 1

    if c in ch_order:
        ch_order.remove(c)
    else:
        pass
        #print(f">{c}<", ord(c))


print("Making combinations.")

# List combinations
combination_priority = []
end = False
for chrs in key_priority:
    for i in range(1, len(chrs)+1):
        for combo in combinations(chrs, i):
            combo = "".join(sorted(combo))
            # Prevent keyboard keys, duplicates and already assigned keys from being added
            if len(combo) > 1 and combo not in combination_priority and combo not in key_map:
                combination_priority.append(combo)

            if len(combination_priority) >= 1000:
                #print(combination_priority[-10:])
                end = True
                break
        if end:
            break
    if end:
        break

combination_priority = ["".join(sorted(x)) for x in combination_priority]


# Make initial key map
key_map.update(zip(combination_priority, ch_order[:len(combination_priority)]))


# Save key map
with open("key_map.json", "w", encoding="utf8") as f:
    json.dump(key_map, f)

print()

# Print map as table
print_items = list(key_map.items())
i = 0
w = 4
row_s = ""
table_str = ""
while i < len(print_items) and i < 150:
    element_str = ' {:5}: {:^5} |'.format(*print_items[i])

    if element_str not in table_str:
        row_s += element_str

    if i%w == w-1:
        table_str += row_s + "\n"
        row_s = ""

    i += 1

print(table_str)

#print(hex(ord("₺")))
#print(unicodedata.name("₺"))