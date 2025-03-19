import json
import os

# Load tags from the JSON file
def load_tags(filename="tags.json"):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        print("Tags file not found!")
        return []

if __name__ == "__main__":
    tags = load_tags()
    print("Loaded Tags:", tags)
