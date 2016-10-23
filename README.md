![title](./resources/title.png)

LINE BOT on AWS Lambda + API Gateway using Chalice.

## Functions

| Command   | Image                                 |
|-----------|---------------------------------------|
| Greeting  | ![greeting](./resources/greeting.png) |
| Choice    | ![choice](./resources/choice.png)     |
| Shuffle   | ![shuffle](./resources/shuffle.png)   |
| Weather   | ![weather](./resources/weather.png)   |
| News      | ![news](./resources/news.png)         |
| Echo      | ![echo](./resources/echo.png)         |

## Development

#### Requirements

Because of AWS Lambda's restrictions, Supported python version is 2.7 only.

- beautifulsoup4
- chalice
- line-bot-sdk
- feedparser

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

## LICENSE

MIT. See [LICENSE](./LICENSE)

