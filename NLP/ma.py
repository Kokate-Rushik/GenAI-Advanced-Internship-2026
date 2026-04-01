from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Configuring & Data Saving
model_name = "microsoft/DialoGPT-small"
local_save_path = "./my_local_model"

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir = local_save_path)
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir = local_save_path)

def chat():
    chat_history_ids = None
    print("Chatbot: Hello! I am your AI assistant. How can I help you today? (Type 'exit' to quit)")

    while True:
        # User Input Handling
        user_input = input("User: ")

        # Exit condition
        if user_input.lower() in ['exit','quit']:
            print("ChatBot: Goodbye!")
            break

        # Encoding & Response Generation
        # Encode user input
        inputs = tokenizer(user_input + tokenizer.eos_token, return_tensors='pt')
        new_user_input_ids = inputs['input_ids']
        user_attention_mask = inputs['attention_mask']


        # Append new user input to chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=1) if chat_history_ids is not None else new_user_input_ids

        # Generate a response (Max 1000 tokens)
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.6,
            repetition_penalty=1.2
        )

        # Display Output
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat()