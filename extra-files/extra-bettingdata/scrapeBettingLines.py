# https://stackoverflow.com/questions/68186451/what-is-the-proper-way-of-using-python-requests-requests-requestget-o
import requests

import datetime
import pandas as pd

# https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-capture-background-xhr-requests/
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

# goalieDF: goalie_name,event_id,opening_line,team, for csv output
goalieDF = pd.DataFrame()

# eventsDF: event_id, home, visitor
eventsDF = pd.DataFrame()

# start to finish of 2023-24 NHL regular season
startDate = datetime.datetime(2023, 10, 10)
endDate = datetime.datetime(2024, 4, 18)

# link template for site (date will be appended to access each day of the regular season)
linkTemplate = 'https://www.bettingpros.com/nhl/odds/player-props/saves/?date='

# key found @ https://www.reddit.com/r/sheets/comments/rnt310/pulling_table_from_bettingproscom/
headers = {
    "x-api-key": "CHi8Hy5CEE4khd46XNYL23dCFX96oUdw6qOt1Dnh"
}

# creates chrome webdriver
# https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-capture-background-xhr-requests/
def get_driver():
    chrome_options = Options()
    
    #performance: https://stackoverflow.com/questions/53657215/how-to-run-headless-chrome-with-selenium-in-python
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# function to scrape bettingpros betting lines for goalie saves, for a given date range (inclusive)
# https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-capture-background-xhr-requests/
def bettingpros(startDate, endDate, linkTemplate):
    global goalieDF, eventsDF

    # grab starting date
    currentDate = startDate

    # loop through date range specified 
    while currentDate <= endDate:

        # datetime to string: https://stackoverflow.com/questions/17245612/formatting-time-as-d-m-y
        dateToString = currentDate.strftime('%Y-%m-%d')

        # construct link for currentDate
        url = linkTemplate + dateToString

        # init driver
        driver = get_driver()

        # get site
        driver.get(url)

        # wait to load
        time.sleep(1)

        # get total height, to automate scrolling until bottom to trigger calls for dynamic data on page (XHR)
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        scroll_position = 0
        # scroll down page until bottom: https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-scroll-page/
        while scroll_position < scroll_height:
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            scroll_position += 250
            time.sleep(0.5)
            scroll_height = driver.execute_script("return document.body.scrollHeight")

        # wait for load
        time.sleep(1)

        # to check if there are games going on the day specified 
        # check the page html for "no offers found"
        # if found, it means no games that day so skip the current date

        # https://stackoverflow.com/questions/35486374/how-to-get-the-entire-web-page-source-using-selenium-webdriver-in-python
        page_source = driver.page_source

        #check if no data
        if "no offers found" in page_source.lower():
            print(f"no data today {dateToString}. skipping this day.")
        else:
            #if data, continue scraping
            print(f"data found {dateToString}. scraping.")

            # problem: using a list, duplicates of xhr requests were being saved
            # solution: use sets
            # https://www.analyticsvidhya.com/blog/2024/02/get-unique-values-from-a-list-using-python/#:~:text=Using%20the%20set()%20Function,-Python's%20set()&text=It%20automatically%20removes%20duplicates%20and,containing%20only%20the%20unique%20elements.
            offer_urls = set()
            event_urls = set()

            # go through all network requests
            for request in driver.requests:
                if request.response:
                    #save 'offers' requests for goalieDF
                    if 'offers' in request.url and 'api.bettingpros.com' in request.url:
                        offer_urls.add(request.url)
                    
                    #save 'events' requests for eventsDF
                    elif 'events' in request.url and 'api.bettingpros.com' in request.url:
                        event_urls.add(request.url)

            # parse offer json files
            if offer_urls:
                for url in offer_urls:
                    response = requests.get(url, headers=headers)
                    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            offers = data.get('offers', [])
                            for offer in offers:
                                #get data
                                for participant in offer.get('participants', []):
                                    goalie_name = participant.get('name', '')
                                    event_id = offer.get('event_id', '')
                                    opening_line = offer.get('selections', [{}])[0].get('opening_line', {}).get('line', '')
                                    team = participant.get('player', {}).get('team', '')

                                    offer_data = {
                                        'goalie_name': goalie_name,
                                        'event_id': event_id,
                                        'opening_line': opening_line,
                                        'team': team
                                    }

                                    #add to dataframe
                                    new_data = pd.DataFrame([offer_data])
                                    goalieDF = pd.concat([goalieDF, new_data], ignore_index=True)
                        except json.JSONDecodeError:
                            print(f"Error: Response content is not valid JSON for {url}")

                    else:
                        print(f"Error: {response.status_code} for URL {url}")

            # scrape events requests
            if event_urls:
                for url in event_urls:
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            events = data.get('events', [])
                            for event in events:
                                event_id = event.get('id')
                                home_team = event.get('home')
                                visitor_team = event.get('visitor')

                                event_data = {
                                    'event_id': event_id,
                                    'home_team': home_team,
                                    'visitor_team': visitor_team
                                }

                                new_event_data = pd.DataFrame([event_data])
                                eventsDF = pd.concat([eventsDF, new_event_data], ignore_index=True)
                        except json.JSONDecodeError:
                            print(f"Error: Response content is not valid JSON for {url}")
                    else:
                        print(f"Error: {response.status_code} for URL {url}")

        driver.quit()

        # https://stackoverflow.com/questions/3240458/how-to-increment-a-datetime-by-one-day
        currentDate += datetime.timedelta(days=1)

    #create csv files
    goalieDF = goalieDF.sort_values(by='event_id')
    eventsDF = eventsDF.sort_values(by='event_id')

    goalieDF.to_csv('goalie_saves_data.csv', index=False)
    eventsDF.to_csv('events_data.csv', index=False)

bettingpros(startDate, endDate, linkTemplate)
