import requests
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


    if not deal_titles:
        print("No deal titles found. Check the HTML structure.")
    else:
        for title in deal_titles:
            game_title = title.find("div", class_="h6 name")
            print(game_title.text.strip())
            title_subelements = title.find_all("div", class_="card-badge")
            for subelement in title_subelements:
                game_price = subelement.find("s", class_="text-muted")
                game_discount = subelement.find("strong", class_="")
                game_discount_per = subelement.find("span", class_="align-text-bottom")
                print(game_price.text.strip())
                print(game_discount.text.strip())
                print(game_discount_per.text.strip())


except requests.RequestException as e:
    print(f"Error fetching data: {e}")

# Add a delay to avoid rate limiting
time.sleep(2)
