import json
from newspaper import Article
from bs4 import BeautifulSoup

def extract_article_as_json(url: str, bold: bool = False) -> dict:
    article = Article(url)
    article.download()
    article.parse()

    title = article.title
    raw_html = article.html
    soup = BeautifulSoup(raw_html, "html.parser")

    # Get subtitle
    subtitle = ""
    meta_desc = soup.find("meta", {"name": "description"})
    if meta_desc and meta_desc.get("content"):
        subtitle = meta_desc["content"]
    elif soup.find("h2"):
        subtitle = soup.find("h2").get_text(strip=True)

    
    # Final clean body from article.text (already filtered by newspaper3k)
    # Replace matching bold words with **word** if they are in the text
    body = article.text
    if bold:
        for tag in soup.find_all(["b", "strong"]):
            bold_text = tag.get_text(strip=True)
            if bold_text in body:
                body = body.replace(bold_text, f"**{bold_text}**")

    return {
        "title": title,
        "subtitle": subtitle,
        "body": body
    }
