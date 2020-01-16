import requests
from bs4 import BeautifulSoup


search_term = input("Search: ").title()
url = "https://www.britannica.com/place/" + search_term

request = requests.get(url)
if request.status_code == 200:
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    sub_page_list = soup.find("ul", {"data-level" : "h1"})

    # Try to Find Children/Sub-Topics.
    try:
        # The False recursive is to only search for direct children.
        sub_info = sub_page_list.findAll("li", recursive=False)
        sub_info_2 = [child.find(href=True) for child in sub_info]
        
        # Extracting Links.
        links = [x["href"] for x in sub_info_2]
        # Extracting Topics.
        topics = [x.get_text().title() for x in sub_info_2]
        # Merging Links and Topics Together.
        links_and_topics = list(zip(links, topics))
        
        for i in links_and_topics:
            print(i)
            print()
        for i in links_and_topics:
            print(i)
            print()

    # If there are no Sub-Topics, just print the text.        
    except AttributeError:
        info = soup.find_all("p")
        text = ""
        for p in info:
            text_piece = p.get_text()
            text += text_piece
        text = text.strip("Our editors will review what you’ve submitted and determine whether to revise the article.")
        print(text)
elif request.status_code == 404:
    print("No article was found.")
