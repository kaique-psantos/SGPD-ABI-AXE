import requests, os
from bs4 import BeautifulSoup

def get_instagram_followers():
    url = f"https://www.instagram.com/abiaxeegbe_oficial/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        followers = soup.find('meta', property='og:description')['content']
        followers_count = followers.split(' ')[0].replace(',', '.')
        return followers_count
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return 0



