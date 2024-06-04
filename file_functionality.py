import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text=''
            for page in pdf_reader.pages:
                text+=page.extractText()
            return text

        except Exception as e:
            raise Exception("erroe reading the PDF file")

    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception("file type not supported")




def get_table_data(quiz_str):
    try:
        if not quiz_str.strip():  # Check if the string is not empty
            raise ValueError("Empty JSON string")

        # Print the quiz_str to debug its content
        print("Received JSON string for parsing:")
        print(quiz_str)

        quiz_dict = json.loads(quiz_str)

        # Since the structure is not a list of questions but a dictionary with keys as question numbers,
        # we need to iterate over the dictionary values
        quiz_table_data = []

        for key, item in quiz_dict.items():
            mcq = item.get('mcq', 'No question provided')
            options = ' | '.join([f"{opt_key}: {opt_value}" for opt_key, opt_value in item.get("options", {}).items()])
            correct = item.get('correct', 'No answer provided')
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        
        return quiz_table_data
    
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"Error processing quiz data: {e}")
        traceback.print_exc()
        return None