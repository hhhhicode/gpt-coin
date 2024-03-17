def get_instructions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            instructions = file.read()
        return instructions
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred while reading the file:", e)


def write_upbit_output(message):
    with open("upbit_output.txt", "w", encoding="utf-8") as file:
        file.write(message)
