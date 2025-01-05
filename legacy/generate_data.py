# problem: i have folder full of images and i do not want to manually make a list of every pokemon. solution:
import os

def gen_list_from_folder(folder_path, output_file):
    # folder exists?
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder '{folder_path}' not found.")
    # get a list of files
    files = [f for f in os.listdir(folder_path) if f.endswith('.webp')]
    # sort files
    files.sort()
    
    # generate the list
    pokemon_data = []
    for file in files:
        # split into number and name 
        parts = file.split(' ', 1)
        if len(parts) != 2:
            continue
        name = parts[1].rsplit('.', 1)[0].lower()
        #add to list
        pokemon_data.append({"name": name, "image": file})

    # write the py file
    with open(output_file, 'w') as py_file:
        py_file.write("pokemon_data = [\n")
        for entry in pokemon_data:
            py_file.write(f"    {{\"name\": \"{entry['name']}\", \"image\": \"{entry['image']}\"}},\n")
        py_file.write("]\n")

# generate
folder_path = "pokemon_images_full"
output_file = "pokemon_data_legacy.py"
gen_list_from_folder(folder_path, output_file)
