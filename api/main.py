from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import requests

import re


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Social(BaseModel):
    social: str
    username: str
    followers: str


@app.get('/')
async def hi():
   return "hi"


@app.get('/instagram/{username}', response_model=Social)
def instagram(username: str):
    headers = {
        "X-IG-App-ID":"1217981644879628", 
        "Cookie":"csrftoken=UBzjwjbhDCQ3dUTPU6D6Rj6gP65j1BGt; mid=ZCCpDgAEAAEjm4-UQcqcFpk_Xa1f; ig_did=491B2C4B-EFAB-4A32-A6FC-08B29C71481B; dpr=2; datr=Om8xZAPqvuJmSxJQQQ77bPnl; rur=\"RVA\0547391109971\0541712498096:01f741054ba6c2a8bf21df499b2769f065ed4bd4efd6bbcd8c20f87d0d380e4b09cf2314\"; ds_user_id=7391109971; sessionid=7391109971%3AnShEmQgNHMcQmU%3A22%3AAYcZUfmEDDsL5J4ALPPhG4mr9c_w30-r2jTstY9-aw; shbid=\"19630\0547391109971\0541712498060:01f7915c893802acaed7bc12a062c9041dfb0847b6376af194c3ee063e6900e88c6e297e\"; shbts=\"1680962060\0547391109971\0541712498060:01f74f496c8d21b383d08fcba10dde48686990adf9c395088943ccbb77ef4ee55440f9a3\"", 
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }

    r = requests.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=headers)

    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="User not found")
    followers = r.json()["data"]["user"]["edge_followed_by"]["count"]
    return {"social": "instagram", "username": username, "followers": f'{followers:,}'}



@app.get('/twitch/{username}', response_model=Social)
def twitch(username: str):
    headers = {
        "Client-Id":"kimne78kx3ncx6brgo4mv6wki5h1ko", 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0"
    }
    
    body = {
		"extensions": {
			"persistedQuery": {
				"sha256Hash": "84ed918aaa9aaf930e58ac81733f552abeef8ac26c0117746865428a7e5c8ab0",
				"version": 1
			}
		},
		"operationName": "ChannelAvatar",
		"variables": {
			"channelLogin": f"{username}"
		}
    }

    r = requests.post("https://gql.twitch.tv/gql", headers=headers, json=body)
    json = r.json()["data"]["user"]

    if json == None:
        raise HTTPException(status_code=404, detail="User not found")
    followers = json["followers"]["totalCount"]
    return {"social": "twitch", "username": username, "followers": f'{followers:,}'}



@app.get('/twitter/{username}', response_model=Social)
def twitter(username: str):

    headers = { 
        "accept-language": "en-US,en;q=0.5",
        "connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0"
    }


    def get_twitter_authorization():
        sw = requests.get("https://twitter.com/sw.js").text
        url = re.search("https://abs.twimg.com/responsive-web/client-serviceworker/serviceworker.(\d|([a-zA-Z]))+.js", sw).group()

        target = requests.get(url).text
        authorization = re.search(r'(Bearer.*?)(\)|$)', target).group().replace("Bearer \".concat(\"", "").replace("\")", "")
        return f'Bearer {authorization}'

    headers["authorization"] = get_twitter_authorization()


    def get_twitter_guest_token():
        result = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers=headers)
        guest_token = result.json()['guest_token']
        return guest_token

    headers["x-guest-token"] = get_twitter_guest_token()

    r = requests.get(f"https://twitter.com/i/api/graphql/k26ASEiniqy4eXMdknTSoQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22blue_business_profile_image_shape_enabled%22%3Afalse%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D", headers=headers)
    json = r.json()["data"]

    if not bool(json):
        raise HTTPException(status_code=404, detail="User not found")
    followers = json["user"]["result"]["legacy"]["followers_count"]
    return {"social": "twitter", "username": username, "followers": f'{followers:,}'}