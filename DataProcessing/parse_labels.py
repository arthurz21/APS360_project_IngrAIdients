
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
from collections import Counter, defaultdict
import math


#################################################
# FORM AND EDITING THE DICTIONARY
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

    # ingredient = parts[0]

    # clean once more and return
    return ingredient.strip()


# for the webscraped version it's already cleaned
def ingredient_identifier_web(string):
    # clean once more and return
    string = re.sub(r'\d+', '', string)
    string = re.sub(r'\(.*?\)|/|\d+', '', string).strip()
    string = re.sub(r'\(.*?\)|/|\d+|-', '', string)
    
    # Replace 'arlic' with 'garlic'
    string = string.replace('garlic', 'arlic')
    string = string.replace('arlic', 'garlic')
    return string.strip()


# parses through the full json and returns a dictionary with ID keys and
# values are lists with unique ingredients that have been cleaned
def parse_ingredients(json_file, webscraped=False):

    # open and extract data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # storing the results in this dictionary
    results = {}

    count  = 0

    # for each recipe/entry, get its ingredient list
    for entry in data:
        # recipe_id = entry.get("id", "NO_ID")
        # if webscraped:
        #     ingredients = [ingredient_identifier_web(item["text"]) for item in entry.get("ingredients", [])]
        # else:
        #     ingredients = [ingredient_identifier(item["text"]) for item in entry.get("ingredients", [])]
        # results[recipe_id] = list(set(ingredients))
        count +=1

    print(count)
    return results



#################################################
# GENERATING STATS AND PLOTS
#################################################

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
        # for all the ingredients give their counts
        f.write("\n********************\nALL INGREDIENTS SORTED BY COUNT:\n")
        for ingredient, count in sorted_by_count:
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


# plotting function that creates mean median mode stats, longest shortest recipe, and num ingredients per recipe
def analyze_ingredients(ingredients_dict, modifier=""):
    # count the number of ingredients for each recipe
    ingredients_count = [len(ingredients) for ingredients in ingredients_dict.values()]
    # calculate statistics
    total_recipes = len(ingredients_count)
    total_ingredients = sum(ingredients_count)
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
    print(f"Total Ingredients: {total_ingredients}")
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


# makes a plot to show what would happen by varying the number of cutoffs
def numbers_cut_vs_ingredients_remaining(ingredients_dict):
    cutoffs = np.linspace(0, 1000, 21, dtype=int)
    number_kept = []
    for cutoff in cutoffs:
        _, kept_ingredients = rare_ingredients_filtering(ingredients_dict, cutoff=cutoff)
        number_kept.append(len(kept_ingredients))
    number_kept = np.array(number_kept)

    # plt.scatter(cutoffs, number_kept)
    # plt.xlabel("cutoff number")
    # plt.ylabel("remaining # unique ingredients")
    # plt.show()


# plots the rarity plot
def rarity(ingredients_dict):

    # dictionary to store ingredient counts by ingredient name
    ingredient_counts = defaultdict(int)
    for ingredient_list in ingredients_dict.values():
        for ingredient in ingredient_list:
            key = ingredient.lower()
            ingredient_counts[key] += 1
    # sort ingredients by their counts in descending order
    sorted_by_count = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_by_count)

    # plotting the distribution of ingredients per recipe
    ingredient_freq = []
    for ingredient, count in sorted_by_count:
        ingredient_freq.append(count)

    # create the histogram
    plt.hist(ingredient_freq, bins=100, edgecolor='black')
    plt.title('Rarity of Ingredients Distribution')
    plt.xlabel('Count of Ingredients in Full Dataset')
    plt.ylabel('Frequency of that Count')
    plt.ylim((0, 30))
    plt.grid(axis='y', alpha=0.25)
    plt.savefig("rarity.png")
    plt.close()



#################################################
# HELPER FILTERING FUNCTIONS
#################################################


# this is to filter out while we're writing the files to make sure only recipes with ingredient
# lists and at least one image are used
def extract_valid_ids_into_set(valid_ids_file):
    valid_ids = set() 
    with open(valid_ids_file, "r") as f:
        for line in f:
            id_str = line.strip() 
            if id_str: valid_ids.add(id_str)
    return valid_ids


