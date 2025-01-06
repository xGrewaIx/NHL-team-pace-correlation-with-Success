import requests as req
import time
import pandas as pd
import datetime

# https://sportsdata.io/cart/free-trial
key = '46ae0c34d4c44216ac33d43945eb5246'

# start to finish of 2023-24 NHL regular season
startDate = datetime.datetime(2023, 10, 10)
endDate = datetime.datetime(2024, 4, 18)

# gets the starting goalies and relevent data for each date specified through sportsdata.io api
def get_goaltenders_data(date):
    url = f"https://api.sportsdata.io/v3/nhl/projections/json/StartingGoaltendersByDate/{date}"
    headers = {
        'Ocp-Apim-Subscription-Key': key
    }
    
    # send request
    response = req.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json() 
    else:
        print(f"error fetching data for {date}: {response.status_code}")
        return None

# helper func to parse data
def parse_goaltender_data(data):

    if data is None:
        return []
    
    goaltender_data = []
    
    for entry in data:
        goaltender_info = {
            'game_id': entry.get('GameID'),
            'home_team': entry.get('HomeTeam'),
            'away_team': entry.get('AwayTeam'),
            'home_goaltender': f"{(entry.get('HomeGoaltender') or {}).get('FirstName', '')} {(entry.get('HomeGoaltender') or {}).get('LastName', '')}",
            'away_goaltender': f"{(entry.get('AwayGoaltender') or {}).get('FirstName', '')} {(entry.get('AwayGoaltender') or {}).get('LastName', '')}"
        }
        goaltender_data.append(goaltender_info)
    
    return goaltender_data

def main():

    current_date = startDate
    all_goaltender_data = []
    
    # loop through regular season
    while current_date <= endDate:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"getting data for {date_str}")
        
        # fetch data
        data = get_goaltenders_data(date_str)
        
        # parse
        goaltender_data = parse_goaltender_data(data)
        
        # append
        all_goaltender_data.extend(goaltender_data)
        
        # next day
        current_date += datetime.timedelta(days=1)
        
        # sleep to avoid API time out
        time.sleep(1)
    
    # create dataframe
    df = pd.DataFrame(all_goaltender_data)
    
    # sort the DataFrame by game_id
    df = df.sort_values(by='game_id', ascending=True)
    
    # Save to CSV (optional)
    df.to_csv('starting_goaltender_data.csv', index=False)

if __name__ == "__main__":
    main()
