import argparse
from scraper.core import scrape_and_save

def main():
    parser = argparse.ArgumentParser(description="Scrape EasyNoteCards and save to JSON or CSV.")
    parser.add_argument('url', help='URL of the EasyNoteCards page to scrape.')
    parser.add_argument('-o', '--output', default='data/flashcards.json', help='Output file path.')
    parser.add_argument('-u', '--unit', default='', help='Unit name to associate with the flashcards.')
    parser.add_argument('-c', '--chapter', default='', help='Chapter name to associate with the flashcards.')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json', help='Output format: json or csv.')

    args = parser.parse_args()

    scrape_and_save(
        url=args.url,
        output_file=args.output,
        unit=args.unit,
        chapter=args.chapter,
        format=args.format
    )

if __name__ == '__main__':
    main()