# create a dictionary of remapping words for remapping all catagories into 32
def create_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as file:
        for line in file:
            if "||" in line:
                parts = line.split("||")
                name = parts[0].strip()
                category = parts[1].strip()
                name = re.sub(r'\s?\(\d+\)', '', name)
                mapping[name] = category
    return mapping


# rounds by a different threshold
def custom_round(value, threshold=0.8):
    if value - int(value) >= threshold:
        return int(value) + 1
    else:
        return int(value)


def create_ingredient_variant_matching():

    lines = [
        "agent1 (4337)", "agent2 (4337)", "allium (5320)", "berries (4501)", 
        "butter1 (3601)", "butter2 (3601)", "butter3 (3601)", "butter4 (3600)", 
        "cheese (5127)", "chocolate (4310)", "cinnamon (4819)", "condiment (6017)", 
        "cream1 (3526)", "cream2 (3526)", "dried fruit, jams, snacks, treats (4397)", 
        "fats (5831)", "flour1 (3426)", "flour2 (3426)", "flour3 (3426)", "flour4 (3425)", 
        "fruit (4674)", "juice1 (4282)", "juice2 (4281)", "liquids (3586)", 
        "meat and substitutes (5767)", "milk1 (3582)", "milk2 (3582)", "milk3 (3581)", 
        "nightshade (4732)", "nut1 (4253)", "nut2 (4253)", "oil1 (3571)", 
        "oil2 (3571)", "oil3 (3571)", "pepper1 (4416)", "pepper2 (4416)", 
        "powder1 (4323)", "powder2 (4323)", "root vegetable (4135)", "sauce (4987)", 
        "seasoning1 (4026)", "seasoning2 (4026)", "seed (6145)", "starches (5408)", 
        "syrup1 (4373)", "syrup2 (4372)", "syrup3 (4372)", "vegetable (4603)", 
        "vinegar (4866)", "water1 (4265)", "water2 (4264)", "water3 (4264)", 
        "wheat product (4735)"
    ]
    print(len(lines))
    variant_dict = {}
    for line in lines:
        match = re.match(r"([\w\s,']+?)\d*\s*\(\d+\)", line.strip())
        if match:
            base_word = match.group(1).strip()
            variant_dict.setdefault(base_word, []).append(re.sub(r"\s*\(.*?\)", "", line).strip())
    return variant_dict


#################################################
# FILTERING FUNCTIONS
#################################################


# takes out recipes that don't have images 
def make_valid(ingredients_dict, valid_ids_file):
    new_dict = {}
    for key_id, ingredients in ingredients_dict.items():
        if key_id in valid_ids:
            new_dict[key_id] = ingredients
    return new_dict

# filter the 375 classes to 32 classes by remapping scheme
def remap(ingredients_dict, word_map):
    new_dict = {}
    for key_id, ingredients in ingredients_dict.items():
        new_dict[key_id] = list(set([word_map[ingr] for ingr in ingredients]))
    return new_dict

# takes out recipes that have too many or few ingredients
def too_few_ingredients_recipe_filtering(ingredients_dict, cutoff=[4, 12]):
    new_dict = {}
    for key_id, ingredients in ingredients_dict.items():
        if len(ingredients) >= cutoff[0] and len(ingredients) <= cutoff[1]:
            new_dict[key_id] = ingredients
    return new_dict

# takes out ingredients from all dictionaries if the ingredient is too rare or common
def rare_ingredients_filtering(ingredients_dict, cutoff=[0, 1000]):
    # dictionary to store ingredient counts by ingredient name
    ingredient_counts = defaultdict(int)
    for ingredient_list in ingredients_dict.values():
        for ingredient in ingredient_list:
            key = ingredient.lower()
            ingredient_counts[key] += 1
    # sort ingredients by their counts in descending order
    sorted_by_count = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)
    # create a set of kept ingredients
    kept_ingredients = set()
    for ingredient, count in sorted_by_count:
        if count >= cutoff[0] and count<cutoff[1]:
            kept_ingredients.add(ingredient)
    # now in a new dictionary, remove any ingredients that are not in the set
    new_dict = {}
    for key_id, ingredients in ingredients_dict.items():
        fixed_ingredients = [ingred for ingred in ingredients if ingred in kept_ingredients]
        if len(fixed_ingredients)!= 0:  
            new_dict[key_id] = fixed_ingredients
    return new_dict, kept_ingredients


