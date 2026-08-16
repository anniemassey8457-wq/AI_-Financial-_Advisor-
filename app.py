import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Financial Advisor", page_icon="💰")
st.title("💰 AI Financial Advisor - AIFA")
st.write("Get personalized financial advice using Google Gemini AI")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.5-flash')

    tab1, tab2 = st.tabs(["Personal Finance", "Goal Planning"])

    with tab1:
        st.header("Personal Financial Planning")
        income = st.number_input("Monthly Income (₹)", min_value=0)
        expenses = st.number_input("Monthly Expenses (₹)", min_value=0)
        savings = st.number_input("Current Savings (₹)", min_value=0)
        debt = st.number_input("Total Debt (₹)", min_value=0)

        if st.button("Get Financial Advice"):
    with st.spinner("Generating your financial advice..."):
        prompt = f"""Act as a financial advisor.
        Income: {income}, Expenses: {expenses}, Savings: {savings}, Debt: {debt}
        Give 3 budget tips, 2 saving tips, and 1 debt repayment strategy in simple points."""
        try:
            response = model.generate_content(prompt)
            st.success("Financial advice generated successfully!")
            st.write(response.text)
        except Exception as e:
            st.error("Sorry, we could not generate financial advice.")
            st.write(e)
    

    with tab2:
        st.header("Goal-Based Financial Planning")
        goal = st.text_input("What is your financial goal? e.g. Buy a home")
        goal_amount = st.number_input("Goal Amount (₹)", min_value=0)
        time_years = st.number_input("Time to achieve goal (years)", min_value=1)

        if st.button("Create Goal Plan"):
            prompt = f"""Act as a financial advisor. 
            Goal: {goal}, Amount: {goal_amount}, Time: {time_years} years.
            Calculate monthly savings needed and suggest 2 investment options. Give answer in points."""
            response = model.generate_content(prompt)
            st.write(response.text)
else:
    st.warning("Please enter your Gemini API Key in the sidebar to continue")
    
