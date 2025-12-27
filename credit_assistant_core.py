# credit_assistant_core.py
import ollama
import re


def generate_policy_advice(application, policy_text=""):
    """
    Generate explainable risk guidance using Ollama DeepSeek-R1:8B,
    including Debt-to-Income (DTI) ratio.
    """

    # Calculate DTI
    monthly_income = application.get("monthly_income", 1)
    total_monthly_debt = application.get("total_monthly_debt", 0)
    dti = round((total_monthly_debt / monthly_income) * 100, 2)

    prompt = f"""
You are a Credit Policy Interpretation Assistant for a bank.
You do NOT make final approval/rejection decisions.

Loan Application:
- Name: {application['name']}
- Loan Amount: ${application['loan_amount']}
- Term (Months): {application['term_months']}
- Monthly Income: ${application['monthly_income']}
- Total Monthly Debt: ${application['total_monthly_debt']}
- Debt-to-Income (DTI): {dti}%
- Credit Score: {application['credit_score']}
- Collateral: {application['collateral']}
- Past Defaults: {application['past_defaults']}

Bank Policy:
{policy_text if policy_text else "Use generic lending best practices."}

Tasks:
1. Highlight any potential policy exceptions.
2. Flag risks or concerns, including high DTI if applicable.
3. Suggest required approval authority (e.g., Branch Manager, Credit Committee).
4. Provide reasoning in clear human-readable text for audit purposes.
5. Suggest a final recommendation: Approve / Reject / Needs further review.
   - Only suggest based on policy and risk, but do NOT enforce a decision.

Output in structured form:
- Exceptions:
- Risks:
- Required Approval:
- Explanation:
- Suggested Decision:
"""

    # Call DeepSeek-R1:8B via Ollama
    response = ollama.chat(
        model="deepseek-r1:8b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2},
    )
    return response["message"]["content"]


def parse_deepseek_output(text):
    """
    Parse DeepSeek structured output into a dictionary
    """
    result = {
        "Exceptions": "",
        "Risks": "",
        "Required Approval": "",
        "Explanation": "",
        "Suggested Decision": "",
    }
    for key in result.keys():
        pattern = rf"{key}:(.*?)(?:- [A-Z]|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            result[key] = match.group(1).strip()
    return result
