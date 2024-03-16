# from flask import Flask, request, jsonify
import requests

# app = Flask(__name__)

access_url = "https://id.twitch.tv/oauth2/token"
access_params = {
    "client_id": "429jpzpf7x2073d3kwsscsrpnftx04",
    "client_secret": "qh3rx6nnlruawu3il3hqbk0ase4yfa",
    "grant_type": "client_credentials"
}

access_response = requests.post(access_url, params=access_params)

access_token = access_response.json()["access_token"]

print(access_token)

game_url = "https://api.igdb.com/v4/games"

access_headers = {
    "Client-ID": "429jpzpf7x2073d3kwsscsrpnftx04",
    "Authorization": f"Bearer {access_token}"
}
#TODO:
# 1. Get the game name from frontend
game_name = "mario"
game_body = "fields *; search" + '\"' + game_name + '\"' + ";" + "limit 5;"

game_response = requests.post(game_url, headers=access_headers, data=game_body)

game_data = game_response.json()
game_name_array = []
game_id_array = []
for game in game_data:
    game_name_array.append(game["name"])   
    game_id_array.append(game["id"]) 

print(game_name_array)
print(game_id_array)
cover_url = "https://api.igdb.com/v4/covers"

cover_urls = []

for game_id in game_id_array:
    cover_body = "fields *; where id = " + str(game_id) + ";"
    cover_response = requests.post(cover_url, headers=access_headers, data=cover_body)
    cover_data = cover_response.json()
    if cover_data:
        cover_urls.append(cover_data[0]["url"])
    else:
        cover_urls.append(None)

print(cover_urls)
