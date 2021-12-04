import requests as r
from bs4 import BeautifulSoup as bs
#spojeni se se servrem a ziskani dat

zdroje = {"https://www.hackster.io/news": {"selector": "a.hckui__typography__link",
                        "url": "https://www.hackster.io/news",
                        "list_clanku": []},
          "https://www.computerworld.com/news/": {"selector": "h3 a" ,
                                "url": "https://www.computerworld.com/news/",
                                "list_clanku": []},
          "https://www.gamespot.com/news/": {"selector": ".promo-strip__item a",
                           "url": "https://www.gamespot.com/news/",
                           "list_clanku": []}
         }

def download_articles(url: str, selector: str):
  odezva = r.get(url)
  #Overeni propojeni se serverem ... chceme 200
  if odezva.status_code != 200:
      return list()

  print(odezva.status_code)

  #Prevod textu na html
  html = odezva.text
  soup = bs(html)
  vysledek = {}
  list_clanku = []
  list_nadpisu = []
  for elem in soup.select(selector)[:3]:
    #print("https://www.hackster.io/news" + elem["href"])
    list_clanku.append(url + elem["href"])
    list_nadpisu.append(soup.title.text.replace("\n", ""))
  list_clanku = set(list_clanku)
  vysledek[url] = list(list_clanku)
  vysledek["title"] = list_nadpisu
  return vysledek
def stahni():
    for zdroj in zdroje:
      url = zdroje[zdroj]["url"]
      selector = zdroje[zdroj]["selector"]
      stazeno = download_articles(url, selector)
      zdroje[zdroj]["list_clanku"] = stazeno[zdroj]
      zdroje[zdroj]["nadpis"] = stazeno["title"]
    return zdroje