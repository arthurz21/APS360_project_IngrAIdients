
#################################################
# IMPORTS
#################################################

import re
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import string
from collections import defaultdict
import matplotlib.ticker as ticker




#################################################
# FUNCTIONS
#################################################

# takes in a text string (e.g. "yogurt, greek, plain, nonfat") and returns a
# concatenated ingredient name (e.g. greek yogurt)
def ingredient_identifier(string):

    # remove brackets in strings
    cleaned_string = re.sub(r'\[.*?\]|\(.*?\)|\{.*?\}', '', string)

    # divide, clean, and retain only the first two elements
    parts = cleaned_string.split(",")
    parts = [part.strip() for part in parts]

    # assign preliminary ingredient name with some exclusions and clean
    if len(parts) > 1 and parts[1] not in "fluid raw prepared yellow white plain" and "upc" not in parts[1]:
        if parts[0] not in "nuts spices fish seeds candies denny's snacks salad dressing leavening agents":
            ingredient = parts[1]+" "+parts[0]
        else:
            ingredient = parts[1]
    else:
        ingredient = parts[0]
    ingredient = ingredient.strip()

    # implementing a bunch of very specific parsing based on observations
    if ingredient == "all purpose cajun seasoning a cajun life":
        ingredient = "all purpose cajun seasoning"
    if ingredient == "broilers or fryers chicken":
        ingredient = "broiler or fryers chicken"
    if ingredient == "bacon grease animal fat":
        ingredient = "bacon grease"
    if ingredient == "catsup":
        ingredient = "ketchup"
    if ingredient == "coconut  and or palm kernel shortening confectionery":
        ingredient = "coconut or palm shortening"
    if ingredient == "coleslaw fast foods":
        ingredient = "coleslaw"
    if ingredient == "nestle":
        ingredient = "nestle candies"
    if ingredient == "gerolsteiner brunnen gmbh & co. kg beverages":
        ingredient = "sparkling mineral water"
    if ingredient == "herbal extract powder from stevia leaf sweetener":
        ingredient = "stevia leaf sweetener"
    if ingredient == "mars snackfood us baking chocolate ":
        ingredient = "baking chocolate"
    if ingredient == "martha white's buttermilk biscuit mix martha white foods":
        ingredient = "buttermilk biscuit mix"
    if ingredient == "mascarpone cheese il villaggio":
        ingredient = "mascarpone cheese"
    if ingredient == "organic bitter-sweet dark chocolate chips pascha":
        ingredient = "bitter-sweet dark chocolate chips"
    if ingredient == "organic chipotle dried chile peppers terra dolce ":
        ingredient = "dried chile peppers"
    if ingredient == "palm sugar cock brand":
        ingredient = "palm sugar"
    if ingredient == "pizza dough house of pasta":
        ingredient = "pizza dough"
    if ingredient == "protein powder whey based beverages":
        ingredient = "protein powder"
    if ingredient == "real semi-sweet chocolate baking chips spartan":
        ingredient = "semi-sweet chocolate baking chips"
    if ingredient == "seasoned rice wine vinegar roland":
        ingredient = "seasoned rice wine vinegar"
    if ingredient == "soy sauce made from soy":
        ingredient = "soy sauce"
    if ingredient == "spicy buffalo sauce mcdonald's":
        ingredient = "spicy buffalo sauce"
    if ingredient == "steak seasoning la flor":
        ingredient = "steak seasoning"
    if "creams" in ingredient:
        ingredient = ingredient.replace("creams", "cream")
    if "ready-to-eat" in ingredient:
        ingredient = ingredient.replace("ready-to-eat", "")
    if ingredient == "swanson chicken broth 99% fat free soup":
        ingredient = "chicken broth"
    if ingredient == "tapioca starch amazonas rainforest product":
        ingredient = "tapioca starch"
    if ingredient == "tequila sunrise alcoholic beverage":
        ingredient = "tequila"
    if ingredient == "without salt butter":
        ingredient = "unsalted butter"
    if ingredient == "margarine-butter blend margarine-like":
        ingredient = "margarine"
    if ingredient == "regular margarine":
        ingredient = "margarine"

    # clean once more and return
    return ingredient.strip()


