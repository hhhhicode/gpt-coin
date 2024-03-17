import os
import application.service.my_upbit as my_upbit
import utils.file_util as file_util
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_data_with_gpt4(data_json: str):
    instructions_path = "instructions.md"
    try:
        instructions = file_util.get_instructions(instructions_path)
        if not instructions:
            print("No instructions found.")
            return None

        current_status = my_upbit.get_current_status()
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": data_json},
                {"role": "user", "content": current_status}
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in analyzing data with GPT-4: {e}")
        return None
