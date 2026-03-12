#Me and my partner made the entire code together

#function to check for repeated characters in a row
#only flags if more than three identical characters appear consecutively
def check_rep(pasw):
    if not pasw:
        return None
    curr_reps = 1
    for i in range(1, len(pasw)):
        if pasw[i] == pasw[i-1]:
            curr_reps += 1
            if curr_reps > 3:
                return "Password must not contain more than 3 repeated characters in a row"
        else:
            curr_reps = 1
    return None

#function to check for increasing/decreasing numbers
def check_inc_dec(pasw):
    inc_count = 0
    dec_count = 0
    for i in range(len(pasw)-1):
        if pasw[i].isdigit() and pasw[i+1].isdigit(): #checking if they are numbers first
            if int(pasw[i]) + 1 == int(pasw[i+1]):
                inc_count+=1
            elif int(pasw[i]) - 1 == int(pasw[i+1]):
                dec_count+=1
    if inc_count >= 3:
        requirements.append("Password must not contain more than 3 increasing numbers in a row")
    if dec_count >= 3:
        requirements.append("Password must not contain more than 3 decreasing numbers in a row")
    return None

print("Welcome to password checker! Here are the requirements for your password:")
print("- At least 8 characters long")
print("- Contains both uppercase and lowercase letters")
print("- Contains at least one digit")
print("- Contains at least one special character")
print("- No more than 3 repeated characters in a row")
print("- No more than 3 numbers increasing/decreasing in a row")

requirements = ["placeholder"]
check = True

while requirements:
    requirements.clear()
    password = input("enter a password: ")
    password.split()

    if password.upper() == "X":
        print("Thanks for using password checker. Goodbye!")
        check = False
        break

    #generated using ai for bottom 5 lines
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_number = any(ch.isdigit() for ch in password)
    specials = "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
    has_special = any(ch in specials for ch in password)

    if len(password) < 8:
        requirements.append("Password must be at least 8 characters long")

    if not has_upper or not has_lower:
        requirements.append("Password must contain both uppercase and lowercase letters")
    
    if not has_special:
        requirements.append("Password must contain at least one special character")

    if not has_number:
        requirements.append("Password must contain at least one digit")

    if check_rep(password):
        requirements.append(check_rep(password))

    check_inc_dec(password)

    if requirements:
        print("Your password does not meet the requirements:")
        for i in requirements:
            print(i)
    print("(Enter X to exit)")

if check:
    print("Congratulations, your password is secure!")
