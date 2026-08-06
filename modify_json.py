import json
import sys

def main():
    with open('current_workflow_38.json', 'r', encoding='utf-16') as f:
        data = json.load(f)

    for node in data.get('nodes', []):
        if node.get('type') == 'startCall':
            prompt = node['data']['prompt']
            
            # Prepend language instructions
            lang_instructions = """Language Support Rules:
1. Immediately after greeting the user, ask them which language they are comfortable in.
2. Offer the following options: English, Hindi, Punjabi, Bengali, or Kannada.
3. Once the user selects a language, you MUST communicate entirely in that selected language for the rest of the conversation. Do not use English unless the user selected English.

"""
            node['data']['prompt'] = lang_instructions + prompt
            
            # Update greeting
            node['data']['greeting'] = "Hello, thanks for calling Dine and Order. Which language are you comfortable with? We support English, Hindi, Punjabi, Bengali, or Kannada."

    with open('updated_workflow_38.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()
