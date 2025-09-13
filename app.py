import streamlit as st
import string
import math
import hashlib
import requests
from datetime import datetime


def check_pwned(password):
    sha1_pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_pwd[:5]
    suffix = sha1_pwd[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    hashes = (line.split(':') for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0


def calculate_entropy(password):
    unique_chars = set(password)
    entropy = 0
    for char in unique_chars:
        p_x = password.count(char) / len(password)
        entropy += - p_x * math.log2(p_x)
    return round(entropy * len(password), 2)


def log_attempt(password, entropy, passed_rules, pwned_count):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a") as file:
        file.write(f"[{time}]\n")
        obfuscated = '*' * (len(password)-3) + password[-3:] if len(password) > 3 else '*' * len(password)
        file.write(f"Password: {obfuscated}\n")
        file.write(f"Entropy: {entropy} bits\n")
        file.write(f"Rule Check: {'Passed' if passed_rules else 'Failed'}\n")
        if pwned_count:
            file.write(f"Breach Check: Found in {pwned_count} breaches\n")
        else:
            file.write("Breach Check: Not Found\n")
        file.write("-" * 40 + "\n")


# Streamlit App UI
st.title(" Password Strength & Breach Checker")

password = st.text_input("Enter your password:", type="password")

if st.button("Check Password"):
    if password:
        st.subheader(" Password Analysis")

        # Entropy
        entropy = calculate_entropy(password)
        st.write(f"**Entropy Score:** `{entropy} bits`")
        if entropy < 28:
            st.error("Very Weak – Easily crackable.")
        elif entropy < 36:
            st.warning("Weak – Can be brute-forced.")
        elif entropy < 60:
            st.info("Moderate – Better than average, but could improve.")
        else:
            st.success("Strong – Good work, this one's tough to break.")

        # Character breakdown
        alphanumerical = 0
        specialch = 0
        blankspace = 0
        UC = 0

        for ch in password:
            if ch.isalnum():
                alphanumerical += 1
                if ch.isupper():
                    UC += 1
            elif ch in string.punctuation:
                specialch += 1
            elif ch.isspace():
                blankspace += 1

        st.write("###  Character Breakdown")
        st.write(f"- Alphanumerical characters: `{alphanumerical}`")
        st.write(f"- Special characters: `{specialch}`")
        st.write(f"- Uppercase letters: `{UC}`")
        st.write(f"- Blank spaces: `{blankspace}`")

        passed_rules = alphanumerical >= 8 and specialch >= 1 and blankspace == 0 and UC >= 1
        if passed_rules:
            st.success(" Password passed the rule-based check.")
        else:
            st.error(" Password failed the rule-based check. Suggestions:")
            if alphanumerical < 8:
                st.write("- Add more letters or numbers (at least 8).")
            if specialch < 1:
                st.write("- Include special characters like @, #, $, etc.")
            if UC < 1:
                st.write("- Use at least one uppercase letter.")
            if blankspace > 0:
                st.write("- Remove spaces.")

        # Pwned Password Check
        st.write("###  Checking against known data breaches...")
        pwned_count = check_pwned(password)
        if pwned_count is None:
            st.error("Could not connect to the breach database.")
        elif pwned_count:
            st.warning(f"This password has been found in `{pwned_count}` breaches. Avoid using it.")
        else:
            st.success("Good news — this password has not been found in known breaches.")

        # Log the result
        log_attempt(password, entropy, passed_rules, pwned_count)
    else:
        st.warning("Please enter a password to check.")
