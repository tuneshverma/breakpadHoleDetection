import random
import sys

# Define the filename and key
filename = sys.argv[1]
key = random.randint(1, 1000)

# Read the file contents into a string
with open(filename, "r") as f:
    contents = f.read()

# Convert the string into a list of characters
chars = list(contents)

# Shuffle the list
random.shuffle(chars)

# Convert the shuffled list back into a string
shuffled_contents = "".join(chars)

# Encode the shuffled string using a simple Caesar cipher
encoded_contents = ""
for char in shuffled_contents:
    if char.isalpha():
        encoded_char = chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        encoded_contents += encoded_char
    else:
        encoded_contents += char

# Write the encoded string back to a file
with open(filename, "w") as f:
    f.write(encoded_contents)

# Print the key and filename for reference
print("Key: ", key)
print("Encoded file: ", filename)
