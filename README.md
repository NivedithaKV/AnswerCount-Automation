# AnswerCount-Automation
Automation script that simulates OTP login and dashboard data extraction for an internal company portal using Selenium.
# 🧠 SME Answer Submission Tracker (Selenium Automation Project)

This project is an internal tool automation designed to simplify the login and OTP handling process for an SME (Subject Matter Expert) portal and track the number of answers submitted on a particular date.

It demonstrates how Python + Selenium WebDriver can be used to automate:
- Dual-tab login flow (portal + webmail)
- OTP email detection & extraction
- Dashboard navigation
- Answer submission tracking by date

---

## 🚀 Features

✅ Automates login to internal SME portal  
✅ Fetches OTP from webmail automatically  
✅ Handles login error and OTP invalidation  
✅ Navigates to “My Past Work” dashboard  
✅ Counts how many answers were submitted on a given date

---

### 📁 Files Included

- `answer-count.py` – 💻 Main automation script
- `requirements.txt` – 📦 Python dependencies
- `README.md` – 📘 Documentation and setup guide
- `screenshots/` – 🖼️ *(Optional)* Folder for demo screenshots

---

## 🧰 Tech Stack

- Python 3.x  
- Selenium WebDriver  
- ChromeDriver  
- XPath & WebDriverWait  
- Regular Expressions (`re`)  
- Time module  

---

## ⚙️ How It Works

1. **Launch browser** and open SME portal  
2. **Login with email and password**  
3. Open **webmail tab**, login and monitor email  
4. Wait until **OTP email** arrives → extract 6-digit code  
5. Enter **OTP back into SME portal**  
6. Navigate to **“My Past Work” → “Question Solving”**  
7. Count all **answers submitted on the target date**  

---

## 🔐 Credentials Note

All email addresses, portals, and passwords in the code are **dummy placeholders**.  
Replace them with your internal test credentials **only in a secure local environment**.

---

## 🖼️ Sample Output Screenshot

*(Optional – add this if you want to show a screenshot)*  
![sample_output](screenshots/sample_output.png)

---

