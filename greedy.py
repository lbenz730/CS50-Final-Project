import cs50

# Get amount of change to return
while True:
    print("How much change is owed?")
    change = cs50.get_float()
    if change >= 0:
        break
 
# Convert change to cents
cents = round(change * 100)

# Get number of coins to return
coins = cents // 25
cents = cents % 25
coins += cents // 10
cents = cents % 10
coins += cents // 5
cents = cents % 5
coins += cents

# Print result
print("{} coins".format(coins))