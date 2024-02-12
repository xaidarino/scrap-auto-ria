Installation:
=====================
Python and modules installation:
---
1. sudo apt-get update<br/>
2. sudo apt-get install python 3.8<br/>
3. pip3 install BeautifulSoup4<br/>
4. pip3 install aiohttp<br/>
5. pip3 install psycopg2<br/>
6. pip3 install schedule<br/>
7. pip3 install python-dotenv<br/>


Docker and docker-compose installation:
---
On Ubuntu:
---
1. sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common<br/>
2. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -<br/>
3. sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"<br/>
4. sudo apt update<br/>
5. apt-cache policy docker-ce<br/>
6. sudo apt install docker-ce<br/>
7. sudo systemctl status docker<br/>
8. sudo apt-get install docker-compose-plugin<br/>

On Debian:
---
1. sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common<br/>
2. curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -<br/>
3. sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"<br/>
4. sudo apt update<br/>
5. apt-cache policy docker-ce<br/>
6. sudo apt install docker-ce<br/>
7. sudo systemctl status docker<br/>
8. sudo apt-get install docker-compose-plugin<br/>



Structe:
=====================
 main.py - main file that parses web-site auto.ria.com<br/>
 docker-compose.yaml - file that up postgresql database in docker container<br/>
 .env - configure file with settings values<br/>
 dumps - directory with database's dumps<br/>


Configuration:
=====================
 URL - auto.ria.com url<br/>
 DB_HOST - database's IP address<br/>
 DB_NAME - database's name<br/>
 DB_USER - database's user's login <br/>
 DB_PASSWORD - database's user's password<br/>
 START_TIME - in that time file will parse web-site<br/>
 DUMP_TIME = in that time file will make dump database<br/>


How to run:
=====================
1. Unarchive files in any directory<br/>
2. Next you should be in this directory<br/>
3. For the first time: docker-compose up --build (Next times: docker-compose up)<br/>
4. sudo python3 main.py<br/>
