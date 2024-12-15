# scraper/parse.py

from bs4 import BeautifulSoup

def parse_flashcards(html):
    """
    Parses the HTML content to extract flashcard elements.

    :param html: The HTML content of the page.
    :return: A list of BeautifulSoup flashcard elements.
    """
    soup = BeautifulSoup(html, 'html.parser')
    flashcards = soup.find_all('div', class_='vs-card')
    return flashcards
