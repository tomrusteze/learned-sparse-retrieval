import os
import re
import gzip
from collections import defaultdict
import html
from tqdm import tqdm

def read_wt10g_dataset(directory: str) -> dict:
    data = {}

    # Regex pattern to match document IDs
    doc_id_pattern = re.compile(r'<DOCNO>(.*?)</DOCNO>', re.DOTALL)
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    unwanted_pattern = re.compile(r'<!--.*?-->|<[^>]*>')
    
    # Traverse each file in the directory
    for root, _, files in tqdm(os.walk(directory), desc=f"Reading data from {directory}"):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                # Split content into individual documents
                documents = content.split('<DOC>')
                for doc in documents:
                    # Extract document ID using regex
                    doc_id_match = re.search(doc_id_pattern, doc)
                    if doc_id_match:
                        doc_id = doc_id_match.group(1).strip()
                        # Remove HTML tags and extra spaces
                        text = doc.split('</DOCHDR>')[-1].strip()
                        text = html.unescape(text)
                        text = re.sub(unwanted_pattern, '', text)
                        text = re.sub(r'<.*?>', '', text)
                        text = re.sub(url_pattern, '', text)
                        text = re.sub(r'\s+', ' ', text).strip()
                        if text:
                            data[doc_id] = text
    return data

# Example usage:
if __name__ == "__main__":
    wt10g_directory = 'data/WT10gmini/'
    dataset_dict = read_wt10g_dataset(wt10g_directory)
    print(len(dataset_dict))