# turns flour into flour1 flour2 flour3 flour4
def balance_ingredients(ingredient_dict):
    # get all ingredient counts
    ingredient_counts = Counter()
    for ingredients in ingredient_dict.values():
        ingredient_counts.update(ingredients)
    # find the actual mind
    min_frequency = min(ingredient_counts.values())
    # for all ingredients figure out how many it should be remapped to
    ingredient_mapping = defaultdict(list)
    for ingredient, count in ingredient_counts.items():
        num_variants = custom_round(count/min_frequency, threshold=0.8)
        # print(ingredient, num_variants, count/min_frequency)
        if num_variants > 1:
            for i in range(1, num_variants + 1):
                ingredient_mapping[ingredient].append(f"{ingredient}{i}")
        else:
            ingredient_mapping[ingredient].append(ingredient)
    # replace all 
    balanced_ingredient_dict = {}
    ingredient_variant_counts = Counter()
    for key, ingredients in ingredient_dict.items():
        balanced_ingredients = []
        for ingredient in ingredients:
            # use variants cyclically if the ingredient has been split
            variants = ingredient_mapping[ingredient]
            current_variant = variants[ingredient_variant_counts[ingredient] % len(variants)]
            balanced_ingredients.append(current_variant)
            ingredient_variant_counts[ingredient] += 1
        balanced_ingredient_dict[key] = list(set(balanced_ingredients))
    return balanced_ingredient_dict

# turns flour into flour1 flour2 flour3 flour4
def balance_ingredients_with_known(ingredients_dict, ingredient_mapping):
    # replace all 
    balanced_ingredient_dict = {}
    ingredient_variant_counts = Counter()
    for key, ingredients in ingredients_dict.items():
        balanced_ingredients = []
        for ingredient in ingredients:
            # use variants cyclically if the ingredient has been split
            variants = ingredient_mapping[ingredient]
            current_variant = variants[ingredient_variant_counts[ingredient] % len(variants)]
            balanced_ingredients.append(current_variant)
            ingredient_variant_counts[ingredient] += 1
        balanced_ingredient_dict[key] = list(set(balanced_ingredients))
    return balanced_ingredient_dict


# you may specifiy a string and all those ingredients will be removed entirely
def removing_heavys(ingredients_dict, heavy):
    updated_dict = {}
    for recipe, ingredients in ingredients_dict.items():
        updated_ingredients = [ingredient for ingredient in ingredients if ingredient not in heavy]
        if len(updated_ingredients) != 0:
            updated_dict[recipe] = updated_ingredients
    return updated_dict





#################################################
# WRITE THE FINAL INGREDIENTS FOR CNN
#################################################

# recreates dictionary of ingredients from unsplit folder (or training val test folders)
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


# # for each valid file ID, write that ingredient list of data to a TXT file call ID.txt
# def write_all_files(ingredients_dict, valid_ids, main_folder):
#     os.makedirs(main_folder, exist_ok=True)
#     for key_id, ingredients in ingredients_dict.items():
#         if key_id in valid_ids:
#             file_path = os.path.join(main_folder, f"{key_id}.txt")
#             with open(file_path, "w") as f:
#                 for ingredient in ingredients:
#                     f.write(f"{ingredient}\n")
#     return

# for each valid file ID, write that ingredient list of data to a TXT file call ID.txt
def write_all_files_web(ingredients_dict, main_folder):
    os.makedirs(main_folder, exist_ok=True)
    for key_id, ingredients in ingredients_dict.items():
        file_path = os.path.join(main_folder, f"{key_id}.txt")
        with open(file_path, "w") as f:
            for ingredient in ingredients:
                f.write(f"{ingredient}\n")
    return


