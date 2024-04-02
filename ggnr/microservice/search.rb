require 'sinatra'
require 'sinatra/cross_origin'
require 'net/http'
require 'uri'
require 'json'

set :bind, '0.0.0.0'
set :port, 5009

configure do
  enable :cross_origin
end
# Enable CORS
before do
    response.headers['Access-Control-Allow-Origin'] = '*'
  end

options "*" do
    response.headers["Allow"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept, X-User-Email, X-Auth-Token"
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    200
 end
  

def fetch_cover_urls(game_data)
  # Get access token to call IGDB API
  access_url = URI("https://id.twitch.tv/oauth2/token")
  access_params = {
    'client_id' => ENV['CLIENT_ID'],
    'client_secret' => ENV['CLIENT_SECRET'],
    'grant_type' => 'client_credentials'
  }
  # Get access token to call IGDB API
  access_response = Net::HTTP.post_form(access_url, access_params)
  access_token = JSON.parse(access_response.body)["access_token"]

  cover_urls = []
  cover_url = URI("https://api.igdb.com/v4/covers")


  # Get cover image for each game
  game_data.each do |game|
    game_id = game['id']
    cover_body = "fields *; where game = #{game_id};"
    http = Net::HTTP.new(cover_url.host, cover_url.port)
    http.use_ssl = true
    request = Net::HTTP::Post.new(cover_url)
    request["Client-ID"] = ENV['CLIENT_ID']
    request["Authorization"] = "Bearer #{access_token}"
    request.body = cover_body
    cover_response = http.request(request)
    cover_data = JSON.parse(cover_response.body)
    # If cover image exists, add to cover_urls
    if cover_data.any?
      cover_urls.push("https://images.igdb.com/igdb/image/upload/t_cover_big/" + cover_data[0]["image_id"] + ".png")
    else
      cover_urls.push(nil)
    end
  end

  cover_urls
end

post '/search' do
  # Parse request payload
  request.body.rewind
  request_payload = JSON.parse request.body.read
  game_name = request_payload['game_name']

  access_url = URI("https://id.twitch.tv/oauth2/token")
  # Get access token to call IGDB API
  access_params = {
    'client_id' => ENV['CLIENT_ID'],
    'client_secret' => ENV['CLIENT_SECRET'],
    'grant_type' => 'client_credentials'
  }
  access_response = Net::HTTP.post_form(access_url, access_params)
  access_token = JSON.parse(access_response.body)["access_token"]

  game_url = URI("https://api.igdb.com/v4/games")
  http = Net::HTTP.new(game_url.host, game_url.port)
  http.use_ssl = true
  request = Net::HTTP::Post.new(game_url)
  request["Client-ID"] = ENV['CLIENT_ID'] 
  request["Authorization"] = "Bearer #{access_token}"
  # Search for games with similar name to the one provided
  request.body = "fields *; search \"#{game_name}\"; where version_parent=null; limit 5;"
  game_response = http.request(request)
  game_data = JSON.parse(game_response.body)

  cover_urls = fetch_cover_urls(game_data)

  results = []
  # Combine game data with cover image URLs
  game_data.zip(cover_urls).each do |game, cover_url|
    game_info = {
      'name' => game['name'],
      'id' => game['id'],
      'cover_url' => cover_url
    }
    results.push(game_info)
  end
  # Return results as JSON
  content_type :json
  results.to_json
end
