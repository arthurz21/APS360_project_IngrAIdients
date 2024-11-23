
# def process_ingredients(input_file, output_file):
#     with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#         for line in infile:
#             # Extract the ingredient part before the parentheses
#             ingredient = line.split('(')[0].strip()
#             # Write the formatted line to the output file
#             outfile.write(f"{line.strip():<30} || {ingredient}\n")

# # Example usage
# process_ingredients('test.txt', 'processed_ingredients.txt')


def process_file(input_file, output_file, keyword):
    normal_lines = []
    keyword_lines = []

    with open(input_file, 'r') as infile:
        for line in infile:
            if keyword in line:
                # Replace content after "||" with the keyword
                if "||" in line:
                    parts = line.split("||", 1)
                    keyword_lines.append(f"{parts[0]}|| {keyword}\n")
                else:
                    keyword_lines.append(line)
            else:
                normal_lines.append(line)

    with open(output_file, 'w') as outfile:
        # Write normal lines first
        outfile.writelines(normal_lines)
        # Write keyword lines at the end
        outfile.write("\n")  # Separate sections with a blank line
        outfile.writelines(keyword_lines)


# Example usage
input_file = "processed_ingredients.txt"  # Replace with your input file name
output_file = "processed_ingredients_AHH.txt"  # Replace with your desired output file name
keyword = "snack"  # Replace with your desired keyword

process_file(input_file, output_file, keyword)

