from youtubesearchpython import VideosSearch
import json
from pprint import pprint
white_list = [f'{i} hours ago' for i in range(23)] + [f'{i} minetes ago' for i in range(59)] + [f'{i} days ago' for i in range(1,7)]

chanels = []
query_list = ["Tesla", "Facebook", "bitcoin", "GTA", "rockstar", "python"]
list_publiched = []

#create dictionary
results = {}
def vysledky():
  for query in query_list:
    #Pro ukladani nejnovejsich videi
    erlyer_videos = []
    #vytazeni 100 videi
    videosSearch = VideosSearch(query, limit = 20, language="en")
    #vytvori list slovniku jednotlivych videi
    videos = videosSearch.result()["result"]
    #rostridi videa
    for video in videos:
      if video["publishedTime"] in white_list:
        erlyer_videos.append(video)
    #Upraveni co vsechno ulozit do slovniku results
    results[query] = erlyer_videos
  vysledky_podle_query = {}
  print(results)
  for q in query_list:
    print(q)
    mezi = []
    for i in range(3):
      try:
        print(i)
        # print("aktualni", vysledky_podle_query[q])
        print(["https://youtu.be/" + results[q][i]["id"], results[q][i]["title"]])
        mezi.append(["https://youtu.be/" + results[q][i]["id"], results[q][i]["title"]])
      except:
        print(59*"=")
        print("prazdnyyy:",q)
        print(59 * "=")
    vysledky_podle_query[q] = mezi
  return vysledky_podle_query