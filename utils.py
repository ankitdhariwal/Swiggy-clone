import json

# Writing to a text file
def writeFile(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def readFile(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

# Appending to a text file
def appendFile(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content)
