import requests, json
from bs4 import BeautifulSoup
import time

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
                #title_details = soup.find("ul", class_="details list-group list-group-flush")
                title_details = new_soup.find_all("li", class_="list-group-item")
                #more_details = title_details.find_all("li", class_="list-group-item")
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
                
                #table extract of historic prices
                #table = new_soup.find('table', attrs={'class':'subs noBorders evenRows'})
                #table_rows = table.find_all('tr')
                script = new_soup.find(id = "price_history_data")
                game_price_history_jsonObj = json.loads(script.contents[0])
                game_price_history = game_price_history_jsonObj['data']

                for price_point in game_price_history:
                    #print("what is this" + price_point[0]) 
                    print(price_point) # this is an array of price points at a given date
                #for a in game_price_history_jsonObj['data']:
                #    print(a)
                    #for b in a['data']:
                    #    print(b)

                #print(json.loads(script.contents[0]))

                    #print("This is one detail" + one_detail)        

            get_title_details(game_url)
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


        #print(parsed_titles)



except requests.RequestException as e:
    print(f"Error fetching data: {e}")

# Add a delay to avoid rate limiting
time.sleep(2)
