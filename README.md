Password Strength & Breach Checker
An interactive Streamlit web application that evaluates how strong your password is and checks if it has appeared in known data breaches using the Have I Been Pwned API.
The app calculates entropy, evaluates rule-based strength, provides character breakdown, and securely checks your password against millions of leaked credentials — helping you avoid weak or compromised passwords.

Features
Entropy Score – Estimates password complexity in bits.

Rule-based Check – Requires at least:
8+ alphanumeric characters
1+ special character
1+ uppercase letter
No blank spaces

Breach Check – Uses the Have I Been Pwned API
(with k-anonymity SHA1 hashing) to verify if your password has been leaked.
Character Breakdown – Counts uppercase, numbers, special characters, spaces.
Logging – Records attempts (obfuscated passwords, entropy, rule check, breach results) in logs.txt.
Streamlit UI – Clean and user-friendly web interface.

Tech Stack

Language: Python 3

Framework: Streamlit

Libraries:
hashlib → secure SHA1 hashing
requests → API calls
math → entropy calculation
string → character classification
datetime → logging

Installation

Clone the repository:
git clone https://github.com/sanjaysanju2504/Password-Checker.git
cd Password-Checker

Install dependencies:
pip install streamlit requests
Run the Streamlit app:
streamlit run app.py

Usage
Enter a password into the text field.
Click Check Password.

Review:
Entropy score
Character breakdown
Rule-based check results
Breach database results

Example:
Password: myPassword@123
Entropy Score: 42.75 bits
Result: Moderate – Better than average, but could improve.
Breach Check: Not Found

Future Improvements
Add password generation suggestions.
Include visual entropy gauge.
Provide real-time feedback as the user types.
Deploy on Streamlit Cloud / Heroku.

Contributing
Pull requests are welcome! Please open an issue first to discuss improvements or bug fixes.

License
This project is licensed under the MIT License 
