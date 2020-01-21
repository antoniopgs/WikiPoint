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

def split_sections(data):
    # Detect Tags:
    h2_tags = [h2.strip("\n") for h2 in re.findall("\n== .* ==\n", data)]
    h3_tags = [h3.strip("\n") for h3 in re.findall("\n=== .* ===\n", data)]
    h4_tags = [h4.strip("\n") for h4 in re.findall("\n==== .* ===\n", data)]
    h5_tags = [h5.strip("\n") for h5 in re.findall("\n===== .* =====\n", data)]
    h6_tags = [h6.strip("\n") for h6 in re.findall("\n====== .* ======\n", data)]
    # Create Tags Group:
    tags_group = [h2_tags, h3_tags, h4_tags, h5_tags, h6_tags]
    # Create Sections Group:
    h2_sections, h3_sections, h4_sections, h5_sections, h6_sections = [], [], [], [], []
    sections_group = [h2_sections, h3_sections, h4_sections, h5_sections, h6_sections]
    # Generate:
    for tags, sections in zip(tags_group, sections_group):
        for i in range(len(tags)):
            current_tag = tags[i]
            try:
                next_tag = tags[i+1]
                section = data[data.index(current_tag):data.index(next_tag)].strip(current_tag).strip()
            except IndexError:
                section = data[data.index(current_tag):].strip(current_tag).strip()
            sections.append([current_tag, section])
    return sections_group
    

search_result = search()
topic_result = select_topic(search_result)
page = wikipedia.page(search_result[topic_result-1])
pre_info = page.content.split("\n== See also ==\n")
info = pre_info[0].strip()
organized_info = split_sections(info)

for generated_list in organized_info:
    for element in generated_list:
        print(f"\n----- Printing {element[0]} -----\n")
        print(element[1])

with open("text.txt", "w", encoding="utf-8") as file:
    file.write(info)

# Create PowerPoint Presentation
ppt = Presentation()
title_slide_layout = ppt.slide_layouts[0]
title_slide = ppt.slides.add_slide(title_slide_layout)
title = title_slide.shapes.title
title.text = page.title
subtitle = title_slide.placeholders[1]
subtitle.text = page.summary
ppt.save('presentation.pptx')