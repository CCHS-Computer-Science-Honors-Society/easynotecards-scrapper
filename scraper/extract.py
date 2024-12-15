
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def extract_flashcard_data(card, base_url):
    """
    Extracts data from a single flashcard element.

    :param card: A BeautifulSoup element representing a flashcard.
    :param base_url: The base URL to resolve relative image URLs.
    :return: A dictionary containing flashcard data.
    """
    front, options, images, answer = extract_flashcard_contents(card, base_url)
    return {
        'front': front,
        'options': options,
        'back': answer,
        'images': images
    }

def extract_flashcard_contents(card, base_url):
    """
    Extracts the front, options, images, and answer from a flashcard.

    :param card: A BeautifulSoup element representing a flashcard.
    :param base_url: The base URL to resolve relative image URLs.
    :return: A tuple containing front text, options list, images list, and answer text.
    """
    front, options = extract_question_and_options(card)
    images = extract_images(card, base_url)
    answer = extract_answer(card)
    return front, options, images, answer

def extract_question_and_options(card):
    """
    Extracts the question (front) and options from a flashcard.

    :param card: A BeautifulSoup element representing a flashcard.
    :return: A tuple containing front text and a list of options.
    """
    term_div = card.find('div', class_='term')
    if not term_div:
        raise ValueError("Missing 'term' div in flashcard.")

    question_text_div = term_div.find('div', class_='term-text')
    if not question_text_div:
        raise ValueError("Missing 'term-text' div in flashcard.")

    full_text = extract_full_text(question_text_div)
    front, options = parse_front_and_options(full_text)
    return front, options

def extract_full_text(question_text_div):
    """
    Extracts and formats the full text from the question text div.

    :param question_text_div: A BeautifulSoup element containing the question text.
    :return: A formatted string of the question text.
    """
    paragraphs = question_text_div.find_all('p')
    full_text = ''
    for paragraph in paragraphs:
        for br in paragraph.find_all('br'):
            br.replace_with('\n')
        full_text += paragraph.get_text(separator='\n').strip() + '\n'
    return full_text.strip()

def parse_front_and_options(full_text):
    """
    Parses the full text to separate the front (question) and options.

    :param full_text: The complete text extracted from the question.
    :return: A tuple containing the front text and a list of options.
    """
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    front = ""
    options = []
    current_option = ""
    option_labels = ['A)', 'B)', 'C)', 'D)', 'E)']
    contains_image_reference = False

    for line in lines:
        if "SEE IMAGE FOR CHOICES" in line.upper():
            contains_image_reference = True
            break
        if any(line.startswith(label) for label in option_labels):
            if current_option:
                options.append(current_option.strip())
            current_option = line
        else:
            if current_option:
                current_option += " " + line
            else:
                front += line + " "

    if current_option:
        options.append(current_option.strip())

    front = front.strip()

    if contains_image_reference:
        options = ["[See image for choices]"]

    return front, options

def extract_images(card, base_url):
    """
    Extracts image URLs from a flashcard.

    :param card: A BeautifulSoup element representing a flashcard.
    :param base_url: The base URL to resolve relative image URLs.
    :return: A list of absolute image URLs.
    """
    images = []
    image_elements = card.find_all('img', class_='ei')
    for img in image_elements:
        img_src = img.get('src')
        if img_src:
            img_url = resolve_image_url(img_src, base_url)
            images.append(img_url)
    return images

def resolve_image_url(img_src, base_url):
    """
    Resolves relative image URLs to absolute URLs.

    :param img_src: The image source URL (possibly relative).
    :param base_url: The base URL to resolve against.
    :return: An absolute image URL.
    """
    if img_src.startswith('//'):
        return 'https:' + img_src
    elif img_src.startswith('/'):
        parsed_url = urlparse(base_url)
        return urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", img_src)
    elif not img_src.startswith(('http://', 'https://')):
        return urljoin(base_url, img_src)
    return img_src

def extract_answer(card):
    """
    Extracts the answer from a flashcard.

    :param card: A BeautifulSoup element representing a flashcard.
    :return: The answer text.
    """
    def_div = card.find('div', class_='def')
    if not def_div:
        return "No answer found."

    answer_paragraph = def_div.find('p')
    if answer_paragraph:
        answer_text = answer_paragraph.get_text(strip=True)
        _, _, answer = answer_text.partition('Answer:')
        return answer.strip() if answer else "No answer text found."

    return "No answer text found."
