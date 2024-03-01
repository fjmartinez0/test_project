import requests
from bs4 import BeautifulSoup

# URL of Deku Deals
url = "https://www.dekudeals.com"

# Fetch the web page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find game deals (example: titles and prices)
game_deals = soup.find_all("div", class_="game-deal")

# Print the first few deals
for deal in game_deals[:5]:
    title = deal.find("h2").text
    price = deal.find("span", class_="price").text
    print(f"Title: {title} | Price: {price}")

# You can extend this to create a wishlist and set up email notifications!
    

#print("Hello world")
#print("Hello world Fernando Martinez")


