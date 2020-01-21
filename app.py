from pptx import Presentation
import wikipedia
import re

def search():
    search_term = input("Search: ")
    # Fix Search Term in case of errors:
    fixed_search_term = wikipedia.suggest(search_term)
    # If Search Term needs fixing:
    if fixed_search_term:
        return wikipedia.search(fixed_search_term)
    # If Search Term doesn't need fixing:
    else:
        return wikipedia.search(search_term)

def select_topic(search_term):
    while True:
        print("---------- DETECTED TOPICS ---------")
        # Iterate over Search Result's Length and Contents at the same time:
        for i, topic in zip(range(len(search_term)), search_term):
            print(f"{i+1} - {topic}")
        topic_number = input("\nInsert Topic Number: ")
        try: 
            if 1 <= int(topic_number) <= len(search_term):
                return int(topic_number)
            else:
                print("Invalid Topic Number.\n")
        except TypeError:
            print("Invalid Topic Number.\n")

# Search and get info:
search_result = search()
topic_result = select_topic(search_result)
page = wikipedia.page(search_result[topic_result-1])
pre_info = page.content.split("\n== See also ==\n")
info = pre_info[0].strip()

# Write info to .txt file:
with open("text.txt", "w", encoding="utf-8") as file:
    file.write(info)

# Find all tags and add page title as first tag:
tags = [tag.replace("=", "").strip().title() for tag in re.findall("\n==.*==\n", info)]
tags.insert(0, page.title)

# Split by all tags. Get tag's texts:
tags_text = [section.strip() for section in re.split("\n==.*==\n", info)]

# Create List with all Tags and Text:
sections = list(zip(tags, tags_text))
for section in sections:
    print(f"Tag: {section[0]}")
    print()
    print(section[1])
    print("\n ---- BREAK -----\n")

# PowerPoint Generator:
ppt = Presentation()
just_title = ppt.slide_layouts[0]
title_content = ppt.slide_layouts[1]
section_header = ppt.slide_layouts[2]
two_content = ppt.slide_layouts[3]
comparison = ppt.slide_layouts[4]
title_only = ppt.slide_layouts[5]
blank = ppt.slide_layouts[6]
content_caption = ppt.slide_layouts[7]
picture_caption = ppt.slide_layouts[8]
for i in range(len(sections)):
    if i == 0:
        slide = ppt.slides.add_slide(just_title)
    else:
        slide = ppt.slides.add_slide(section_header)
    title = slide.shapes.title
    title.text = sections[i][0]
ppt.save('presentation.pptx')