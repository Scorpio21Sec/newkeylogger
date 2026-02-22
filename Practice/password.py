import re

def check_password_strength(password):
    length_error = len(password) < 12
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ !@#$%^&*()_+={}\[\]:;'<>,.?/~`-]", password) is None

    errors = {
        'Too Short': length_error,
        'No Digit': digit_error,
        'No Uppercase': uppercase_error,
        'No Lowercase': lowercase_error,
        'No Symbol': symbol_error
    }

    passed = not any(errors.values())

    print("\nPassword:", password)
    print("Strength Check:")
    for k, v in errors.items():
        print(f" - {k}: {'❌' if v else '✅'}")
    
    if passed:
        print("✅ This is a strong password!")
    else:
        print("❌ Weak password. Improve based on ❌ above.")

password = input("Enter your password to test: ")
check_password_strength(password)
