# followers-dasboard

A dashboard to track your Instagram, Twitter and Twitch followers and an unofficial API wrapper of the previously mentioned socials.
Built using Svelte, TypeScript and FastApi (Python).
> ⚠️ ATTENTION: the unofficial API wrapper is intended as a personal reverse engineering exercise for didactic purposes. Note that using APIs without owner consent is often forbidden by Terms and Conditions. 

## **API**
The API wrapper is built using Python. The number of followers is extracted by calling the official APIs using Python's Requests library, then formatted using a FastApi's response modal. 
* **Twitter**:
Twitter was the trickiest to get because of some continuously changing headers in the get request, in particular *authorization* and *x-guest-token*. The first one seems to be hard-coded by Twitter once in a while on their website, in particular on a page accessible by an URL present on *https://twitter.com/sw.js*. Once obtained this header, a new guest token is obtained by activating a new guest session. Finally, with the necessary headers and a get request, the number of followers gets returned.
* **Instagram**:
Instagram get request needs two headers, *X-IG-App-ID* and *Cookie*. The data in the code comes from a browser sessions since it seems that these two headers do not expire. 
* **Twitch**:
Similarly to Instagram, the necessary headers don't seem to expire. Instead, Twitch uses a post request to obtain the necessary data, therefore a body containing the username is given. 

## **Site**
A simple single page website to fetch the API and show the number of followers, built using Svelte and TypeScript.