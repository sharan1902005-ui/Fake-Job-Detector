import requests
from bs4 import BeautifulSoup


def extract_from_url(url):

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return soup.get_text(" ", strip=True)

    except:
        return ""