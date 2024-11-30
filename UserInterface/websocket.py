# import http.server
# import socketserver
# import os
# import re

# PORT = 8000
# HTML_FILE = "index.html"
# TEXT_FILE_PATH = "/Users/felicialiu/Desktop/APS360/Project Guidelines/user_interface/test_folder/results.txt"  # Replace with your file path

# # Function to read and return the contents of the text file
# def read_text_file(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             content = file.read()
#             return content
#     except FileNotFoundError:
#         return "The specified file was not found."
#     except Exception as e:
#         return f"Error reading the file: {str(e)}"

# # Function to remove numbers from the string
# def remove_numbers(content):
#     return re.sub(r'\d+', '', content)

# # Write the initial content (from the text file) to the HTML file
# def write_to_html(content):
#     # Remove numbers from the content
#     cleaned_content = remove_numbers(content)

#     print(cleaned_content)

#     # Write to the HTML file
#     with open(HTML_FILE, "w") as file:
#         file.write(f"""
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Dynamic Webpage</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     font-size: 18px;  /* Adjusted font size for body text */
#                 }}
#                 h1 {{
#                     font-size: 24px;  /* Adjusted font size for heading */
#                     color: #333;      /* Heading color */
#                 }}
#             </style>
#         </head>
#         <body>
#             <h1>Ingredients Prediction:</h1>
#             <pre>{cleaned_content}</pre>
#         </body>
#         </html>
#         """)

# # Read the text file and update the HTML
# file_content = read_text_file(TEXT_FILE_PATH)
# write_to_html(file_content)

# # Set up the HTTP server
# class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == "/":
#             self.path = HTML_FILE
#         return super().do_GET()

# # Start the server
# with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
#     print(f"Serving at http://localhost:{PORT}")
#     print("Edit the text file to update the content and refresh the page.")
#     httpd.serve_forever()


# import http.server
# import socketserver
# import os
# import re

# PORT = 8000
# HTML_FILE = "index.html"
# FOLDER_PATH = "/Users/felicialiu/Desktop/APS360/Project/user_interface/test_folder"  # Replace with your folder path

# # Function to read and return the contents of the text file
# def read_text_file(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             content = file.read()
#             return content
#     except FileNotFoundError:
#         return "The specified file was not found."
#     except Exception as e:
#         return f"Error reading the file: {str(e)}"

# # Function to remove numbers from the string
# def remove_numbers(content):
#     return re.sub(r'\d+', '', content)

# # Function to list images in the folder
# def list_images_in_folder(folder_path):
#     images = []
#     for file_name in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, file_name)
#         if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#             images.append(file_name)
#     return images

# # Write the HTML content with images and text file contents
# def write_to_html(content, images):
#     # Remove numbers from the content
#     cleaned_content = remove_numbers(content)

#     # Write to the HTML file
#     with open(HTML_FILE, "w") as file:
#         file.write(f"""
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Dynamic Webpage</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     font-size: 18px;  /* Adjusted font size for body text */
#                 }}
#                 h1 {{
#                     font-size: 24px;  /* Adjusted font size for heading */
#                     color: #333;      /* Heading color */
#                 }}
#                 .image-container {{
#                     margin-bottom: 20px;
#                 }}
#                 .image-container img {{
#                     max-width: 100%; 
#                     height: auto;
#                     margin-bottom: 10px;
#                 }}
#             </style>
#         </head>
#         <body>
#             <h1>Ingredients Prediction:</h1>
            
#             <!-- Display images -->
#             <div class="image-container">
#         """)

#         # Loop through and display images
#         for image in images:
#             file.write(f'<img src="{os.path.join(FOLDER_PATH, image)}" alt="{image}">')

#         # Continue with the rest of the HTML content
#         file.write(f"""
#             </div>
#             <h2>Text File Contents (No Numbers):</h2>
#             <pre>{cleaned_content}</pre>
#         </body>
#         </html>
#         """)

# # List images in the folder
# images_in_folder = list_images_in_folder(FOLDER_PATH)

# # Read the text file and update the HTML
# text_file_path = os.path.join(FOLDER_PATH, "results.txt")  # Assuming the text file is named 'results.txt'
# file_content = read_text_file(text_file_path)

# write_to_html(file_content, images_in_folder)

# # Set up the HTTP server
# class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == "/":
#             self.path = HTML_FILE
#         return super().do_GET()

# # Start the server
# with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
#     print(f"Serving at http://localhost:{PORT}")
#     print("Edit the text file or add new images to the folder and refresh the page.")
#     httpd.serve_forever()



# import http.server
# import socketserver
# import os
# import re

# PORT = 8000
# HTML_FILE = "index.html"
# FOLDER_PATH = "/Users/felicialiu/Desktop/APS360/Project/user_interface/test_folder"  # Replace with your folder path
# STATIC_FOLDER = "static"  # Folder for static content, e.g., images

# # Ensure the static folder exists in the server directory
# os.makedirs(STATIC_FOLDER, exist_ok=True)

