# %%
import json
import os
import time
import random
import pandas as pd
import urllib.request
import urllib.error
import http.client
from bs4 import BeautifulSoup
from tqdm import tqdm

json_file = "links.json"

with open(json_file, "r") as f:
    links_json = json.load(f)

category = 'Supreme Court of India'
category_links = links_json[category]
print(f"Started file ... {json_file} with {len(category_links)} docs\n\n")

df = pd.DataFrame(category_links, columns=["url"])
df.reset_index(inplace=True)
df.columns = ["doc_id", "url"]
df["status"] = "pending"

def scrape_and_save(df_batch, start_index):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for idx, row in tqdm(df_batch.iterrows(), total=len(df_batch)):
        doc_id = row["doc_id"]
        BASE_URL = row["url"]

        success = False
        retries = 3
        for attempt in range(retries):
            try:
                req = urllib.request.Request(BASE_URL, headers=headers)
                response = urllib.request.urlopen(req)
                html = response.read()
                break  # Success
            except (urllib.error.HTTPError, urllib.error.URLError, http.client.IncompleteRead) as e:
                print(f"[Retry {attempt+1}] Error at doc {doc_id}: {e}")
                time.sleep(random.uniform(2, 5))
        else:
            print(f"[Failed] Skipping doc {doc_id} after {retries} retries.")
            df.at[idx, "status"] = "failed"
            continue

        soup = BeautifulSoup(html, "lxml")
        data_html = soup.find("div", attrs={"class": "judgments"})

        if data_html is None:
            print(f"[Warning] Could not find 'judgments' div in {BASE_URL}. Skipping.")
            df.at[idx, "status"] = "not_found"
            continue

        text = data_html.get_text()
        save_path = os.path.join("G:\\college stuff\\sem6\\NLP project indian\\2024", f"{doc_id}.txt") # change path as necessary
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)
        df.at[idx, "status"] = "done"
        print(f"Document {doc_id} saved successfully.")  # Be kind to the server

    return df_batch

batch_size = 100
for start in range(0, len(df), batch_size):
    end = min(start + batch_size, len(df))
    batch_df = df.iloc[start:end].copy()
    print(f"\nProcessing batch {start} to {end - 1}...")
    df.iloc[start:end] = scrape_and_save(batch_df, start)
    time.sleep(4)

# === Save final status log ===
df.to_csv("scraping_status.csv", index=False)
print("Scraping completed and log saved.")


