![title](./resources/title.png)

LINE BOT on AWS Lambda + API Gateway using Chalice.

## Requirements

- Python2.7
- chalice
- line-bot-sdk
- feedparser

## Functions

| Command   | Image                                 |
|-----------|---------------------------------------|
| Weather   | ![weather](./resources/weather.png)   |
| News      | ![news](./resources/news.png)         |
| Greeting  | ![greeting](./resources/greeting.png) |
| Shuffle   | ![shuffle](./resources/shuffle.png)   |
| Choice    | ![choice](./resources/choice.png)     |
| Echo      | ![echo](./resources/echo.png)         |

## How to run

#### Setup

Create `.chalice/config.json` :

```console
$ cat .chalice/config.json
{
  "app_name": "linebot", 
  "stage": "dev"
}
```

Set `CHANNEL_ACCESS_SECRET` and `CHANNEL_ACCESS_TOKEN` :

```console
$ vim app.py  # and setting your channel secret and channel access token.
```

#### Deploy to AWS Lambda and API Gateway

Deploying by chalice cli:

```console
$ chalice deploy
```

#### Configuration on LINE DEVELOPERS

Open your line bot setting's page and Set WebHook url.

`https://hoge.execute-api.ap-northeast-1.amazonaws.com/dev/callback`

Success! :tada:

## Development

#### Setup environment

```console
$ virtualenv -p python2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt -r requirements-dev.txt -c constraints.txt
```

#### Running tests

```console
$ python -m unittest tests
```

## LICENSE

MIT. See [LICENSE](./LICENSE)

