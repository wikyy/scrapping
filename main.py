
from fastapi import FastAPI
import requests
import os
from bs4 import BeautifulSoup
import sqlite3

app = FastAPI()






def save_to_db(page_id, page_name ,page_decription):
    conn = sqlite3.connect("data/db.sqlite3")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS pages (page_id text, page_name text , page_decription text)")
    c.execute("INSERT INTO pages (page_id, page_name , page_decription) VALUES (?,?,?)", (page_id, page_name, page_decription ) )
    conn.commit()
    conn.close()

@app.get("https://www.facebook.com/{page_id}")
def scrape_facebook_page(page_id: str):
    url = f"https://www.facebook.com/{page_id}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    page_name = soup.find("title").get_text().strip()
    page_decription = soup.find("meta",{"name":"description"})['content']
 
    return {"page_id": page_id,"page_name": page_name , "page_decription" : page_decription} , page.status_code

   


def test_scrape_facebook_page():
    respone , status_code =scrape_facebook_page("es.muellert")
    assert status_code==200 , "test invalid"
    print(respone)
    
    save_to_db(respone.get("page_id"), respone.get("page_name"),respone.get("page_decription"))

test_scrape_facebook_page()

print('finish')
