import requests, json
from bs4 import BeautifulSoup
import time
from datetime import datetime

# Define the website to be crawled
url = "https://www.dekudeals.com/eshop-sales?filter[since]=2024-02-29&sort=metacritic"
headers = {"User-Agent": "Your User Agent String"}


def get_game_highlevel_details(game_title):
    #print(game_title.text.strip())
    this_game_name = game_title.find("div", class_="h6 name").text.strip()    
    this_game_price = game_title.find("s", class_="text-muted").text.strip()
    this_game_discount = game_title.find("strong", class_="").text.strip()
    this_game_discount_per = game_title.find("span", class_="align-text-bottom").text.strip()
        
    this_game_metacritic_score = game_title.find("span", class_="text-white p-1 rounded bg-success").text.strip()
    if not this_game_metacritic_score:
        this_game_metacritic_score = game_title.find("span", class_="text-white p-1 rounded bg-warning").text.strip()
        if not this_game_metacritic_score:
            print("No metacritic score found. Check the HTML structure.")

    return [this_game_name, this_game_price, this_game_discount, this_game_discount_per, this_game_metacritic_score]

def get_game_price_history_data(json_script_pricedata):

    game_price_history_jsonObj = json.loads(json_script_pricedata.contents[0])
    game_price_history = game_price_history_jsonObj['data']

    my_curated_price_list = []
    my_price_change_dates = []
    for price_point in game_price_history:
        current_price_point = [price_point[0], price_point[-1]]

        #print(type(price_point))
        if not my_curated_price_list:
            my_curated_price_list.append(current_price_point)
            my_price_change_dates.append(current_price_point[0])
        else:
            # If it is the same price as before (not date), skip record, otherwise, append
            if my_curated_price_list[-1][-1:] == current_price_point[-1:]: 
                continue
            else:
                my_curated_price_list.append(current_price_point)
                my_price_change_dates.append(current_price_point[0])
    return my_curated_price_list, my_price_change_dates

 # How long it takes for the first discount
def get_days_for_first_discount(game_price_history):
    #print(len(game_price_history))
    if(len(game_price_history)>=2):
        #print(1)
        #print(len(game_price_history))
        #print("First price: " + game_price_history[0][0])
        #print("First discount: " + game_price_history[1][0])
        d1 = datetime.strptime(game_price_history[0][0], "%Y-%m-%d")
        d2 = datetime.strptime(game_price_history[1][0], "%Y-%m-%d")
        return abs((d2 - d1).days)
    else:
        return 0
    
def discounts_analysis(game_price_history, game_price_changes_dates_history):
    print("======= Discounts Analysis =========")
    #print(len(game_price_history))
    discounts_analsysis_result = []
    if(len(game_price_history)>=2):
        #print(1)
        #print(game_price_history[0:][0])
        date_list = game_price_changes_dates_history
        #print(date_list)
        # Convert date strings to datetime objects
        datetime_list = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in date_list]
        #print (len(game_price_changes_dates_history))
        total_days = 0
        # Calculate differences
        for i in range(len(game_price_changes_dates_history) - 1):
            #print(i)
            difference = (datetime_list[i + 1] - datetime_list[i]).days
            total_days += difference
            #print(difference)
            #print(f"Difference between {date_list[i]} and {date_list[i + 1]}: {difference}")
        my_avg_days_for_price_change = total_days/(len(game_price_changes_dates_history) - 1)
        print (f"Avg days for price change:  {my_avg_days_for_price_change}")

        for discount in game_price_history:
            price_change_date = discount[-1]
            price_change_value = discount[-1]
            d1 = datetime.strptime(game_price_history[0][0], "%Y-%m-%d")
            d2 = datetime.strptime(game_price_history[1][0], "%Y-%m-%d")

            #print(discount)
            #print("here")
            #print(discount[0][0] + " " + discount[0][-1] )
            #print(len(discount))
            #print(discount[1][0] + " " + discount[1][-1] )
            #print(len(game_price_history))
            #print("First price: " + game_price_history[0][0])
            #print("First discount: " + game_price_history[1][0])
            #d1 = datetime.strptime(game_price_history[0][0], "%Y-%m-%d")
            #d2 = datetime.strptime(game_price_history[1][0], "%Y-%m-%d")
            #discounts_analsysis_result.append(abs((d2 - d1).days))
        return my_avg_days_for_price_change
    else:
        return 0
    
def get_game_details(var_game_url):
    headers = {"User-Agent": "Your User Agent String"}
    response = requests.get(var_game_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    this_game_details_html = soup.find_all("li", class_="list-group-item") # ---->>> this gets all of the left panel data

    this_game_details = []
    
    # Only the platforms and release date are relevant
    for detail in this_game_details_html:
        current_detail_string = detail.text.strip()
        if (current_detail_string.find("Released")>=0):
            game_release_date = current_detail_string[10:]
            print(game_release_date)
        elif (current_detail_string.find("Platforms")>=0):
            game_platforms = current_detail_string[11:]
        else:
            continue
    
    # Process the price history data from a json object within the HTML
    json_script_pricedata = soup.find(id = "price_history_data")
    game_price_history_data, game_price_history_dates = get_game_price_history_data(json_script_pricedata)
    game_days_for_first_discount =  get_days_for_first_discount(game_price_history_data)
    game_avg_days_for_price_change = discounts_analysis(game_price_history_data, game_price_history_dates)

    this_game_details.append([game_release_date, game_platforms, game_price_history_data, game_price_history_dates, 
                              game_days_for_first_discount, game_avg_days_for_price_change])
    return this_game_details


def main():


    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")
        game_titles_list = soup.find_all("div", class_="col-xl-2 col-lg-3 col-sm-4 col-6 cell")

        games_data = []
        more_game_details = []

        if not game_titles_list:
            print("No deal titles found. Check the HTML structure.")
        else:
            for game_title in game_titles_list:
                game_url = 'https://www.dekudeals.com' + game_title.find("a", class_="main-link").get('href')
                print(game_url)
                
                game_highlevel_data = get_game_highlevel_details(game_title)
                game_more_details = get_game_details(game_url)
                
                #games_data.append(game_highlevel_data, game_more_details)
                
                #print(games_data[-1])

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

    # Add a delay to avoid rate limiting
    time.sleep(2)

if __name__ == "__main__":
    main()