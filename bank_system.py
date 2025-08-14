import streamlit as st
from datetime import datetime

# -------------------------------
# BankAccount Class (OOP)
# -------------------------------
class BankAccount:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance
        self.transactions = []  # Store transaction history

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append((datetime.now(), "Deposit", amount))
        return f"✅ ₹{amount} deposited successfully."

    def withdraw(self, amount):
        if amount > self.balance:
            return "❌ Insufficient funds."
        self.balance -= amount
        self.transactions.append((datetime.now(), "Withdraw", amount))
        return f"✅ ₹{amount} withdrawn successfully."

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transactions

# -------------------------------
# Streamlit App Config
# -------------------------------
st.set_page_config(page_title="Mini Banking System", layout="centered")
st.title("🏦 Mini Banking System")

# -------------------------------
# Session State Management
# -------------------------------
if "users" not in st.session_state:
    st.session_state.users = {}  # Dictionary of {name: BankAccount}
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# -------------------------------
# Tabs: Login/Register & Banking
# -------------------------------
tab1, tab2 = st.tabs(["🔐 Login / Register", "💼 Banking Dashboard"])

# -------------------------------
# Tab 1: Login / Register
# -------------------------------
with tab1:
    st.subheader("🔐 Login or Create Account")

    with st.form("auth_form"):
        name = st.text_input("Enter your name")
        pin = st.text_input("Enter a 4-digit PIN", type="password", max_chars=4)
        action = st.radio("Choose Action", ["Create Account", "Login"])
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name or not pin or not pin.isdigit() or len(pin) != 4:
                st.warning("⚠️ Please enter a valid name and 4-digit numeric PIN.")
            elif action == "Create Account":
                if name in st.session_state.users:
                    st.error("🚫 Account already exists. Please login.")
                else:
                    st.session_state.users[name] = BankAccount(name, pin)
                    st.session_state.logged_in_user = name
                    st.success(f"✅ Account created successfully! Welcome, {name}")
            elif action == "Login":
                user = st.session_state.users.get(name)
                if user and user.pin == pin:
                    st.session_state.logged_in_user = name
                    st.success(f"✅ Logged in successfully! Welcome back, {name}")
                else:
                    st.error("🚫 Invalid credentials. Please try again.")

# -------------------------------
# Tab 2: Banking Dashboard
# -------------------------------
with tab2:
    if st.session_state.logged_in_user:
        user = st.session_state.users[st.session_state.logged_in_user]
        st.subheader(f"👋 Welcome, {user.name}")

        operation = st.radio("Select Operation", ["Check Balance", "Deposit", "Withdraw", "Transaction History", "Logout"])

        if operation == "Check Balance":
            st.success(f"💳 Your current balance is ₹{user.get_balance():,.2f}")

        elif operation == "Deposit":
            amount = st.number_input("Enter deposit amount", min_value=0.0, step=100.0)
            if st.button("Deposit"):
                msg = user.deposit(amount)
                st.success(msg)

        elif operation == "Withdraw":
            amount = st.number_input("Enter withdrawal amount", min_value=0.0, step=100.0)
            if st.button("Withdraw"):
                msg = user.withdraw(amount)
                if "Insufficient" in msg:
                    st.error(msg)
                else:
                    st.success(msg)

        elif operation == "Transaction History":
            st.markdown("📜 **Recent Transactions**")
            history = user.get_transaction_history()
            if history:
                for time, action, amt in reversed(history[-10:]):
                    st.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action} of ₹{amt}")
            else:
                st.info("No transactions yet.")

        elif operation == "Logout":
            st.session_state.logged_in_user = None
            st.success("👋 Logged out successfully. See you again!")

    else:
        st.warning("🔒 Please login from the 'Login / Register' tab to access banking operations.")
