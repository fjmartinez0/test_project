import requests, json
from bs4 import BeautifulSoup
import time
from datetime import datetime

url = "https://www.dekudeals.com/eshop-sales?filter[since]=2024-02-29&sort=metacritic"
headers = {"User-Agent": "Your User Agent String"}



try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors
    soup = BeautifulSoup(response.content, "html.parser")
    deal_titles = soup.find_all("div", class_="col-xl-2 col-lg-3 col-sm-4 col-6 cell")

    #print(deal_titles)
    #print(deal_titles.prettify())

    parsed_titles = []
    more_game_details = []

    if not deal_titles:
        print("No deal titles found. Check the HTML structure.")
    else:
        for title in deal_titles:
            game_url = title.find("a", class_="main-link").get('href')
            game_url = 'https://www.dekudeals.com' + game_url
            print(game_url)
            

            def get_title_details(var_game_url):
                new_headers = {"User-Agent": "Your User Agent String"}
                new_response = requests.get(var_game_url, headers=new_headers)
                new_soup = BeautifulSoup(new_response.content, "html.parser")
                this_game_details = []
                title_details = new_soup.find_all("li", class_="list-group-item")
                for detail in title_details:
                    one_detail = detail.text.strip()
                    if (one_detail.find("Released")>=0):
                        game_release_date = one_detail[10:]
                        print(game_release_date)
                    elif (one_detail.find("Platforms")>=0):
                        game_platforms = one_detail[11:]
                        print(game_platforms)
                    else:
                        continue                
                
                script = new_soup.find(id = "price_history_data")
                game_price_history_jsonObj = json.loads(script.contents[0])
                game_price_history = game_price_history_jsonObj['data']

                my_curated_price_list = []
                my_price_change_dates = []
                for price_point in game_price_history:
                    current_price_point = [price_point[0], price_point[-1]]

                    #print("what is this" + price_point[0]) 
                    #print(type(price_point))
                    if not my_curated_price_list:
                        #my_curated_price_list.append(price_point)
                        my_curated_price_list.append(current_price_point)
                        my_price_change_dates.append(current_price_point[0])
                        #print(my_curated_price_list)
                        #print(price_point)
                    else:
                        #print(price_point[0], )
                        #if it is ONLY the same price as before, skip record, otherwise, append
                        if my_curated_price_list[-1][-1:] == current_price_point[-1:]: 
                            continue
                        else:
                            my_curated_price_list.append(current_price_point)
                            my_price_change_dates.append(current_price_point[0])
                            #print(price_point)
                this_game_details.append([game_release_date, game_platforms, my_curated_price_list, my_price_change_dates])
                return this_game_details
            
                #print(price_point[1:]) # this is an array of price points at a given date
                #print(my_curated_price_list)
            
            more_game_details = get_title_details(game_url)
            game_price_history = more_game_details[0][2]
            game_price_changes_dates_history = more_game_details[0][3]
            
            print("I mam here")
            print(more_game_details[0][3])
            #print(more_game_details[0][2])


            # How long it takes for the first discount
            def time_for_first_discount(game_price_history):
                print(len(game_price_history))
                if(len(game_price_history)>=2):
                    #print(1)
                    print(len(game_price_history))
                    print("First price: " + game_price_history[0][0])
                    print("First discount: " + game_price_history[1][0])
                    d1 = datetime.strptime(game_price_history[0][0], "%Y-%m-%d")
                    d2 = datetime.strptime(game_price_history[1][0], "%Y-%m-%d")
                    return abs((d2 - d1).days)
                else:
                    return 0
                
            def discounts_analysis(game_price_history, game_price_changes_dates_history):
                print("======= Discounts Analysis =========")
                print(len(game_price_history))
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
                        print(difference)
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
                    return discounts_analsysis_result
                else:
                    return 0
                
            days_for_first_discount = time_for_first_discount(game_price_history)
            print("Days for first discount: " + str(days_for_first_discount))

            discounts_analysis(game_price_history, game_price_changes_dates_history)

            # How often it gives a discount
                            
            # How long does a discount last

            
            game_title = title.find("div", class_="h6 name")
            print(game_title.text.strip())
            game_title = game_title.text.strip()
            game_price = title.find("s", class_="text-muted")
            print(game_price.text.strip())
            game_price = game_price.text.strip()
            game_discount = title.find("strong", class_="")
            game_discount_per = title.find("span", class_="align-text-bottom")
            print(game_discount.text.strip())
            print(game_discount_per.text.strip())
            game_discount = game_discount.text.strip()
            game_discount_per = game_discount_per.text.strip()
            game_metacritic_score = title.find("span", class_="text-white p-1 rounded bg-success")
            if not game_metacritic_score:
                game_metacritic_score = title.find("span", class_="text-white p-1 rounded bg-warning")
                if not game_metacritic_score:
                    print("No metacritic score found. Check the HTML structure.")
            game_metacritic_score = game_metacritic_score.text.strip()
            parsed_titles.append([game_title, game_price, game_discount, game_discount_per, game_metacritic_score])
            break
        #print(parsed_titles)



except requests.RequestException as e:
    print(f"Error fetching data: {e}")

# Add a delay to avoid rate limiting
time.sleep(2)
