from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse

app = FastAPI()


def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

def bing_image_search(query):
    query= query.split()
    query='+'.join(query)
    url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    #add the directory for your image here
    DIR="Pictures"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    image_result_raw = soup.find("a",{"class":"iusc"})

    m = json.loads(image_result_raw["m"])
    murl, turl = m["murl"],m["turl"]# mobile image, desktop image

    image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
    return (image_name,murl, turl)

@app.get("/get_url/")
async def root(q: str = ""):
    # print('req_received')
    # print("q_str =", q)
    results = bing_image_search(q)
    # print(results)
    if len(results) >=1 :
        return {"status":"SUCCESS","url": results[1]}
    else:
        return {"status" : "FAILURE"}
