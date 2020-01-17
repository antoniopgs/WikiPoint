from pptx import Presentation
from bs4 import BeautifulSoup
import requests
import json
import re


# Get Inputs
search_term = input("Search: ").title()

# Build URL
url = "https://en.wikipedia.org/wiki/" + search_term

# Make Request
request = requests.get(url)

# Evaluate Status Code
if request.status_code == 200:
    
    # Get Data
    soup = BeautifulSoup(request.text, "html.parser")

    # Remove All Tables
    soup.table.decompose()

    # Get Headers and Paragraphs
    paragraphs = soup.findAll(["h1", "h2", "h3", "h4", "h5", "h6", "p"])

    """# Get JSON/Dict
    data = {}
    for paragraph in paragraphs:
        data += json.loads(paragraph)"""
    
    # Extract Text Only
    clean_paragraphs = [paragraph.get_text() for paragraph in paragraphs]

    # Join Pieces of Text Together
    text = "\n".join(clean_paragraphs)
    
    # Using Regex to Remove "[x]"
    regex = re.compile("\[.*\]")
    clean_text = regex.sub("", text)

    # Write Text to File:
    with open("text.txt", "w", encoding = "utf-8") as file:
        file.write(clean_text)

    # Create PowerPoint Presentation
    ppt = Presentation()
    title_slide_layout = ppt.slide_layouts[0]
    title_slide = ppt.slides.add_slide(title_slide_layout)
    title = title_slide.shapes.title
    title.text = search_term
    ppt.save('presentation.pptx')
        
elif request.status_code == 404:
    print("No data was found.")
else:
    print("An error occurred.")



