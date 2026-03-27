## RuTracker-Downloader
Lightweight telegram-bot written in Python using python-telegram-bot for downloading .torrent files to directories depending on type of content.

Ready-to-use docker-compose.yml with VLESS-proxy to avoid RuTracker and Telegram GeoBan in Russia and other countries where ISP blocks them. 

There are two types of content series and films with their own directories by default. 
## Setup Guide
There are two variants of docker-compose.yml configs.
1. docker-compose.yml - built-in xray-client container to avoid ISP's ban.
2. docker-compose-no-restrictions.yml - config without xray-client container for regions without geoban.

### Built-in proxy setup
To avoid geoban you need to have a working VLESS-proxy. 
You need to change environment variables to your VLESS-proxy inbound settings in docker-compose.yml:
```
environment:
  - ADDRESS=VLESS_IP
  - PORT=VLESS_PORT
  - ID=VLESS_ID
  - PUBLIC_KEY=VLESS_PUB_KEY
  - SHORT_ID=VLESS_SHORT_ID
  - SNI=VLESS_SNI
```
### No-Restrictions
Use docker-compose-no-restrictions.yml for further setup.

### Volumes settings
Change in your docker-compose file PATH_TO_TORRENTS to path where program need to download .torrent files.
```
volumes:
      - PATH_TO_TORRENTS:/home/downloads
```

### .env settings
Before starting the bot you have to add your telegram-bot token given by ! [BotFather](https://t.me/botfather) and your RuTracker account credentials to .env file.
```
BOT_TOKEN=YOUR_BOT_TOKEN
USERNAME=YOUR_RUTRACKER_USERNAME
PASSWORD=YOUR_RUTRACKER_PASSWORD
```

When you set up all exact same way as were written you can start bot using one command:
`docker compose up -d`

