# flying_bear_bot
flying_bear_bot

# Setup

Install deps
```
pip install -r requrements.txt
```
Define local_settings.py under 
```
flying_bear_bot/flying_bear_bot/local_settings.py
```
with telegram bot related variables:
```
TELEGRAM_BOT = [{
    'token': '', # bot token
    'register': 'bot.dispatchers.register',
    'webhook': ''
}]
```
`webhook` url is used to get Telegram updates without hammering server. Read more [here](https://core.telegram.org/bots/api#setwebhook)
Test env is being run on Heroku so url there is provided out of the box. To test bot locally you will need
to have `real` domain name or setup tunel using something like [ngrok](https://ngrok.com/)

# ngrok setup 
1. Download and install ngrok appropriate for your platfrom
2. run 
```
./ngrok http 8000 # in case if your django server is running on 8000 port
```
In outpur you will get `Forwarding` link. you need one with `https`.
Now you can fill it into settings
```
TELEGRAM_BOT = [{
    'token': '', # bot token
    'register': 'bot.dispatchers.register',
    'webhook': '{your ngrok tunel url}/bot_register/%s'
}]
```