import re
from flask import jsonify
import requests
from bs4 import BeautifulSoup


def get_recipe(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'json',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        response = requests.get(url, headers=headers)
        print(response)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({'body':'Error- URL not found'})
        else:
            return jsonify({'error': 'Error getting recipe: ' + str(e)}), response.status_code
    except requests.RequestException as e:
        print("here")
        return jsonify({'error': 'Error getting recipe: ' + str(e)}), 500
    soup = BeautifulSoup(response.content, 'html.parser')
    class_re = re.compile('wprm-recipe wprm-recipe-template(.)*')
    div = soup.find_all('div', class_=class_re)

    if len(div) > 0:
        return jsonify({'body': str(div[0])})
    else:
        print("Template Not Found")
        return jsonify({'body': "<div>Error- site format not yet supported</div>"})
    
    