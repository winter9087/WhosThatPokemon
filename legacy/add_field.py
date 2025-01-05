#add empty field for german names

from pokemon_data_legacy_1 import pokemon_data
def add_field_to_dic(input_dictionary,field_added):
    for i in input_dictionary:
        i[field_added] = ""
    return input_dictionary

# Add "name_german" with an empty value to each dictionary
pokemon_data = add_field_to_dic(pokemon_data, "silhouette")

# Output the modified data
output_file = "pokemon_data_new.py"
with open(output_file, "w") as f:
    f.write("pokemon_data = [\n")
    for pokemon in pokemon_data:
        f.write(f"    {pokemon},\n")
    f.write("]\n")