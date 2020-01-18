from pptx import Presentation
import wikipedia


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

with open("text.txt", "w", encoding="utf-8") as file:
    file.write(page.content)

# Create PowerPoint Presentation
ppt = Presentation()
title_slide_layout = ppt.slide_layouts[0]
title_slide = ppt.slides.add_slide(title_slide_layout)
title = title_slide.shapes.title
title.text = page.title
subtitle = title_slide.placeholders[1]
subtitle.text = page.summary
ppt.save('presentation.pptx')