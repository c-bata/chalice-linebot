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

#### Environment Variables

Set environment variables on your AWS console.

```bash
export LINE_BOT_CHANNEL_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export LINE_BOT_CHANNEL_ACCESS_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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

#### Coding styles

```console
$ flake8 --ignore=E501 app.py chalicelib/
```

## LICENSE

MIT. See [LICENSE](./LICENSE)
