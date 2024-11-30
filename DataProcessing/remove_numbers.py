import os
import re

def remove_numbers_from_text(content):
    """Remove all numbers from the text content."""
    return re.sub(r'\d+', '', content)

def process_text_file(file_path):
    """Reads a file, removes numbers, and writes the updated content back to the file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Remove numbers from the content
        cleaned_content = remove_numbers_from_text(content)

        with open(file_path, 'w') as file:
            file.write(cleaned_content)
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {str(e)}")

def process_folder(folder_path):
    """Recursively goes through the folder and processes each text file."""
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # Check if the file is a text file (based on file extension)
            if file_name.lower().endswith('.txt'):
                file_path = os.path.join(root, file_name)
                process_text_file(file_path)

if __name__ == "__main__":
    folder_path = input("Enter the folder path to process: ")
    if os.path.exists(folder_path):
        process_folder(folder_path)
        print("All text files have been processed.")
    else:
        print(f"The folder path {folder_path} does not exist.")
