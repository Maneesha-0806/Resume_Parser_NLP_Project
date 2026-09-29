import spacy
import re
import pymupdf as fitz  # PyMuPDF library for PDF text extraction
import phonenumbers

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                
                # Sort blocks primarily by their Y-coordinate (top to bottom)
                # and secondarily by X-coordinate (left to right)
                # block[1] = top edge, block[0] = left edge
                blocks.sort(key=lambda b: (b[1], b[0]))
                
                for block in blocks:
                    # block[6] == 0 ensures we only grab text blocks, ignoring images
                    if block[6] == 0: 
                        text += block[4] + "\n" 
    except Exception as e:
        print(f"Error: {e}")
        
    # Clean up excess blank lines
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def parse_resume(text):
    """Extracts Name, Email, Phone, and Skills from the raw text."""
    # 1. Load the pre-trained NLP model
    nlp = spacy.load("en_core_web_sm")
    
    # 2. Inject custom rules for detecting tech skills
    # We use an EntityRuler to teach spaCy new specific keywords
    if "entity_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("entity_ruler", before="ner")
        # You can expand this list based on the job requirements
        skills_database = ["Python", "Machine Learning", "NLP", "Java", "SQL", 
                           "Data Analysis", "C++", "AWS", "Docker", "React"]
        
        patterns = [{"label": "SKILL", "pattern": skill} for skill in skills_database]
        ruler.add_patterns(patterns)

    # Process the text through the NLP pipeline
    doc = nlp(text)

    # 3. Extract Name (Smarter Line-by-Line Approach)
    name = None
    # Split the text into individual lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Check the first 10 lines
    for line in lines[:10]:
        # Skip common generic headers
        if line.lower() in ["resume", "curriculum vitae", "cv"]:
            continue
            
        # Ask spaCy if this specific line contains a person
        doc_line = nlp(line)
        for ent in doc_line.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                break
        
        if name:
            break
            
    # FALLBACK: If spaCy misses it, grab the first clean line 
    if not name:
        for line in lines[:5]:
            # Check for 2-4 words, no numbers, no emails
            if 1 < len(line.split()) <= 4 and not re.search(r'\d', line) and "@" not in line:
                # Ignore common headers
                if line.lower() not in ["resume", "curriculum vitae", "cv", "education", "technical skills"]:
                    name = line
                    break

    # 4. Extract Email using Regex
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email_match = re.search(email_pattern, text)
    email = email_match.group(0) if email_match else None

    # 5. Extract Phone Number using phonenumbers (UPDATED)
    phone = None
    # "IN" sets the fallback region to India if the number lacks a '+' country code.
    # Change this to "US", "GB", etc., based on where your primary applicants are from.
    matches = phonenumbers.PhoneNumberMatcher(text, "IN")     
    for match in matches:
        # Formats the extracted number to a clean, standardized international format
        phone = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        break # We stop after finding the first valid phone number in the resume

    # 6. Extract Skills (Using the custom SKILL entities we defined earlier)
    found_skills = set(ent.text for ent in doc.ents if ent.label_ == "SKILL")

    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Skills": list(found_skills)
    }

if __name__ == "__main__":
    # Provide the path to a sample PDF resume
    pdf_path = "C:\\Users\\manee\\Downloads\\Maneesha_CA_Resume_Tech.pdf" 
    
    print(f"Reading {pdf_path}...")
    raw_text = extract_text_from_pdf(pdf_path)
    
    if raw_text.strip():
        print("\nParsing information...\n")
        extracted_data = parse_resume(raw_text)
        
        # Print the results cleanly
        for key, value in extracted_data.items():
            print(f"{key}: {value}")
    else:
        print("No text could be extracted from the PDF.")