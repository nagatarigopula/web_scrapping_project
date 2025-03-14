import requests
from bs4 import BeautifulSoup
import re

url = "https://example.com/reviews"  # Replace with actual site
headers = {"User-Agent": "Mozilla/5.0"}

def scrape_reviews():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []
    for review in soup.find_all(class_="review-class"):  # Adjust class accordingly
        name = review.find(class_="user-name").text.strip()
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", review.text)
        email = email_match.group(0) if email_match else "N/A"
        content = review.find(class_="review-text").text.strip()
        rating = int(review.find(class_="review-rating").text.strip()[0])
        reviews.append({"name": name, "email": email, "review": content, "rating": rating})

    return reviews

print(scrape_reviews())
