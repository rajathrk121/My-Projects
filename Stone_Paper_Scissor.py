import random

a = ("stone", "paper", "scissor")
b = random.choice(a)

print("Enter your choice:")
print("1. Stone")
print("2. Paper")
print("3. Scissor")

choice = int(input("Enter Your Choice: "))

if choice == 1:
    c = "stone"
elif choice == 2:
    c = "paper"
elif choice == 3:
    c = "scissor"
else:
    c = "invalid"

print("Your choice is:", c)
print("Computer's choice is:", b)

if c == b:
    print("The Game is Drawn")
elif (c == "stone" and b == "scissor") or (c == "scissor" and b == "paper") or (c == "paper" and b == "stone"):
    print("You had Won. Your choice is", c)
elif (c == "scissor" and b == "stone") or (c == "paper" and b == "scissor") or (c == "stone" and b == "paper"):
    print("Computer had Won. Computer's choice is", b)
else:
    print("Invalid input. Please start the game again.")
