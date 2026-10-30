# Resume Parser

A Python script that extracts basic information from a PDF resume using PyMuPDF and spaCy.

## Features

- Extracts text from PDF pages while preserving block order.
- Detects a candidate name from the first few lines.
- Extracts an email address with regular expressions.
- Detects phone numbers from various countries and formats the first valid match internationally.
- Identifies configured technical skills with spaCy's `EntityRuler`.

## Requirements

- Python 3.9 or newer
- A text-based PDF resume
- The spaCy English model `en_core_web_sm`

Install the Python packages:

```bash
pip install spacy pymupdf phonenumbers
```

Download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Open `resume_parser.py`.
2. Update the `pdf_path` value near the bottom of the file to point to your resume:

```python
pdf_path = r"C:\path\to\your\resume.pdf"
```

3. Run the script:

```bash
python resume_parser.py
```

The script prints the extracted name, email, phone number, and skills. For example:

```text
Name: MANEESHA C A
Email: maneeshaca08@gmail.com
Phone: +91 86107 13062
Skills: ['Machine Learning', 'Python', 'Java']
```

## Supported Skills

The default skill list includes:

- Python
- Machine Learning
- NLP
- Java
- SQL
- Data Analysis
- C++
- AWS
- Docker
- React

To recognize additional skills, add them to `skills_database` in `parse_resume()`.

## Limitations

- Scanned or image-only PDFs may produce little or no text without OCR.
- Phone detection supports international numbers through the `phonenumbers` library. Numbers without a country code use India (`IN`) as the fallback region; change this in `parse_resume()` if needed.
- Name detection depends on spaCy's model and fallback heuristics.
- Skills are limited to the entries configured in `skills_database`.
- The current script processes one PDF path configured in the source code.

## Project Structure

```text
.
├── README.md
└── resume_parser.py
```