# writes the list of valid current IDs after all my processing
def write_dict_keys_to_file(ingredients_dict, file_path):
    try:
        with open(file_path, 'w') as file:
            for key in ingredients_dict.keys():
                file.write(f"{key}\n")
        print(f"Keys written to {file_path} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


#################################################
# MAIN
#################################################

json_file = "/Users/felicialiu/Desktop/APS360/Project/dev/recipes_with_nutritional_info.json"
valid_ids_file = "/Users/felicialiu/Desktop/APS360/Project/dev/valid_recipe_ids.txt"
main_folder = "/Users/felicialiu/Desktop/APS360/Project/new_unsplit/default"
remapping_file = "/Users/felicialiu/Desktop/APS360/Project/dev/remapped.txt"


# same always, open the json, extract IDs and ingredient lists
ingredients_dict = parse_ingredients(json_file)

# # from given file that corresponds to recipes with images
# # remove those without images
# valid_ids = extract_valid_ids_into_set(valid_ids_file)
# ingredients_dict = make_valid(ingredients_dict, valid_ids_file)

# # from given file that changes word correspondences
# # remap 375 ingredient catagories into only 32
# word_map = create_mapping(remapping_file)
# ingredients_dict = remap(ingredients_dict, word_map)

# # define heavy ingredients and remove them entirely
# heavys = "salt sugar"
# ingredients_dict = removing_heavys(ingredients_dict, heavys)

# # balance still heavy ingredients with the lower numbers
# ingredients_dict = balance_ingredients(ingredients_dict)

# print(len(ingredients_dict['fffb3bbff2']), ingredients_dict['fffb3bbff2'])


###############
# UNUSED BALANCING

# # use to choose a good number for cutoff rare_ingredients_filtering
# numbers_cut_vs_ingredients_remaining(ingredients_dict)

# filter ingredients out if they are too obscure/rare
# ingredients_dict, _ = rare_ingredients_filtering(ingredients_dict, cutoff=[50, 200])

# # filter out recipes that have too few ingredients
# ingredients_dict = too_few_ingredients_recipe_filtering(ingredients_dict, cutoff=[2, 9])
###############

# run full analysis
# rarity(ingredients_dict)
# generate_ingredient_report(ingredients_dict)
# analyze_ingredients(ingredients_dict)

# once analysis looks good generate the folder of all ingredient lists
# then divide into training testing cohorts
# write_all_files(ingredients_dict, valid_ids, main_folder)

# write all valid ids after processing
# new_valid_keys = "/Users/felicialiu/Desktop/APS360/Project Guidelines/dev/new_valid_keys.txt"
# write_dict_keys_to_file(ingredients_dict, new_valid_keys)




###############
# UNUSED TESTING

# for key_id, ingredients in ingredients_dict.items():
#     if len(ingredients) == 1:
#         print(key_id, ":", ingredients)
# print(len(valid_ids), len(ingredients_dict.keys()))

# modi = "test"
# main_folder = '/Users/felicialiu/Desktop/APS360/Project Guidelines/LABELS/{}'.format(modi)
# ingredients_dict = read_all_files(main_folder)
# generate_ingredient_report(ingredients_dict, modi)
# analyze_ingredients(ingredients_dict, modi)

###############




#################################################
# WEBSCRAPING
#################################################

# json_file = "/Users/felicialiu/Desktop/APS360/Project Guidelines/dev/processed_recipe_data.json"
# main_folder = "/Users/felicialiu/Desktop/APS360/Project Guidelines/new_unsplit/default"
# remapping_file = "/Users/felicialiu/Desktop/APS360/Project Guidelines/dev/remapped_web.txt"


# # same always, open the json, extract IDs and ingredient lists
# ingredients_dict = parse_ingredients(json_file, webscraped=True)

# # from given file that changes word correspondences
# # remap 1350 ingredient catagories into only 32
# word_map = create_mapping(remapping_file)
# ingredients_dict = remap(ingredients_dict, word_map)

# # define heavy ingredients and remove them entirely
# heavys = "salt sugar weird"
# ingredients_dict = removing_heavys(ingredients_dict, heavys)

# # balance still heavy ingredients with the lower numbers
# ingredient_mapping = create_ingredient_variant_matching()

# ingredients_dict = balance_ingredients_with_known(ingredients_dict, ingredient_mapping)

# # run full analysis
# rarity(ingredients_dict)
# generate_ingredient_report(ingredients_dict)
# analyze_ingredients(ingredients_dict)

# # once analysis looks good generate the folder of all ingredient lists
# # then divide into training testing cohorts
# write_all_files_web(ingredients_dict, main_folder)

# # write all valid ids after processing
# # new_valid_keys = "/Users/felicialiu/Desktop/APS360/Project Guidelines/dev/new_valid_keys.txt"
# # write_dict_keys_to_file(ingredients_dict, new_valid_keys)

