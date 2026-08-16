import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Financial Advisor - AIFA")
st.write("Get personalized financial advice using Google Gemini AI")

# Session State
if "financial_advice" not in st.session_state:
    st.session_state.financial_advice = ""

if "goal_plan" not in st.session_state:
    st.session_state.goal_plan = ""

# Sidebar
st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input(
    "Enter your Gemini API Key",
    type="password"
)

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.5-flash")

    tab1, tab2 = st.tabs(["💰 Personal Finance", "🎯 Goal Planning"])

    # Personal Finance
    with tab1:
        st.header("Personal Financial Planning")

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0,
            value=0,
            step=1000
        )

        expenses = st.number_input(
            "Monthly Expenses (₹)",
            min_value=0,
            value=0,
            step=1000
        )

        savings = st.number_input(
            "Current Savings (₹)",
            min_value=0,
            value=0,
            step=1000
        )

        debt = st.number_input(
            "Total Debt (₹)",
            min_value=0,
            value=0,
            step=1000
        )

        if st.button("💡 Get Financial Advice"):
            if income <= 0:
                st.warning("Please enter your monthly income.")
            else:
                prompt = f"""
                Act as a financial advisor.

                Income: ₹{income}
                Expenses: ₹{expenses}
                Savings: ₹{savings}
                Debt: ₹{debt}

                Give:
                3 budget tips,
                2 saving tips,
                and 1 debt repayment strategy.

                Give the answer in simple points.
                """

                try:
                    with st.spinner("🤖 Generating your financial advice..."):
                        response = model.generate_content(prompt)

                    st.session_state.financial_advice = response.text
                    st.success("✅ Financial advice generated successfully!")

                except Exception as e:
                    st.error("❌ Unable to generate advice. Please check your API key and try again.")

        if st.session_state.financial_advice:
            st.subheader("📋 Your Financial Advice")
            st.write(st.session_state.financial_advice)

    # Goal Planning
    with tab2:
        st.header("🎯 Goal-Based Financial Planning")

        goal = st.text_input(
            "What is your financial goal? e.g. Buy a home"
        )

        goal_amount = st.number_input(
            "Goal Amount (₹)",
            min_value=0,
            value=0,
            step=1000
        )

        time_years = st.number_input(
            "Time to achieve goal (years)",
            min_value=1,
            value=1,
            step=1
        )

        if st.button("🎯 Create Goal Plan"):
            if goal == "":
                st.warning("Please enter your financial goal.")
            elif goal_amount <= 0:
                st.warning("Please enter a goal amount.")
            else:
                prompt = f"""
                Act as a financial advisor.

                Goal: {goal}
                Goal Amount: ₹{goal_amount}
                Time: {time_years} years

                Calculate the approximate monthly savings needed
                and suggest 2 suitable investment options.

                Give the answer in simple points.
                """

                try:
                    with st.spinner("🤖 Creating your personalized goal plan..."):
                        response = model.generate_content(prompt)

                    st.session_state.goal_plan = response.text
                    st.success("✅ Goal plan created successfully!")

                except Exception as e:
                    st.error("❌ Unable to create the goal plan. Please check your API key and try again.")

        if st.session_state.goal_plan:
            st.subheader("📋 Your Goal Plan")
            st.write(st.session_state.goal_plan)

else:
    st.info("🔑 Please enter your Gemini API Key in the sidebar to continue.")