# parses through the full json and returns a dictionary with ID keys and
# values are lists with unique ingredients that have been cleaned
def parse_ingredients(json_file):

    # open and extract data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # storing the results in this dictionary
    results = {}

    # for each recipe/entry, get its ingredient list
    for entry in data:
        recipe_id = entry.get("id", "NO_ID")
        ingredients = [ingredient_identifier(item["text"]) for item in entry.get("ingredients", [])]
        results[recipe_id] = list(set(ingredients))

    return results


# generates top 10 bot 10 ingredient counts, full alphabetical ingredient list with counts
# and a bar plot with alphabetical entries and corressponding counts
def generate_ingredient_report(ingredients_dict, modifier=""):
    print("plotting...")

    # dictionary to store ingredient counts by ingredient name
    ingredient_counts = defaultdict(int)
    for ingredient_list in ingredients_dict.values():
        for ingredient in ingredient_list:
            key = ingredient.lower()
            ingredient_counts[key] += 1

    # sort ingredients alphabetically for the main list
    sorted_ingredients = sorted(ingredient_counts.items())
    # sort ingredients by their counts in descending order for top/bottom lists
    sorted_by_count = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)

    # write the TEXT document output
    with open(modifier+"list_ingredients.txt", "w") as f:
        # total count
        f.write(f"Total # Unique Ingredients: {len(sorted_ingredients)}\n\n")
        # full list of ingredients (alphabetically sorted)
        for ingredient, count in sorted_ingredients:
            f.write(f"{ingredient} ({count})\n")
        # top 10 most common ingredients (sorted by count)
        f.write("\nTop 10 Most Common Ingredients:\n")
        top_10 = sorted_by_count[:10]
        for ingredient, count in top_10:
            f.write(f"{ingredient} ({count})\n")
        # bottom 10 least common ingredients (sorted by count)
        f.write("\nTop 10 Least Common Ingredients:\n")
        bottom_10 = sorted_by_count[-10:]
        for ingredient, count in bottom_10:
            f.write(f"{ingredient} ({count})\n")

    # setup for the histogram plotting, ingredients and colour bars
    fig, ax = plt.subplots(figsize=(12, 6))
    all_letters = list(string.ascii_uppercase)
    unique_ingredients = sorted(ingredient_counts.keys())
    ingredient_colors = {name: plt.get_cmap('tab20')(i % 20) for i, name in enumerate(unique_ingredients)}

    # letterwise mapping ingredient names to counts 
    letter_groups = defaultdict(lambda: defaultdict(int))
    for ingredient, count in ingredient_counts.items():
        first_letter = ingredient[0].upper()
        letter_groups[first_letter][ingredient] += count
    
    # track bottom positions for stacking
    bottom = np.zeros(len(all_letters))
    for ingredient, color in ingredient_colors.items():
        heights = [letter_groups[letter][ingredient] for letter in all_letters]
        ax.bar(all_letters, heights, bottom=bottom, color=color, label=ingredient if any(heights) else "")
        bottom += np.array(heights)

    # lab and format
    ax.set_xlabel("Ingredient Names (first letter)")
    ax.set_ylabel("# Occurrences Across Recipes")
    ax.set_title("Ingredient Distribution Across All Recipes")
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    handles, labels = ax.get_legend_handles_labels()
    filtered_handles_labels = [(h, l) for h, l in zip(handles, labels) if l]
    
    # save plot and end
    plt.savefig(modifier+"ingredient_distribution_stacked.png", bbox_inches='tight')
    plt.close()

    print("done plotting.")
    return


# this is to filter out while we're writing the files to make sure only recipes with ingredient
# lists and at least one image are used
def extract_valid_ids_into_set(valid_ids_file):
    valid_ids = set() 
    with open(valid_ids_file, "r") as f:
        for line in f:
            id_str = line.strip() 
            if id_str: valid_ids.add(id_str)
    return valid_ids


# for each valid file ID, write that ingredient list of data to a TXT file call ID.txt
def write_all_files(ingredients_dict, valid_ids, main_folder):
    os.makedirs(main_folder, exist_ok=True)
    for key_id, ingredients in ingredients_dict.items():
        if key_id in valid_ids:
            file_path = os.path.join(main_folder, f"{key_id}.txt")
            with open(file_path, "w") as f:
                for ingredient in ingredients:
                    f.write(f"{ingredient}\n")
    return


