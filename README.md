````markdown
# EasyNoteCards Flashcard Scraper

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [JSON Output Structure](#json-output-structure)
- [Handling Multi-line Options](#handling-multi-line-options)
- [Image Extraction](#image-extraction)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Welcome to the **EasyNoteCards Flashcard Scraper**! This Python-based tool is designed to streamline the extraction of flashcard data from [EasyNoteCards](https://www.easynotecards.com/) for use in OpenCourseWare (OCW) projects. Whether you're creating study materials, integrating with learning management systems, or conducting academic research, this scraper provides a reliable and efficient solution to gather structured flashcard data.

## Features

- **Accurate Data Extraction**: Captures the front (question), options (A-E), and back (answer) of each flashcard.
- **Multi-line Option Handling**: Effectively groups multi-line options to ensure data integrity.
- **Image Extraction**: Retrieves all images within flashcards that have the class `ei`.
- **Metadata Inclusion**: Allows users to specify and include `unit` and `chapter` information for each flashcard.
- **Flexible Output**: Saves the scraped data in a well-structured JSON format.
- **User-Friendly Interface**: Utilizes command-line arguments for easy customization.
- **Robust Error Handling**: Skips flashcards with missing or malformed elements while providing informative logs.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.11 or higher**: [Download Python](https://www.python.org/downloads/)
- **UV package manager**: [Download UV](https://github.com/astral-sh/uv)
- **Internet Connection**: Required to access the EasyNoteCards website and download images.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/easynotecards-scraper.git
   cd easynotecards-scraper
   ```
````

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   uv venv
   ```

3. **Install Required Libraries**

   ```bash
   uv pip install
   ```

   _If you don't have a `requirements.txt`, you can install the dependencies directly:_

   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

The scraper is executed via the command line. Below are the steps and examples to run the script effectively.

### Basic Syntax

```bash
python scrape_easynotecards.py <URL> --unit <UNIT_NAME> --chapter <CHAPTER_NAME> [--output <OUTPUT_FILE.json>]
```

### Parameters

- `<URL>`: **(Required)** The URL of the EasyNoteCards page you want to scrape.
- `--unit` or `-u`: **(Required)** The unit name to associate with the flashcards.
- `--chapter` or `-c`: **(Required)** The chapter name to associate with the flashcards.
- `--output` or `-o`: **(Optional)** The name of the output JSON file. Defaults to `flashcards.json` if not provided.

### Examples

1. **Basic Usage**

   ```bash
   python scrape_easynotecards.py https://www.easynotecards.com/abc123 --unit "Biology" --chapter "Cell Biology"
   ```

   _This will save the output to `flashcards.json`._

2. **Specify Output File**

   ```bash
   python scrape_easynotecards.py https://www.easynotecards.com/abc123 --unit "Biology" --chapter "Cell Biology" --output biology_flashcards.json
   ```

3. **Using Short Flags**

   ```bash
   python scrape_easynotecards.py https://www.easynotecards.com/abc123 -u "Chemistry" -c "Organic Chemistry" -o chem_flashcards.json
   ```

## JSON Output Structure

The scraper outputs data in a structured JSON format, making it easy to integrate with other applications or for further analysis.

### Sample JSON Output

```json
[
  {
    "front": "A localized group of organisms that belong to the same species is called a",
    "options": [
      "A) biosystem",
      "B) community",
      "C) population",
      "D) ecosystem",
      "E) family"
    ],
    "back": "C",
    "unit": "Biology",
    "chapter": "Cell Biology",
    "images": [
      "https://www.easynotecards.com/images/example1.jpg",
      "https://www.easynotecards.com/images/example2.png"
    ]
  },
  {
    "front": "Another complex question that spans multiple lines and includes details such as A) which should not be confused with option A).",
    "options": [
      "A) The temperature decreased from 20°C to 15°C.",
      "B) The plant's height is 25 centimeters (cm).",
      "C) The fish swam in a zigzag motion.",
      "D) The six pairs of robins hatched an average of three chicks.",
      "E) The contents of the stomach are mixed every 20 seconds."
    ],
    "back": "C",
    "unit": "Biology",
    "chapter": "Cell Biology",
    "images": []
  }
  // ... more flashcards
]
```

### Field Descriptions

- **`front`**: _String_ - The question text.
- **`options`**: _Array of Strings_ - Multiple-choice options labeled from A) to E).
- **`back`**: _String_ - The correct answer (e.g., "C").
- **`unit`**: _String_ - The unit name provided by the user.
- **`chapter`**: _String_ - The chapter name provided by the user.
- **`images`**: _Array of Strings_ - URLs of images associated with the flashcard. This array will be empty if no images with class `ei` are found.

## Handling Multi-line Options

The scraper is designed to handle scenarios where options span multiple lines, ensuring each option is correctly grouped and captured.

### Example Scenario

**Problem**: Multi-line options are being split incorrectly, causing parts of the question to appear in the options array.

**Solution**: The script now detects the start of options by identifying lines that begin with "A)", "B)", etc., and groups subsequent lines accordingly.

### How It Works

1. **Option Detection**: The script scans each line of the flashcard content. When it encounters a line starting with "A)", it marks the beginning of options.
2. **Grouping**: All lines following "A)" that start with "B)", "C)", etc., are treated as separate options. Lines that do not start with an option label are considered continuations of the current option.
3. **Aggregation**: Multi-line options are concatenated into single entries within the options array.

### Benefits

- **Data Integrity**: Ensures that questions and options are distinctly separated, even when options span multiple lines.
- **Flexibility**: Adapts to various formatting styles used in flashcards.

## Image Extraction

The scraper not only extracts textual data but also retrieves all images associated with each flashcard that have the class `ei`.

### How It Works

1. **Image Detection**: Searches for all `<img>` tags within a flashcard that have the class `ei`.
2. **URL Resolution**: Converts relative image URLs to absolute URLs to ensure they can be accessed independently.
3. **Inclusion in JSON**: Adds an `images` array to each flashcard entry containing the URLs of the extracted images.

### Example

```json
"images": [
    "https://www.easynotecards.com/images/example1.jpg",
    "https://www.easynotecards.com/images/example2.png"
]
```

## Troubleshooting

If you encounter any issues while using the scraper, consider the following solutions:

### 1. **No Flashcards Found**

**Symptom**: The script outputs "No flashcards found on the page."

**Solution**:

- **Verify URL**: Ensure that the provided URL is correct and points to a valid EasyNoteCards page.
- **Check HTML Structure**: Use your browser's developer tools to inspect the flashcard elements and confirm that they are contained within `<div>` tags with the class `vs-card`.

### 2. **Empty Options Array**

**Symptom**: The `options` array in the JSON output is empty.

**Solution**:

- **HTML Structure Changes**: The website's HTML structure might have changed. Inspect the flashcard's HTML to ensure that options are still separated by `<br>` tags and start with labels like "A)", "B)", etc.
- **Multi-line Options**: Ensure that the script is correctly grouping multi-line options. Refer to the [Handling Multi-line Options](#handling-multi-line-options) section.

### 3. **Images Not Extracted**

**Symptom**: The `images` array is empty even though images are present in the flashcards.

**Solution**:

- **Class Name Verification**: Ensure that images have the class `ei`. If the class name has changed, update the script accordingly.
- **Relative URLs**: Verify that image URLs are being correctly resolved to absolute URLs. If not, inspect the `src` attributes and adjust the URL resolution logic in the script.

### 4. **Permission Issues**

**Symptom**: `Permission denied` errors when trying to write the JSON file.

**Solution**:

- **File Permissions**: Ensure that you have write permissions in the directory where you're running the script.
- **File in Use**: Make sure the output file is not open in another program.

### 5. **Python Errors**

**Symptom**: Python raises syntax or runtime errors.

**Solution**:

- **Dependencies**: Ensure all required libraries are installed. Run `pip install -r requirements.txt` to install missing packages.
- **Python Version**: Confirm that you're using Python 3.6 or higher.
- **Script Updates**: If you've modified the script, double-check for any syntax errors or unintended changes.

## Contributing

Contributions are welcome! If you'd like to enhance the scraper or fix bugs, please follow these steps:

1. **Fork the Repository**

   Click the "Fork" button at the top right of the repository page to create your own fork.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/easynotecards-scraper.git
   cd easynotecards-scraper
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

   Implement your enhancements or bug fixes.

5. **Commit Your Changes**

   ```bash
   git commit -m "Add feature: YourFeatureDescription"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**

   Navigate to the original repository and click on "New Pull Request" to propose your changes.

### Guidelines

- **Code Quality**: Ensure your code follows Python best practices and is well-documented.
- **Testing**: Test your changes thoroughly to prevent introducing bugs.
- **Documentation**: Update the `README.md` if your changes affect usage or add new features.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software, provided you include the original license and copyright.

## Contact

For any questions, suggestions, or feedback, please reach out:

- **Author**: [Your Name](https://github.com/yourusername)
- **Email**: [your.email@example.com](mailto:your.email@example.com)
- **GitHub**: [https://github.com/yourusername/easynotecards-scraper](https://github.com/yourusername/easynotecards-scraper)

---

_Happy Scraping! 🚀_

```

```
