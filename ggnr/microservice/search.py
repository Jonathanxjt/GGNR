from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def fetch_cover_urls(game_data):
    access_url = "https://id.twitch.tv/oauth2/token"
    access_params = {
        "client_id": "429jpzpf7x2073d3kwsscsrpnftx04",
        "client_secret": "qh3rx6nnlruawu3il3hqbk0ase4yfa",
        "grant_type": "client_credentials"
    }
    access_response = requests.post(access_url, params=access_params)
    access_token = access_response.json()["access_token"]

    cover_urls = []
    cover_url = "https://api.igdb.com/v4/covers"
    access_headers = {
        "Client-ID": "429jpzpf7x2073d3kwsscsrpnftx04",
        "Authorization": f"Bearer {access_token}"
    }
    for game in game_data:
        game_id = game.get('id')
        cover_body = f"fields *; where game = {game_id};"
        cover_response = requests.post(cover_url, headers=access_headers, data=cover_body)
        cover_data = cover_response.json()
        if cover_data:
            cover_urls.append("//images.igdb.com/igdb/image/upload/t_cover_big/" + cover_data[0]["image_id"] + ".png")
        else:
            cover_urls.append(None)

    return cover_urls

@app.route('/search', methods=['POST'])
def search_games():
    game_name = request.json['game_name']

    access_url = "https://id.twitch.tv/oauth2/token"
    access_params = {
        "client_id": "429jpzpf7x2073d3kwsscsrpnftx04",
        "client_secret": "qh3rx6nnlruawu3il3hqbk0ase4yfa",
        "grant_type": "client_credentials"
    }
    access_response = requests.post(access_url, params=access_params)
    access_token = access_response.json()["access_token"]

    game_url = "https://api.igdb.com/v4/games"
    access_headers = {
        "Client-ID": "429jpzpf7x2073d3kwsscsrpnftx04",
        "Authorization": f"Bearer {access_token}"
    }
    game_body = f"fields *; search \"{game_name}\"; limit 5;"
    game_response = requests.post(game_url, headers=access_headers, data=game_body)
    game_data = game_response.json()

    cover_urls = fetch_cover_urls(game_data)

    results = []
    for game, cover_url in zip(game_data, cover_urls):
        game_info = {
            'name': game.get('name'),
            'id' : game.get('id'),
            'cover_url': cover_url
        }
        results.append(game_info)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