def make_valid(ingredients_dict, valid_ids_file):
    new_dict = {}
    for key_id, ingredients in ingredients_dict.items():
        if key_id in valid_ids:
            new_dict[key_id] = ingredients
    return new_dict


def analyze_ingredients(ingredients_dict, modifier=""):
    # count the number of ingredients for each recipe
    ingredients_count = [len(ingredients) for ingredients in ingredients_dict.values()]
    # calculate statistics
    total_recipes = len(ingredients_count)
    avg_ingredients = sum(ingredients_count) / total_recipes if total_recipes > 0 else 0
    min_ingredients = min(ingredients_count) if ingredients_count else 0
    max_ingredients = max(ingredients_count) if ingredients_count else 0
    # find shortest and longest
    shortest_recipe_id = min(ingredients_dict.keys(), key=lambda k: len(ingredients_dict[k]))
    longest_recipe_id = max(ingredients_dict.keys(), key=lambda k: len(ingredients_dict[k]))
    shortest_recipe = ingredients_dict[shortest_recipe_id]
    longest_recipe = ingredients_dict[longest_recipe_id]
    
    # PRINT GENERAL STATS
    print(f"Total Recipes: {total_recipes}")
    print(f"Average Ingredients per Recipe: {avg_ingredients:.2f}")
    print(f"Shortest Recipe Length [{len(shortest_recipe)}] (ID: {shortest_recipe_id}): {shortest_recipe}")
    print(f"Longest Recipe Length [{len(longest_recipe)}] (ID: {longest_recipe_id}): {longest_recipe}")
    
    # plotting the distribution of ingredients per recipe
    ingredient_freq = [0] * (max_ingredients + 1)
    for count in ingredients_count:
        ingredient_freq[count] += 1
    x_positions = range(1, max_ingredients + 1)
    colors = plt.cm.viridis(np.linspace(0, 1, len(x_positions)))
    bar_width = 0.8
    plt.bar(x_positions, ingredient_freq[1:], width=bar_width, color=colors[:max_ingredients], alpha=0.8)

    # Customize the plot
    plt.title('Distribution of # Ingredients in Each Recipe')
    plt.xlabel('# Ingredients')
    plt.ylabel('# Recipes')
    plt.xticks(x_positions)
    plt.grid(axis='y', alpha=0.25)

    plt.savefig(modifier+"number_dist.png")
    plt.close()


def read_all_files(main_folder):
    ingredients_dict = {}
    
    # iterate through all files in the specified folder
    for filename in os.listdir(main_folder):
        if filename.endswith(".txt"):  # Ensure we only process .txt files
            key_id = filename[:-4]  # Remove the .txt extension to get the key
            file_path = os.path.join(main_folder, filename)
            
            # read the ingredients from the file
            with open(file_path, "r") as f:
                ingredients = [line.strip() for line in f.readlines() if line.strip()]  # Read non-empty lines
            
            # store the ingredients in the dictionary
            ingredients_dict[key_id] = ingredients
    
    return ingredients_dict


#################################################
# MAIN
#################################################



json_file = "/Users/felicialiu/Desktop/APS360/Project Guidelines/dev/recipes_with_nutritional_info.json"
valid_ids_file = "/Users/felicialiu/Desktop/APS360/Project Guidelines/dev/valid_recipe_ids.txt"
main_folder = "/Users/felicialiu/Desktop/APS360/Project Guidelines/new_unsplit/default"

ingredients_dict = parse_ingredients(json_file)
valid_ids = extract_valid_ids_into_set(valid_ids_file)

ingredients_dict = make_valid(ingredients_dict, valid_ids_file)

# for key_id, ingredients in ingredients_dict.items():
#     if len(ingredients) == 1:
#         print(key_id, ":", ingredients)

generate_ingredient_report(ingredients_dict)
analyze_ingredients(ingredients_dict)


# print(len(valid_ids), len(ingredients_dict.keys()))

write_all_files(ingredients_dict, valid_ids, main_folder)



# modi = "test"
# main_folder = '/Users/felicialiu/Desktop/APS360/Project Guidelines/LABELS/{}'.format(modi)
# ingredients_dict = read_all_files(main_folder)
# generate_ingredient_report(ingredients_dict, modi)
# analyze_ingredients(ingredients_dict, modi)