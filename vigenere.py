"""
vigenere.py
Usage: vigenere.py k
Where k is a key containaing only aplphabetical character

Luke Benz
"""
import cs50
import sys
    
# Ensure proper usage
if len(sys.argv) != 2:
    sys.exit("Usage: vigenere.py k")
    
# Store key and ensure all characters are alphabetical
key = sys.argv[1]
for i in range(len(key)):
    if str.isalpha(key[i]) == False:
        sys.exit("Usage: vigenere.py k")
        
print("plaintext: ", end = "")
message = cs50.get_string()
print("ciphertext: ", end = "")
    
shift = 0
counter = 0
keyLength = len(key)
    
# Loop over characters in plaintext
for i in range(len(message)):
    # Get alphabetical index of the counter character in the key
    if str.isupper(key[counter%keyLength]):
        shift = ord(key[counter%keyLength]) - ord('A')
    else:
        shift = ord(key[counter%keyLength]) - ord('a')
        
    # Check if i'th character in message is alphabetic
    if str.isalpha(message[i]):
        # Determine case and hanle accordingly
        if str.isupper(message[i]):
            newchar = chr((ord(message[i]) - ord('A') + shift) % 26 + ord('A'))
            print("{}".format(newchar), end = "")
            counter += 1
        else:
            newchar = chr((ord(message[i]) - ord('a') + shift) % 26 + ord('a'))
            print("{}".format(newchar), end = "")
            counter += 1
    # If character isn't alphabetical, print as is
    else:
        print("{}".format(message[i]), end = "")
    
# Return new line
print()
sys.exit(0)