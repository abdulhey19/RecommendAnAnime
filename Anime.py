import requests
from bs4 import BeautifulSoup
import random
from io import BytesIO
from PIL import Image

def getAnimeName(url):

    response = requests.get(url)
    response=response.content
    bSoup=BeautifulSoup(response,"html.parser")

    animeList=[]

    for soup in bSoup.find_all("a", {"class": "link-title"}):
        animeList.append(soup.get("href"))

    sayi = random.randint(0, len(animeList))
    anime_url=animeList[sayi]
    return getOneAnimeInfo(anime_url)

def getGenres():
    url="https://myanimelist.net/anime.php"
    response = requests.get(url)
    response = response.content
    bSoup = BeautifulSoup(response, "html.parser")

    listOfGenres=[]

    for soups in bSoup.find("div",attrs={"class":"genre-link"}):
        for soup in soups.find_all("a"):
            genre=soup.text
            genre=genre[0:genre.rfind("(")-1]
            listOfGenres.append(genre)
    return listOfGenres

def getUrl():
    url="https://myanimelist.net/anime.php"
    response = requests.get(url)
    response = response.content
    bSoup = BeautifulSoup(response, "html.parser")

    listOfUrls=[]
    for soups in bSoup.find(attrs={"class":"genre-link"}):
        for soup in soups.find_all("a"):
            genre="https://myanimelist.net"+soup.get("href")
            listOfUrls.append(genre)

    return listOfUrls

def getOneAnimeInfo(url):
    response = requests.get(url)
    response = response.content
    bSoup = BeautifulSoup(response, "html.parser")

    title=bSoup.find("h1",{"class":"title-name h1_bold_none"}).text
    date=bSoup.find("div",{"class":"information-block di-ib clearfix"}).find("a").text
    rank=bSoup.find("div", {"class":"score-label"}).text
    categories=[]
    for soup in bSoup.find_all("span", {"itemprop":"genre"}):
        categories.append(soup.text)

    desc=bSoup.find("p", {"itemprop":"description"}).text
    desc=desc[0:desc.index("[")-1].strip()
    image=bSoup.find("img",{"class":"lazyloaded"}).get("src")
    #image=image.replace("cdn.","")
    return (title,date,rank,categories,desc,image)

def getImg(url):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    return image