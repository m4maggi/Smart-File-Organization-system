import os
from dotenv import load_dotenv
import google.generativeai as genai
import ast
from PyPDF2 import PdfReader
from docx import Document

# Load environment variables from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="You are a file organization system. You get files as input. You read the content of the file and return a category name as output such as letters, college mails, Subject notes, banking documents, etc."
)

#directory_path = "C:/Users/megha/Desktop/Sample files - Copy/Documents"
initial_categories = []


def extract_text(filepath):
    """Extracts text from the first 3 pages or lines of a file."""
    text = ""
    if filepath.endswith('.pdf'):
        try:
            reader = PdfReader(filepath)
            for page in reader.pages[:3]:  # First 3 pages
                text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF file {filepath}: {e}")
    elif filepath.endswith('.docx'):
        try:
            doc = Document(filepath)
            for paragraph in doc.paragraphs[:100]:  # First 100 lines
                text += paragraph.text
        except Exception as e:
            print(f"Error reading DOCX file {filepath}: {e}")
    elif filepath.endswith('.txt'):
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()[:100]  # First 100 lines
                text += "".join(lines)
        except Exception as e:
            print(f"Error reading TXT file {filepath}: {e}")
    return text.strip()

def sort_doc(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(('.pdf', '.txt', '.docx')):  # Supported file types
            filepath = os.path.join(directory_path, filename)
            content_excerpt = extract_text(filepath)
            if not content_excerpt:
                category = "unidentified"
            else:
                # Generate category based on extracted text
                result = model.generate_content([
                    content_excerpt,
                    "\n\n",
                    '''1) Just read the document until wherever you want so that you could identify what is there inside the doc.
                    2) Return a category name (in 1-2 words) so that the document will be sorted into that category directory.
                    3) If you cannot process the content of the document, then return as unidentified.
                    4) Do not return any other things (it has to be a category name or else unidentified).'''
                ])
                category = result.text.strip()
            initial_categories.append(category)
            print(f"Processed {filename}: {category}")

    print(initial_categories)

    # Deduplicate and clean categories
    while 1:
        try:
            response = model.generate_content(f'read all these categories, remove duplicates or make similar categories into a same name category. Rename the names if necessary.just return a python list of category names. Any other text is not required: {', '.join(initial_categories)}.')
            # Use ast.literal_eval to safely convert the string to a list
            final_categories = ast.literal_eval(response.text)    
        except Exception:
            continue
        break

    #print(response)

    #Use ast.literal_eval to safely convert the string to a list
    final_categories = ast.literal_eval(response.text)

    print("Final responses :",final_categories)

    # Sorting docs into those categories
    categorized_documents = {}
    for filename in os.listdir(directory_path):
        if filename.endswith(('.pdf', '.txt', '.docx')):
            print("...")
            filepath = os.path.join(directory_path, filename)
            content_excerpt = extract_text(filepath)
            if not content_excerpt:
                category = "unidentified"
            else:
                # Get the category for the document
                result = model.generate_content(
                    [
                        content_excerpt,
                        "\n\n",
                        "Select one category name for the document from the given list only. Just return the category name: " + ', '.join(final_categories),
                    ]
                )
                best_category = result.text.strip()
            
            # Handle case where the category directory doesn't exist
            category_path = os.path.join(directory_path, best_category)
            os.makedirs(category_path, exist_ok=True)  # Create directory if it doesn't exist

            # Move the file to its category directory
            destination_path = os.path.join(category_path, filename)
            os.rename(filepath, destination_path)
            
            # Add to categorized documents dictionary
            if best_category not in categorized_documents:
                categorized_documents[best_category] = []
            categorized_documents[best_category].append(filepath)

    print("Categorization complete.")

