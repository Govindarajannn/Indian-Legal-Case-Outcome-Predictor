# %%
import requests
import re
from bs4 import BeautifulSoup
import time
import json
import urllib.parse


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                  "AppleWebKit/537.36 (KHTML, like Gecko) " +
                  "Chrome/123.0.0.0 Safari/537.36"
}

URL = 'https://indiankanoon.org/browse/'
page = requests.get(URL, headers=headers)  # Add headers here
print("Status code:", page.status_code)    # Check status


# %%
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all(class_ = "browsecat")
table = results[0]

# %%
links_href = []
for td in table.find_all('td'):
    a_tag = td.find('a')
    if a_tag:
        court_name = a_tag.text.strip()
        href = a_tag['href']
        links_href.append(href)


links = {}
no_of_pages = list(range(100))
base = 'https://indiankanoon.org'

# %%
for link in links_href: # loop for multiple courts, if scraping data from multiple courts
    linkd = link
    URL = base+linkd
    page = requests.get(URL,headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    result_new = soup.find_all(class_ = 'browselist')
    links[court_name] = []
    print("Court Name: " + court_name + "\n")
    for link_new in result_new: # loop for every year
        print((link_new.find('a').text) + " Year Started .....\n")
        if((int)(link_new.find('a').text) < 1949 or (int)(link_new.find('a').text) > 2025):
            continue   
        URL = base + link_new.find('a')['href']
        page = requests.get(URL,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        result_new2 = soup.find_all(class_ = 'browselist')
        for link_new2 in result_new2: # loop for every month
            for page_in in no_of_pages:
                time.sleep(1)
                URL = base + link_new2.find('a')['href']
                query = URL + '&pagenum={}'.format(page_in)
                encoded_query = urllib.parse.quote(query)
                URL = f"https://indiankanoon.org/search/?formInput={encoded_query}&pagenum={page_in}"
                page = requests.get(URL, headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                result_new3 = soup.find_all(class_ = 'result_title')
                if(len(result_new3) == 0):
                    break
                for link_new3 in result_new3:
                    URL = base + link_new3.find('a')['href']
                    links[court_name].append(URL)
                    print(URL)
        print("Current Year Completed\n")
    
    

# %%
valid_court_name = ['Rajya Sabha Debates']

final_list = {}
for court_name in valid_court_name:
  final_list["Supreme Court of India"] = links[court_name]


# %%
json_object = json.dumps(final_list, indent = 4) 

# saving the dictionary with links in a json file
with open("links.json", "w") as outfile:  
    outfile.write(json_object)


