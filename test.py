import difflib, csv
from unidecode import unidecode

def autofill_suggestions(user_input, term_pool, num_suggestions=3):
    # Normalize user input and term pool to ASCII
    normalized_input = unidecode(user_input)
    normalized_pool = [unidecode(term) for term in term_pool]
    
    # Find the closest matches
    matches = difflib.get_close_matches(normalized_input, normalized_pool, n=num_suggestions, cutoff=0.6)
    
    # Find the original terms that match the normalized closest matches
    suggestions = [next(term for term in term_pool if unidecode(term) == match) for match in matches]
    
    return suggestions


# get dictionaries
with open('assets/codes.csv', 'r', encoding='utf-8') as codes_input:
    cr = csv.reader(codes_input)
    countries = {}
    types = {}
    for line in cr:
        countries[line[1]] = line[0].replace('\ufeff', '')
        types[line[0].replace('\ufeff', '').replace("The ", "")] = line[1]

# Example usage
term_pool = ["United States", "United Kingdom", "Congo", "China, People's Republic of", "Chile"]
user_input = "united states of"

# suggestions = autofill_suggestions(user_input, countries)
# print(f"Suggestions for '{user_input}': {suggestions}")

# user_input = input("Your choice: ")

# You have to handle the case where 2 or more teams starts with the same string.
# For example the user input is 'B'. So you have to select between "Blackpool" and
# "Blackburn"
filtered_teams = [lambda x: x.startswith(user_input), types.keys()]

print(filtered_teams)

if len(filtered_teams) > 1:
    # Deal with more that one team.
    print('There are more than one team starting with "{0}"'.format(user_input))
    print(filtered_teams[0])

else:
    # Only one team found, so print that team.
    print(filtered_teams[0])


def items_starting_with(prefix, items):
    # Normalize the prefix and items to ASCII
    normalized_prefix = unidecode(prefix).lower()
    
    # Find all items that start with the normalized prefix
    matching_items = [item for item in items if unidecode(item).lower().startswith(normalized_prefix)]
    
    return matching_items

# Example usage
items = ["Argentina", "Armenia", "Australia", "Austria", "Brazil", "Canada", "China"]
prefix = "Reunion"

matching_items = items_starting_with(prefix, types.keys())
print(f"Items starting with '{prefix}': {matching_items}")