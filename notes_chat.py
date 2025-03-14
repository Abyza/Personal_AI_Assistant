import ollama
import os
import json
import re

with open("modelfiles/modelfile_notes_1.txt", "r", encoding="utf-8") as file:
    notes_chat_content = file.read()
    
with open("modelfiles/modelfile_notes_2.txt", "r", encoding="utf-8") as file:
    notes_chat_content_save = file.read()
    
with open("modelfiles/modelfile_notes_3.txt", "r", encoding="utf-8") as file:
    notes_chat_content_retrieve = file.read()
    
with open("modelfiles/modelfile_notes_4.txt", "r", encoding="utf-8") as file:
    notes_chat_content_general= file.read()
    
def load_json_notes():
    """Reads 'notes.json', loads its content as a dictionary, and returns a JSON string."""
    with open("notes.json", "r") as file:
        json_data = json.load(file)  # Load JSON as a Python dictionary
        json_notes_string = json.dumps(json_data)  # Convert dictionary to string
    return json_notes_string

def notes_chat_main(query):
    
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': notes_chat_content },
            {'role': 'user', 'content': query}
        ],
        options={'temperature': 0.7}  # Adjust temperature (0.0 = deterministic, 1.0 = creative)
    )
    answer = response['message']['content']
    
    if(answer == "1"):
        answer = notes_chat_save(query)
                        
                    
    if(answer == "2"):
        answer = notes_chat_retrieve(query)
                    
                    
    if(answer == "3"):
        answer = notes_chat_general(query)
    
    return answer

def notes_chat_save(query):
    
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': notes_chat_content_save},
            {'role': 'user', 'content': query}
        ],
        options={'temperature': 0.7}  # Adjust temperature (0.0 = deterministic, 1.0 = creative)
    )
    answer = response['message']['content']
    note_id = generate_json(query, answer , file_path="notes.json")
    response = f"This is saved as a Note. Here is the saved version, and this is note number {note_id}: {answer}"
    return response 

def notes_chat_retrieve(query):
    json_notes_string= load_json_notes()
    notes_chat_retrieve_content  = f'{notes_chat_content_retrieve}{json_notes_string}'
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': notes_chat_retrieve_content},
            {'role': 'user', 'content': query}
        ],
        options={'temperature': 0.7}  # Adjust temperature (0.0 = deterministic, 1.0 = creative)
    )
    
    list_id =response['message']['content']
    answer = get_notes_by_ids( list_id,"notes.json" )
    return answer


def get_notes_by_ids(id_list_str, json_file_path):
    """
    Retrieves the 'fixed_notes' for the given list of IDs from the JSON file.

    :param id_list_str: A string formatted like an array, e.g., "[1, 3, 5]"
    :param json_file_path: Path to the JSON file containing notes.
    :return: A list of dictionaries with 'id' and 'fixed_notes'.
    """
    try:
        # Extract numbers from the string (e.g., "[1, 3]" → [1, 3])
        id_list = [int(num) for num in re.findall(r'\d+', id_list_str)]

        # Load the JSON data from the file
        with open(json_file_path, "r", encoding="utf-8") as file:
            notes_data = json.load(file)

        # Filter notes based on the provided IDs
        filtered_notes = [{"id": note["id"], "fixed_notes": note["fixed_notes"]}
                          for note in notes_data if note["id"] in id_list]

        return filtered_notes

    except Exception as e:
        return {"error": str(e)}


def notes_chat_general(query):
    json_notes_string= load_json_notes()
    notes_chat_retrieve_content  = f'{ notes_chat_content_general}{json_notes_string}'
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': notes_chat_retrieve_content },
            {'role': 'user', 'content': query}
        ],
        options={'temperature': 0.7}  # Adjust temperature (0.0 = deterministic, 1.0 = creative)
    )
    answer = response['message']['content']
    return answer


def generate_json(original_notes, fixed_notes, file_path="notes.json"):
    # Check if file exists
    if not os.path.exists(file_path):
        data = []
    else:
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    # Generate new ID
    new_id = len(data) + 1

    # Create the new note entry
    new_entry = {
        "id": new_id,
        "original_notes": original_notes,
        "fixed_notes": fixed_notes
    }

    # Append the new note and save to file
    data.append(new_entry)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Note added with ID: {new_id}")
    
    return new_id