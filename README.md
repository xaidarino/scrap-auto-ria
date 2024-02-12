Installation:
=====================
Python and modules installation:
---
sudo apt-get update
sudo apt-get install python 3.8
pip3 install BeautifulSoup4
pip3 install aiohttp
pip3 install psycopg2
pip3 install schedule
pip3 install python-dotenv


Docker and docker-compose installation:
---
On Ubuntu:
sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
sudo apt-get install docker-compose-plugin
---
On Debian:
sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
sudo apt-get install docker-compose-plugin



Structe:
=====================
main.py - main file that parses web-site auto.ria.com
docker-compose.yaml - file that up postgresql database in docker container
.env - configure file with settings values
dumps - directory with database's dumps
=====================

Configuration:
=====================
URL - auto.ria.com url
DB_HOST - database's IP address
DB_NAME - database's name
DB_USER - database's user's login 
DB_PASSWORD - database's user's password
START_TIME - in that time file will parse web-site
DUMP_TIME = in that time file will make dump database


How to run:
=====================
1. Unarchive files in any directory
2. Next you should be in this directory
3. For the first time: docker-compose up --build (Next times: docker-compose up)
4. python3 main.py
