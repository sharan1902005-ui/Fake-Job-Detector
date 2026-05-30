from newspaper import Article
import requests
from bs4 import BeautifulSoup


def extract_from_url(url):

    try:
        article = Article(url)

        article.download()

        article.parse()

        if len(article.text) > 100:
            return article.text

    except:
        pass

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

        text = soup.get_text(
            " ",
            strip=True
        )

        return text

    except:
        return ""