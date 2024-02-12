# Import modules
from bs4 import BeautifulSoup
import re
import asyncio
import aiohttp
from datetime import datetime
import psycopg2
import schedule
from dotenv import load_dotenv
import os

# Load settings values from .env
load_dotenv()

# Open connection with database
connection = psycopg2.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )

with connection.cursor() as cursor:
        # Create table if it not exists
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS auto_ria(
                url TEXT,
                title TEXT,
                price_usd INT,
                odometer INT,
                username TEXT,
                phone_number INT,
                image_url TEXT,
                images_count INT,
                car_number TEXT,
                car_vin TEXT,
                datetime_found DATE);"""
        )        
        connection.commit()
        # Close connection with database
        connection.close()


# Get ads urls from the page
async def getAdsUrls(session, page_url):
    response = await session.get(url=page_url)
    soup = BeautifulSoup(await response.text(), 'lxml')
    adsUrls = [ad.get('href') for ad in soup.find_all(class_ = 'm-link-ticket')]

    return adsUrls

# Get data from ad
async def getAdsData(session, page):
    
    adsUrls = await getAdsUrls(session, os.getenv('URL') + str(page))

    # Open connection with database
    try:
        connection = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        with connection.cursor() as cursor:

            for adUrl in adsUrls:
                # Check if the ad is the table
                checkUnique = cursor.execute(f"SELECT EXISTS (SELECT url FROM auto_ria WHERE url = '{adUrl}')")
                # If ad is not in table
                if checkUnique is None:
                    response = await session.get(url=adUrl)
                    soup = BeautifulSoup(await response.text(), 'lxml')

                    # Get title
                    autoTitle = soup.find(class_ = 'auto-content_title').text

                    # Get price
                    autoPrice = soup.find(class_ = 'price_value').find('strong').text
                    # Convert price in usd if it is in eur
                    if '€' in autoPrice:
                        autoPriceUSD = round(int(autoPrice[:-1].replace(' ', '')) * 1.08)
                    # Convert price in usd if it is in uah
                    elif 'грн' in autoPrice:
                        autoPriceUSD = round(int(autoPrice[:-3].replace(' ', '')) / 37.62)
                    # Delete some not needed information 
                    else:
                        autoPriceUSD = int(autoPrice[:-1].replace(' ', ''))

                    # Get odometer value
                    autoOdometer = (soup.find('span', class_ = 'argument', string = re.compile(r'\bтис\b'))).text
                    # Convert string into integer
                    autoOdometer = int(re.sub(r'[ .тискм]', '', autoOdometer)) * 1000

                    # Get seller's name
                    sellerName = soup.find(class_ = re.compile('seller_info_name'))
                    # If seller's name not exists it mean that car is not longer for sale and we should skip this ad
                    if sellerName is None:
                        continue
                    # Get text from soup object
                    else:
                        sellerName = sellerName.text


                    # Get seller's phone number
                    sellerNumber = soup.find(class_ = 'phone bold').find('span', class_ = 'mhide').text
                    # Delete some not needed information
                    sellerNumber = int('38' + re.sub(r'[ ()x-]', '', sellerNumber))
                    


                    # Get title img's url 
                    autoImgUrl = soup.find(class_ = 'outline m-auto').get('src')
                    

                    # Get amount of images
                    autoImgsAmount = soup.find(class_ = 'count').find(class_ = 'mhide').text
                    # Delete some not needed information
                    autoImgsAmount = int(re.sub(r'[ з]', '', autoImgsAmount))


                    # Get car's number
                    autoNumber = soup.find(class_ = 'state-num ua')
                    # If it is not car's number in ad
                    if autoNumber == None:
                        autoNumber = 'Авто пригнане'
                    # Get text from soup object and delete some not needed information
                    else:
                        autoNumber = autoNumber.text[:10]


                    # Get vin's number
                    autoVin = soup.find('span', class_ = 'label-vin')

                    # Sometimes vin could be in another place or vin not exists
                    if autoVin is None:
                        # If vin is in another place
                        try:
                            autoVin = soup.find('span', class_ = 'vin-code').text
                        # If vin is not exists
                        except:
                            autoVin = 'Відсутній'
                    # Get text from soup object
                    else:
                        autoVin = autoVin.text
                        

                    # Get date of finding ad
                    dateTimeAutoFound = datetime.now().date()


                    # Insert ad's data into table
                    cursor.execute(f"""INSERT INTO auto_ria 
                            (url, title, price_usd, odometer,
                            username, phone_number, image_url, images_count,
                            car_number, car_vin, datetime_found) VALUES
                            ('{adUrl}', '{autoTitle}', {autoPriceUSD}, {autoOdometer},
                            '{sellerName}', {sellerNumber}, '{autoImgUrl}', {autoImgsAmount}, 
                            '{autoNumber}', '{autoVin}', '{dateTimeAutoFound}');""")
                    connection.commit()

    # If exists some problem with database
    except:
        print("[ERROR] Something went bad while working with database")

    finally:
        # If exists connection with database we should close this connection
        if connection:
            connection.close()

    

# Function for creating asyncio tasks 
async def gatherData():
    url = os.getenv('URL')
    
    # Open aiohttp session
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url)
        soup = BeautifulSoup(await response.text(), 'lxml')

        pagesAmount = int(soup.find_all("span", class_='page-item mhide')[5].text.replace(' ', ''))
        tasks = []
        
        # Cycle for adding tasks into array
        for page in range(1, pagesAmount + 1):
            task = asyncio.create_task(getAdsData(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)

# Main function
def main():
    asyncio.run(gatherData())

# Database dump function
def dbDump():
    os.system(f'pg_dump -h {os.getenv('DB_HOST')} -u {os.getenv('DB_USER')} {os.getenv('DB_NAME')} > ./dumps/dump_{datetime.now().date()}.sql')
        

if __name__ == '__main__':
    # Start parsing function in some time that could we changed in .env(default 12:00)
    schedule.every().day.at(os.getenv('START_TIME')).do(main)
     # Start dump function in some time that could we changed in .env(default 12:00)
    schedule.every().day.at(os.getenv('DUMP_TIME')).do(dbDump)


    # Start while cycle for schedule
    while True:
        schedule.run_pending()









