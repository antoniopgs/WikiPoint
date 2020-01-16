import requests
from bs4 import BeautifulSoup


def read(x):
    info = x.find_all("p")
    text = ""
    for p in info:
        text_piece = p.get_text()
        text += text_piece
    text = text.strip("Our editors will review what you’ve submitted and determine whether to revise the article.")
    return text

def write(x):
    data = read(x)
    with open("data.txt", "w") as file:
        file.write(data)


# Receive Input:
search_term = input("Search: ").title()
# Build URL:
url = "https://www.britannica.com/place/" + search_term
# Get Request:
request = requests.get(url)

# If Request is Successful
if request.status_code == 200:
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')

    # Check for Sub Sections:
    sub_sections = soup.find("ul", {"data-level" : "h1"})

    # If there are sub sections:
    if sub_sections:
        # I can add the data target from any subsection (except 1st) to the url and get full article access:
        sub_sections_2 = sub_sections.findAll("li")
        url_extension = sub_sections_2[1].get("data-target")
        url += url_extension
        url = "https://www.britannica.com/place/Lisbon/The-20th-century"
        request = requests.get(url)
        html = request.text
        soup = BeautifulSoup(html, 'html.parser')
        write(soup)
    else:
    # If there are no Sub Sections, just print the text regularly:      
        write(soup)

# If Page Is Not Found:
elif request.status_code == 404:
    print("No article was found.")
