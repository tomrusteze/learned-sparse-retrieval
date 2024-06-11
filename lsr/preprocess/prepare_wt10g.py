from tqdm import tqdm
from pathlib import Path
from lsr.utils.parsewt10g import read_wt10g_dataset

print("Preparing WT10g datasets")
wt10g_dir = Path("data/WT10g/collection-formatted/")
dataset = read_wt10g_dataset("data/WT10g/collection/")

if not wt10g_dir.is_dir():
    wt10g_dir.mkdir(parents=True, exist_ok=True)
collection_path = wt10g_dir/"collection.tsv"
with open(collection_path, "w", encoding="UTF-8") as f:
    for id, text in tqdm(dataset.items()):
        text = text.replace("\n", " ").replace("\t", " ")
        f.write(f"{id}\t{text}\n")