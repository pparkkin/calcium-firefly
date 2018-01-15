# A Swapping API

## API Description

### Authentication

Start authentication flow. Will return a URL which will take you to Google authentication. After authenticating with Google, you will be redirected back and given an authentication token to use for further requests.

Method and path: `POST /auth`

Request: ``

Response: `{"oauth_url": "<authentication url>"}`

### Add new item

Add a new item.

Requires an authentication token passed in the `X-Auth-Token` header.

Method and path: `POST /items`

Request: `{"description": "<description>"}`

Response: `{"id": "<item id>"}`

### List items

List items. Results can be filtered to only return own or others' items.

Requires an authentication token passed in the `X-Auth-Token` header.

Method and path: `GET /items[?filter=own|others]`

Request: ``

Response: `[{"description": "<description>", "owner": "<owner>", "id": "<item id>"}, ...]`

### Swap items

Swap items. The first item needs to be owned by you. After swapping the items will no longer appear in listing.

Requires an authentication token passed in the `X-Auth-Token` header.

Method and path: `POST /swaps`

Request: `{"my_item": "<item id>", "other_item": "<item id>"}`

Response: `{"id": "<swap id>"}`

## Authentication

You will need to authenticate yourself before using the API. Authentication is done using OAuth with Google. Other providers are not implemented, but should be fairly straightforward. User just needs to specify provider, and needs to authenticate with their chosen provider, who will then provide the token and credentials needed on this end.

I wasn't sure how to implement the OAuth flow, but this is what I came up with. With a typical UI application, the application will redirect to the authentication provider, and after authentication the provider will redirect the user back to the application.I believe there's no way to get around the fact that the user needs to authenticate with the OAuth provider, so that needs to be a part of the flow. The way the flow works in this case, since it's a REST API, is that the user will first call an authentication API, which will provide the user with a URL for the authentication provider's authentication endpoint. The user then needs to open the URL in a browser and perform the authentication, after which the browser will give the user a token, which the user can then use to authenticate any further requests they make to the API.

The aim was to try to minimize the amount of actions that need to be done in a browser. Other possiblities would be to have a whole browser based UI for managing the authentication process, which would allow authenticating and managing the authentication tokens. This would probably the current best practice way of doing it, but I didn't want to get too caught up in implementing all of that. Another option would be to do the authentication with the provider without a redirect back to the application, and have the user pass the token from the provider to the application. This would have just broken up the flow on the application side, and turned something that can be automatic into a manual process.

## Deploying the API service

Download your application secret file from Google App Engine dashboard, and save it as `client_secret.json` at the root of the repo (where the `app.yaml` file is).

Install requirements.

```
$ pip install -t lib -r requirements.txt
```

Run development server.

```
$ dev_appserver.py app.yaml
```

Deploy to Google App Engine.

```
$ gcloud app deploy app.yaml
```

## Example use

You need to have a Google account to use the API.

Get URL for OAuth2 with Google.

```
$ curl -X POST http://calcium-firefly-191803.appspot.com/auth -d ''
{"oauth_url": "https://accounts.google.com/o/oauth2/auth..."}
```

Open the URL in your browser, and sign into Google, and allow the application to access your profile information. After signing in, you will be redirected back to the application, and you will receive an authentication token. You will need the authentication token for all further API calls.

Call the API using the authentication token.

```
$ curl --header "X-Auth-Token: Kx7LC4POEv34" -X POST http://calcium-firefly-191803.appspot.com/items -d '{"description": "new south africa"}'
{"id": "5649391675244544"}
$ curl --header "X-Auth-Token: Kx7LC4POEv34" -X POST http://calcium-firefly-191803.appspot.com/items -d '{"description": "under the sun"}'
{"id": "5639445604728832"}
$ curl --header "X-Auth-Token: Kx7LC4POEv34" http://calcium-firefly-191803.appspot.com/items
[{"owner": "pparkkin@gmail.com", "id": "5639445604728832", "description": "under the sun"}, {"owner": "pparkkin@gmail.com", "id": "5649391675244544", "description": "new south africa"}]
$ curl --header "X-Auth-Token: Kx7LC4POEv34" http://calcium-firefly-191803.appspot.com/items?filter=own
[{"owner": "pparkkin@gmail.com", "id": "5639445604728832", "description": "under the sun"}, {"owner": "pparkkin@gmail.com", "id": "5649391675244544", "description": "new south africa"}]
$ curl --header "X-Auth-Token: Kx7LC4POEv34" -X POST http://calcium-firefly-191803.appspot.com/swaps -d '{"my_item": "5639445604728832", "other_item": "5649391675244544"}'
{"id": "5715999101812736"}
$ curl --header "X-Auth-Token: Kx7LC4POEv34" http://calcium-firefly-191803.appspot.com/items
[]
```
