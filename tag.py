# Author: Green
# Version: 1.0
# Generates a random un-used tag from den_countries.txt, and optionally will provide a *most of the time* valid unclaimed state within the region for use.
# Note: This script is not perfect, and may not always provide a valid state, or may provide an out of bound state. If it does, re-run the script, or ignore the result.
# How to use: Run the code. Input as needed.

# If it breaks, let me know.

import random
import string
import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))

file_path = os.path.join(script_dir, "common/country_tags/den_countries.txt")
states_dir = os.path.join(script_dir, "history", "states")
localisation_dir = os.path.join(script_dir, "localisation", "english")

def load_existing_tags(file_path):
    try:
        with open(file_path, 'r') as file:
            existing_tags = [line.split('=')[0].strip() for line in file if '=' in line]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        existing_tags = []
    return existing_tags

def generate_unique_tag(existing_tags):
    while True:
        tag = "X" + random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
        
        if tag not in existing_tags:
            return tag

def find_lib_states(states_dir):
    lib_states = []
    # Specific region
    core_lines = [
        "#add_core_of = CHI", "#add_core_of = JAP", "#add_core_of = KOR",
        "#add_core_of = MAN", "#add_core_of = LAO", "#add_core_of = NEP",
        "#add_core_of = BHU", "#add_core_of = VIN", "#add_core_of = SIA"
    ]
    
    if not os.path.exists(states_dir):
        print(f"Directory not found: {states_dir}")
        return lib_states
    
    for file_name in os.listdir(states_dir):
        if file_name.endswith(".txt"):
            with open(os.path.join(states_dir, file_name), 'r') as file:
                state_id = None
                owner_found = False
                core_found = False
                for line in file:
                    if "id=" in line:
                        state_id = int(line.split('=')[1].strip())
                    if "owner = LIB" in line:
                        owner_found = True
                    if any(core_line in line for core_line in core_lines):
                        core_found = True
                if owner_found and core_found and state_id:
                    lib_states.append(state_id)
    
    return lib_states

def load_localisation_data(localisation_dir):
    localisation_data = {}
    state_regex = re.compile(r'^\s*STATE_(\d+).*?["\s](.+?)["\s]*$')
    
    for file_name in os.listdir(localisation_dir):
        if file_name.endswith(".yml"):
            with open(os.path.join(localisation_dir, file_name), 'r', encoding='utf-8') as file:
                for line in file:
                    match = state_regex.match(line)
                    if match:
                        state_id = int(match.group(1))
                        state_name = match.group(2).strip('"')
                        localisation_data[state_id] = state_name
    return localisation_data

def main():
    existing_tags = load_existing_tags(file_path)
    new_tag = generate_unique_tag(existing_tags)
    
    print("Generating an available tag...")
    print(f"Existing tags: ", existing_tags)
    print()
    print(f"Generated tag: {new_tag}")

    affirmative_responses = {"y", "yes", "yeah", "yep", "sure", "ok", "okay"}
    choice = input("Do you want to get a random unclaimed state owned by LIB? (yes/no): ").strip().lower()
    if choice in affirmative_responses:
        print("Note: This may include some out of bound states, if it does, re-run again, or ignore the result.")
        lib_states = find_lib_states(states_dir)
        localisation_data = load_localisation_data(localisation_dir)

        if lib_states:
            random_state = random.choice(lib_states)
            state_name = localisation_data.get(random_state, f"STATE_{random_state}")
            print('An available state is :', random_state, "(", state_name, ")")
        else:
            print('No available state found')
    else:
        print('No state selected')

    input("\nPress Enter to exit...")            

if __name__ == "__main__":
    main()
