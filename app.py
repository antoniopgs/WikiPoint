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

search_result = search()
topic_result = select_topic(search_result)
page = wikipedia.page(search_result[topic_result-1])
pre_info = page.content.split("\n== See also ==\n")
info = pre_info[0].strip()

with open("text.txt", "w", encoding="utf-8") as file:
    file.write(info)

h2_tags = [h2.strip("\n") for h2 in re.findall("\n== .* ==\n", info)]
h3_tags = re.findall("\n=== .* ===\n", info)
h4_tags = re.findall("\n==== .* ====\n", info)
h5_tags = re.findall("\n===== .* =====\n", info)
h6_tags = re.findall("\n====== .* ======\n", info)

# Break Into H2 Sections:
h2_sections = []
for i in range(len(h2_tags)):
    current_tag = h2_tags[i]
    try:
        next_tag = h2_tags[i+1]
        pre_h2_section = info[info.index(current_tag):info.index(next_tag)]
    except IndexError:
        pre_h2_section = info[info.index(current_tag):]
    h2_section = [current_tag, pre_h2_section.strip(current_tag)]
    h2_sections.append(h2_section)

for section in h2_sections:
    print(section)
    print("----- BREAK -----")

# Create PowerPoint Presentation
ppt = Presentation()
title_slide_layout = ppt.slide_layouts[0]
title_slide = ppt.slides.add_slide(title_slide_layout)
title = title_slide.shapes.title
title.text = page.title
subtitle = title_slide.placeholders[1]
subtitle.text = page.summary
ppt.save('presentation.pptx')