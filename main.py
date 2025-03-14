import ollama
import notes_chat

with open("modelfiles/modelfile_1.txt", "r", encoding="utf-8") as file:
    main_chat_content = file.read()

with open("modelfiles/modelfile_2.txt", "r", encoding="utf-8") as file:
    general_chat_content = file.read()




def main_chat(query):
    
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': main_chat_content },
            {'role': 'user', 'content': query}
        ],
        options={'temperature': 0.7}  # Adjust temperature (0.0 = deterministic, 1.0 = creative)
    )
    answer = response['message']['content']
    return answer


def general_chat(query):
    
    response = ollama.chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': general_chat_content },
            {'role': 'user', 'content': query}
        ],
        options={'temperature': 0.7}  # Adjust temperature (0.0 = deterministic, 1.0 = creative)
    )
    answer = response['message']['content']
    return answer
    



import streamlit as st

import ollama


# streamlit run main.py




def main():
    st.title("Notes Assistant")

    # User input
    user_input = st.text_input("Enter your notes:", "")

    if user_input:
        with st.spinner("Generating organized notes..."):
            try:
                # Initialize the language model
    
                st.markdown("**Assistant:**")
                
                answer = main_chat(user_input)
                
                if(answer =="1"):
                    
                    answer = general_chat(user_input)
                
                if(answer == "2"):
                    answer = notes_chat.notes_chat_main(user_input)
                    
                    
                    
                final_answer =  answer
                st.write(final_answer)
                
               
                
                #generate_json(user_input , response["response"], "LWS_Project_2/notes_db.json")
                
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Copy and Paste your Notes to get started.")


if __name__ == "__main__":
    main()

