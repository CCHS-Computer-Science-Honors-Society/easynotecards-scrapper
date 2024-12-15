from scraper.core import scrape_and_save

def do():
    indexToUrl = {
        1: 'https://www.easynotecards.com/notecard_set/89356',
        # Add more entries if needed
    }
    
    for i in indexToUrl:
        url = indexToUrl[i]
        output_file = f"data/flashcards_{i}.json"  # Ensure output is saved in the 'data' directory
        unit = f"Unit {i}"
        chapter = f"Chapter {i}"
        # Call the correct function with appropriate parameters
        scrape_and_save(url, output_file, unit, chapter, format='json')

if __name__ == "__main__":
    do()
