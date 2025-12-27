# app.py
import streamlit as st
from credit_assistant_core import generate_policy_advice, parse_deepseek_output

st.set_page_config(page_title="Credit Policy Interpretation Assistant", layout="wide")
st.title("🏦 Credit Policy Interpretation Assistant")

# ---------------------------
# Input Form
# ---------------------------
with st.form("loan_form"):
    st.subheader("Applicant Details")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        loan_amount = st.number_input("Loan Amount ($)", min_value=0)
        term_months = st.number_input("Term (Months)", min_value=1)
        monthly_income = st.number_input("Monthly Income ($)", min_value=0)

    with col2:
        total_monthly_debt = st.number_input("Total Monthly Debt ($)", min_value=0)
        credit_score = st.number_input("Credit Score", min_value=0, max_value=850)
        collateral = st.text_input("Collateral")
        past_defaults = st.number_input("Past Defaults", min_value=0)

    policy_text = st.text_area("Policy Text / Guidelines (optional)")

    submitted = st.form_submit_button("Analyze Loan")

# ---------------------------
# Display Dashboard
# ---------------------------
if submitted:
    application = {
        "name": name,
        "loan_amount": loan_amount,
        "term_months": term_months,
        "monthly_income": monthly_income,
        "total_monthly_debt": total_monthly_debt,
        "credit_score": credit_score,
        "collateral": collateral,
        "past_defaults": past_defaults,
    }

    with st.spinner("Generating policy analysis..."):
        deepseek_text = generate_policy_advice(application, policy_text)
        result = parse_deepseek_output(deepseek_text)

    # ---------------------------
    # Dashboard Cards
    # ---------------------------
    st.subheader("Policy Interpretation & Risk Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Exceptions / Policy Violations:**")
        if result["Exceptions"]:
            st.markdown(
                f"<div style='color:red'>{result['Exceptions']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='color:green'>No exceptions detected</div>",
                unsafe_allow_html=True,
            )

        st.markdown("**Risks:**")
        if result["Risks"]:
            st.markdown(
                f"<div style='color:orange'>{result['Risks']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='color:green'>Low risk</div>", unsafe_allow_html=True
            )

    with col2:
        st.markdown("**Required Approval Authority:**")
        st.info(result["Required Approval"])

        st.markdown("**Explanation / Audit Notes:**")
        st.text_area("", result["Explanation"], height=250)

    # Full raw DeepSeek output (optional)
    with st.expander("Raw DeepSeek Output"):
        st.text(deepseek_text)
