# silhuouououotte field was empty so we also pull from image name for that
import os
from pokemon_data_legacy2 import pokemon_data
# Path to the folder containing silhouette images
silhouette_folder = "pokemon_images_silhouette"

# Function to add silhouette field
def add_silhouette_field(pokemon_data, silhouette_folder):
    updated_data = []
    
    for pokemon in pokemon_data:
        image_name = pokemon['image']
        silhouette_path = os.path.join(silhouette_folder, image_name)
        
        if os.path.exists(silhouette_path):
            pokemon['silhouette'] = image_name  # Just store the relative filename
        else:
            pokemon['silhouette'] = None  # Handle cases where silhouette is missing
        
        updated_data.append(pokemon)
    
    return updated_data

# Add silhouette paths
pokemon_data = add_silhouette_field(pokemon_data, silhouette_folder)

# Save updated data to a Python file
output_file = "pokemon_data_new.py"
with open(output_file, "w") as f:
    f.write("pokemon_data = [\n")
    for pokemon in pokemon_data:
        f.write(f"    {pokemon},\n")
    f.write("]\n")

print(f"Updated data saved to {output_file}")