# # Function to read and return the contents of the text file
# def read_text_file(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             content = file.read()
#             return content
#     except FileNotFoundError:
#         return "The specified file was not found."
#     except Exception as e:
#         return f"Error reading the file: {str(e)}"

# # Function to remove numbers from the string
# def remove_numbers(content):
#     return re.sub(r'\d+', '', content)

# # Function to list images in the folder
# def list_images_in_folder(folder_path):
#     images = []
#     for file_name in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, file_name)
#         if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#             # Copy images to the static folder for serving
#             static_path = os.path.join(STATIC_FOLDER, file_name)
#             if not os.path.exists(static_path):  # Only copy if not already copied
#                 os.rename(file_path, static_path)
#             images.append(file_name)
#     return images

# # Write the HTML content with images and text file contents
# def write_to_html(content, images):
#     # Remove numbers from the content
#     cleaned_content = remove_numbers(content)

#     # Write to the HTML file
#     with open(HTML_FILE, "w") as file:
#         file.write(f"""
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Dynamic Webpage</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     font-size: 18px;  /* Adjusted font size for body text */
#                 }}
#                 h1 {{
#                     font-size: 24px;  /* Adjusted font size for heading */
#                     color: #333;      /* Heading color */
#                 }}
#                 .image-container {{
#                     margin-bottom: 20px;
#                 }}
#                 .image-container img {{
#                     max-width: 100%; 
#                     height: auto;
#                     margin-bottom: 10px;
#                 }}
#             </style>
#         </head>
#         <body>
#             <h1>FOOD IMAGES:</h1>
            
#             <!-- Display images -->
#             <div class="image-container">
#         """)

#         # Loop through and display images
#         for image in images:
#             file.write(f'<img src="{STATIC_FOLDER}/{image}" alt="{image}">')

#         # Continue with the rest of the HTML content
#         file.write(f"""
#             </div>
#             <h2>INGREDIENT PREDICTIONS:</h2>
#             <pre>{cleaned_content}</pre>
#         </body>
#         </html>
#         """)

# # List images in the folder
# images_in_folder = list_images_in_folder(FOLDER_PATH)

# # Read the text file and update the HTML
# text_file_path = os.path.join(FOLDER_PATH, "results.txt")  # Assuming the text file is named 'results.txt'
# file_content = read_text_file(text_file_path)

# write_to_html(file_content, images_in_folder)

# # Set up the HTTP server
# class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == "/":
#             self.path = HTML_FILE
#         return super().do_GET()

# # Start the server
# with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
#     print(f"Serving at http://localhost:{PORT}")
#     print("Edit the text file or add new images to the folder and refresh the page.")
#     httpd.serve_forever()



import http.server
import socketserver
import os
import re
import signal
import sys

PORT = 8000
HTML_FILE = "index.html"
FOLDER_PATH = "/Users/felicialiu/Desktop/APS360/Project/user_interface"  # Replace with your folder path

# Function to read and return the contents of the text file
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "The specified file was not found."
    except Exception as e:
        return f"Error reading the file: {str(e)}"

# Function to remove numbers from the string
def remove_numbers(content):
    return re.sub(r'\d+', '', content)

# Function to list images in the folder
def list_images_in_folder(folder_path):
    images = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            images.append(file_name)
    return images

# Write the HTML content with images and text file contents
def write_to_html(content, images):
    # Remove numbers from the content
    cleaned_content = remove_numbers(content)

    # Write to the HTML file
    with open(HTML_FILE, "w") as file:
        file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dynamic Webpage</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 18px;  /* Adjusted font size for body text */
                }}
                h1 {{
                    font-size: 24px;  /* Adjusted font size for heading */
                    color: #333;      /* Heading color */
                }}
                .image-container {{
                    margin-bottom: 20px;
                }}
                .image-container img {{
                    max-width: 100%; 
                    height: auto;
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <h1>FOOD IMAGES:</h1>
            
            <!-- Display images -->
            <div class="image-container">
        """)

        # Loop through and display images (use relative paths)
        for image in images:
            file.write(f'<img src="{image}" alt="{image}">')

        # Continue with the rest of the HTML content
        file.write(f"""
            </div>
            <h2>INGREDIENT PREDICTIONS:</h2>
            <pre>{cleaned_content}</pre>
        </body>
        </html>
        """)

# List images in the folder
images_in_folder = list_images_in_folder(FOLDER_PATH)

# Read the text file and update the HTML
text_file_path = os.path.join(FOLDER_PATH, "results.txt")  # Assuming the text file is named 'results.txt'
file_content = read_text_file(text_file_path)

write_to_html(file_content, images_in_folder)

# Set up the HTTP server
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve files from the folder where the server is running
        if self.path == "/":
            self.path = HTML_FILE
        return super().do_GET()

# Gracefully handle server stop (Ctrl + C)
def signal_handler(sig, frame):
    print("\nServer stopped.")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Start the server
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Edit the text file or add new images to the folder and refresh the page.")
    httpd.serve_forever()
