def check_rep(pasw):
    rep_count = 0
    for i in range(len(pasw)-1):
        if pasw[i] == pasw[i+1]:
            rep_count+=1
    if rep_count >= 3:
        requirements.append("Password must not contain more than 3 repeated characters")

print("Welcome to password checker! Here are the requirements for your password:")
print("- At least 8 characters long")
print("- Contains both uppercase and lowercase letters")
print("- Contains at least one digit")
print("- Contains at least one special character")
print("- No more than 3 repeated characters in a row")
print("- No more than 3 numbers increasing/decreasing in a row")

requirements = ["placeholder"]

while requirements:
    requirements.clear()
    password = input("enter a password: ")
    password.split()

    #generated using ai for bottom 5 lines
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_number = any(ch.isdigit() for ch in password)
    specials = "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
    has_special = any(ch in specials for ch in password)

    if len(password) < 8:
        requirements.append("Password must be at least 8 characters long.")

    if has_upper and has_lower:
        requirements.append()
    else:
        requirements.append("Password must contain both upppercase and lowercase letters")

    if has_number:
        print()
    else:
        requirements.append("Password must contain at least one digit")
    
    if has_special:
        print()
    else:
        requirements.append("Password must contain at least one special character")

    check_rep(password)

    if requirements:
        print("Your password does not meet the requirements:")
        for i in requirements:
            print(i)

print("Congratulations, your password is secure!")
