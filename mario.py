import cs50

# Get Height from user and reject if not between 0-23
while True:
    print("Height: ", end = "")
    height= cs50.get_int()
    if height >= 0 and height <= 23:
        break
    
# Iteratively print spaces and hashes 
for row in range(height):
    # Print initial spaces
    spaces = height - (row + 1) 
    for j in range(spaces):
        print(" ", end = "")
        
    # Print left half of pyramid
    for k in range(row + 1):
        print("#", end = "")
        
    # Print gap   
    print("  ", end = "")
    
    # Print right half of pyramid
    for l in range(row + 1):
        print("#", end = "")
        
    # Move to new line
    print()