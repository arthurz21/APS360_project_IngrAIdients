import json
import os
from collections import Counter
import requests

# Load the data from the JSON file
with open('recipes_with_nutritional_info.json') as f1:
    layer1_data = json.load(f1)

with open('layer2+.json') as f2:
    layer2_data = json.load(f2)

# Create a dictionary from layer2_data for efficient lookup
layer2_dict = {item["id"]for item in layer2_data}

# Create the output directory if it doesn't exist
output_dir = 'labels_folder'
os.makedirs(output_dir, exist_ok=True)

ingredients_counter = Counter()

# Iterate over the recipes and write the ingredients to files
for recipe in layer1_data:
    recipe_id = recipe['id']

    if recipe_id not in layer2_dict:
        continue
    ingredients = recipe.get('ingredients', [])
    seen_ingredients = set()

    # Open a file with the recipe ID as the filename
    with open(os.path.join(output_dir, f'{recipe_id}.txt'), 'w') as file:
        for ingredient in ingredients:
            ingredient_text = ingredient["text"]
            if ingredient_text.startswith("spices,"):
                # Handle the special case for "spices"
                first_part = ingredient_text.split(',', 1)[1].strip()
            elif ingredient_text.startswith("fish,"):
                # Handle the special case for "fish"
                first_part = ingredient_text.split(',', 1)[1].strip()
            else:
                first_part = ingredient_text.split(',', 1)[0].strip()

            final_ingredient = first_part.split(',', 1)[0].strip()

            if final_ingredient not in seen_ingredients:
                seen_ingredients.add(final_ingredient)
                file.write(final_ingredient + '\n')
                ingredients_counter[final_ingredient] += 1  # Update the counter here

# Create the output file for unique ingredients
output_file = 'unique_ingredients2.txt'
with open(output_file, 'w') as file:
    # Write the total number of unique ingredients
    file.write(f"{len(ingredients_counter)}\n")
    # Write each unique ingredient and its count in alphabetical order
    for ingredient, count in sorted(ingredients_counter.items()):
        file.write(f"{ingredient} ({count})\n")


# Base URL for image download
base_url = "http://wednesday.csail.mit.edu/temporal/release/recipe1M+_images/"

# Create the output directory if it doesn't exist
output_dir = 'image_folder'
os.makedirs(output_dir, exist_ok=True)
layer2_dict = {item["id"]: item for item in layer2_data}


for recipe in layer1_data:
    recipe_id = recipe['id']

    if recipe_id not in layer2_dict:
        continue

    recipe_dir = os.path.join(output_dir, recipe_id)
    # Check if the folder already exists
    if os.path.exists(recipe_dir):
        print(f"Skipping {recipe_id}, folder already exists.")
        continue

    os.makedirs(recipe_dir, exist_ok=True)

    images = layer2_dict[recipe_id].get("images", [])

    for image_id in images:
        # Construct the image URL
        a = image_id["id"]
        sub_path = a[0]+"/"+a[1]+"/"+a[2]+"/"+a[3]  # First four characters as sub-path
        image_url = f"{base_url}{sub_path}/{a}"

        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save the image to the subfolder
            image_path = os.path.join(recipe_dir, f"{a}.jpg")
            with open(image_path, 'wb') as img_file:
                img_file.write(response.content)
        else:
            print(f"Failed to download {image_url}")

