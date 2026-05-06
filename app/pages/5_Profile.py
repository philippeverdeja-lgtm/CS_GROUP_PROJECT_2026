"""
This code is part of the Computer Science Project of group 11.05:
Philippe Verdeja, Yannick Hafner, Remi de la Fortelle, Mara Ciglia and Sam Pellaud.
It contains the "Profile"-page, built around a 7-question questionnaire plus an investment amount.
The idea is to give the user a quick way to find out what type of investor he is.
Each question gives 1 to 4 points and the higher the total at the end, the higher the user's risk tolerance.
"""
 
import streamlit as st
 
# Page configuration, title, subtitle and tab icon (logo without text)
# Logo and tab icon by Claude
st.set_page_config(
    page_title="Profile",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjAgMzYwIj48cmVjdCB3aWR0aD0iMzYwIiBoZWlnaHQ9IjM2MCIgcng9IjUwIiBmaWxsPSIjMGQxYjJhIi8+PHJlY3QgeD0iNjAiIHk9IjE4MCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjE1MCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIxNTIiIHk9IjIzMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjEwMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIyNDQiIHk9IjEyMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjIxMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cG9seWxpbmUgcG9pbnRzPSIzNSwyNjAgODcuNSwxODAgMTc5LjUsMjMwIDI4NSwxMDgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzFmOGZmZiIgc3Ryb2tlLXdpZHRoPSIxNCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjg1LDEwOCkgcm90YXRlKC00MS42MykiPjxwb2x5Z29uIHBvaW50cz0iLTI2LC0yMiAyMiwwIC0yNiwyMiIgZmlsbD0iIzFmOGZmZiIgc3Ryb2tlPSIjMWY4ZmZmIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L2c+PC9zdmc+",
    layout="wide"
)
 
st.title("Investor Profile")
st.write("Answer these questions to find out what type of investor you are.")
 
st.page_link("Home.py", label="Go to Homepage")
st.divider()
 
# Adds the logo of our website at the top right corner
st.markdown("""
    <style>
    .easy-investing-logo {
        position: fixed;
        top: 60px;
        right: 20px;
        width: 130px;
        z-index: 9999;
    }
    </style>
    <div class="easy-investing-logo">
        <svg viewBox="0 0 680 500" xmlns="http://www.w3.org/2000/svg">
            <rect x="160" y="40" width="360" height="360" rx="50" fill="#0d1b2a"/>
            <rect x="220" y="220" width="55" height="150" rx="4" fill="#ffffff"/>
            <rect x="312" y="270" width="55" height="100" rx="4" fill="#ffffff"/>
            <rect x="404" y="160" width="55" height="210" rx="4" fill="#ffffff"/>
            <polyline points="195,300 247.5,220 339.5,270 445,148"
                      fill="none" stroke="#1f8fff" stroke-width="14"
                      stroke-linecap="round" stroke-linejoin="round"/>
            <g transform="translate(445,148) rotate(-41.63)">
                <polygon points="-26,-22 22,0 -26,22" fill="#1f8fff"
                         stroke="#1f8fff" stroke-width="6" stroke-linejoin="round"/>
            </g>
            <text x="340" y="465" font-size="58" font-weight="800"
                  text-anchor="middle" letter-spacing="-1"
                  font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif">
                <tspan fill="#1f8fff">Easy</tspan><tspan fill="#ffffff"> Investing</tspan>
            </text>
        </svg>
    </div>
""", unsafe_allow_html=True)
 
# Score starts at 0 and accumulates across all questions
score = 0
 
# Question 1: Time Horizon
st.write("**Question 1:** How long until you need this money?")
time_horizon = st.radio(
    "Choose one:",
    ["Less than 3 years", "3-7 years", "7-15 years", "More than 15 years"],
    key="q1"  # unique key to preserve widget state across reruns
)
 
if time_horizon == "Less than 3 years":
    score += 1
elif time_horizon == "3-7 years":
    score += 2
elif time_horizon == "7-15 years":
    score += 3
else:
    score += 4
 
st.divider()
 
# Question 2: Financial Cushion
st.write("**Question 2:** If you lost your job, how long could you survive without selling your investments?")
cushion = st.radio(
    "Choose one:",
    ["Less than 3 months", "3-6 months", "6-12 months", "More than 12 months"],
    key="q2"
)
 
if cushion == "Less than 3 months":
    score += 1
elif cushion == "3-6 months":
    score += 2
elif cushion == "6-12 months":
    score += 3
else:
    score += 4
 
st.divider()
 
# Question 3: Loss Tolerance
st.write("**Question 3:** Your portfolio drops 20% in one month. What do you do?")
loss_tolerance = st.radio(
    "Choose one:",
    ["Sell everything, too risky!", "Sell some to reduce loss", "Wait it out", "Buy more, great opportunity!"],
    key="q3"
)
 
if loss_tolerance == "Sell everything, too risky!":
    score += 1
elif loss_tolerance == "Sell some to reduce loss":
    score += 2
elif loss_tolerance == "Wait it out":
    score += 3
else:
    score += 4
 
st.divider()
 
# Question 4: Investment Goal
st.write("**Question 4:** What's your main investment goal?")
goal = st.radio(
    "Choose one:",
    ["Keep money safe", "Generate regular income", "Build wealth over time", "Maximum returns at any cost"],
    key="q4"
)
 
if goal == "Keep money safe":
    score += 1
elif goal == "Generate regular income":
    score += 2
elif goal == "Build wealth over time":
    score += 3
else:
    score += 4
 
st.divider()
 
# Question 5: Experience
st.write("**Question 5:** How much investing experience do you have?")
experience = st.radio(
    "Choose one:",
    ["None, complete beginner", "Savings account or funds", "Trade stocks or ETFs", "Options, leverage, derivatives"],
    key="q5"
)
 
if experience == "None, complete beginner":
    score += 1
elif experience == "Savings account or funds":
    score += 2
elif experience == "Trade stocks or ETFs":
    score += 3
else:
    score += 4
 
st.divider()
 
# Question 6: Monthly Investment Capacity
st.write("**Question 6:** What % of monthly income can you invest comfortably?")
capacity = st.radio(
    "Choose one:",
    ["Less than 5%", "5-15%", "15-30%", "More than 30%"],
    key="q6"
)
 
if capacity == "Less than 5%":
    score += 1
elif capacity == "5-15%":
    score += 2
elif capacity == "15-30%":
    score += 3
else:
    score += 4
 
st.divider()
 
# Question 7: Emotional Resilience
st.write("**Question 7:** Your gains go up 30%, then back to zero. How do you feel?")
emotion = st.radio(
    "Choose one:",
    ["Very frustrated, loss feels real", "Disappointed but ok", "Annoyed but learnt something", "No problem, long term will recover"],
    key="q7"
)
 
if emotion == "Very frustrated, loss feels real":
    score += 1
elif emotion == "Disappointed but ok":
    score += 2
elif emotion == "Annoyed but learnt something":
    score += 3
else:
    score += 4
 
st.divider()
 
# Question 8: Monthly Investment Amount (number input instead of radio)
st.write("**Question 8:** How much can you invest per month? (USD)")
monthly_amount = st.number_input("Enter amount:", min_value=0, step=100, key="q8")
 
st.divider()
 
# Score display with progress bar
st.write(f"**Your Score: {score} / 28**")
st.progress(score / 28)
 
if st.button("Show My Profile", type="primary", width="stretch"):
 
    if monthly_amount == 0:
        st.warning("Please enter your monthly investment amount")
    else:
 
        # Conservative: score 7-10
        if score <= 10:
            profile = "Conservative"
            description = "You value safety over growth. You want predictable returns with minimal losses."
            allocation = "- 70% Bonds\n- 20% ETFs\n- 10% Cash"
            products = "- Government bonds\n- Bond ETFs (iShares, Vanguard)\n- High-yield savings accounts"
            avoid = "- Individual stocks\n- Crypto\n- Leverage/margin trading"
            monthly_plan = (
                f"- Bonds: $ {int(monthly_amount * 0.7)}\n"
                f"- ETFs: $ {int(monthly_amount * 0.2)}\n"
                f"- Cash: $ {int(monthly_amount * 0.1)}"
            )
            pros = "- Sleep well at night\n- Unlikely to panic\n- Stable and predictable"
            cons = "- Low returns (2-4% yearly)\n- Inflation erodes value\n- May miss growth opportunities"
 
        # Balanced: score 11-14
        elif score <= 14:
            profile = "Balanced"
            description = "You want both growth and safety. You accept some risk for better long-term returns."
            allocation = "- 50% Growth\n- 40% Bonds\n- 10% Cash"
            products = "- Index ETFs (VTI, VTSAX)\n- Bond ETFs (BND, VBTLX)\n- Dividend ETFs"
            avoid = "- Individual stocks (unless experienced)\n- Crypto/speculative assets\n- Frequent trading"
            monthly_plan = (
                f"- Growth: $ {int(monthly_amount * 0.5)}\n"
                f"- Bonds: $ {int(monthly_amount * 0.4)}\n"
                f"- Cash: $ {int(monthly_amount * 0.1)}"
            )
            pros = "- Good growth (5-7% yearly)\n- Manageable volatility\n- Flexible and balanced"
            cons = "- May feel conflicted during crashes\n- Temptation to 'do something'\n- Less growth than aggressive"
 
        # Growth-Focused: score 15-21
        elif score <= 21:
            profile = "Growth-Focused"
            description = "You're return-oriented and handle volatility. You believe in long-term investing."
            allocation = "- 75% Growth\n- 20% Bonds\n- 5% Opportunistic"
            products = "- Total market ETF (VTI, ITOT)\n- Tech ETF (QQQ)\n- International ETF (VXUS)\n- Dividend stocks"
            avoid = "- Leverage/margin trading\n- Crypto (unless you understand it)\n- Over-concentrated bets\n- Day trading"
            monthly_plan = (
                f"- Growth: $ {int(monthly_amount * 0.75)}\n"
                f"- Bonds: $ {int(monthly_amount * 0.2)}\n"
                f"- Opportunistic: $ {int(monthly_amount * 0.05)}"
            )
            pros = "- High returns (8-10% yearly)\n- Weather downturns well\n- Build real wealth"
            cons = "- Experience 20-30% drops regularly\n- Requires discipline\n- Temptation to over-trade"
 
        # Aggressive: score 22-28
        else:
            profile = "Aggressive"
            description = "You chase maximum returns and handle major swings. You have real investment experience."
            allocation = "- 60% ETFs\n- 20% Growth Sectors\n- 10% Stocks\n- 5% Crypto\n- 5% Cash"
            products = "- Growth ETFs (QQQ, VUG)\n- Individual high-conviction stocks\n- Bitcoin/Ethereum (small portion)\n- Emerging markets ETF"
            avoid = "- Leverage (unless experienced)\n- Penny stocks\n- 100% crypto portfolio\n- All-in on single stocks"
            monthly_plan = (
                f"- ETFs: $ {int(monthly_amount * 0.6)}\n"
                f"- Growth Sectors: $ {int(monthly_amount * 0.2)}\n"
                f"- Individual Stocks: $ {int(monthly_amount * 0.1)}\n"
                f"- Crypto: $ {int(monthly_amount * 0.05)}\n"
                f"- Cash: $ {int(monthly_amount * 0.05)}"
            )
            pros = "- Potential 10-15%+ returns yearly\n- See downturns as opportunities\n- Not constrained by traditional assets"
            cons = "- Experience 40-50%+ drawdowns\n- Individual stock picks can fail\n- Requires discipline and risk management"
 
        # Display results
        st.title(f"Your Profile: {profile}")
        st.write(f"**Description:** {description}")
        st.divider()
 
        col1, col2 = st.columns(2)
        with col1:
            st.header("**Strengths:**")
            st.write(pros)
        with col2:
            st.header("**Challenges:**")
            st.write(cons)
        st.divider()
 
        st.header("**Proposed Portfolio Allocation:**")
        st.write(allocation)
        st.divider()
 
        st.header("**Investment Products to Consider:**")
        st.write(products)
        st.divider()
 
        st.header("**What to Avoid:**")
        st.write(avoid)
        st.divider()
 
        st.header(f"**Your Monthly Plan (${monthly_amount:,}):**")
        st.markdown(monthly_plan)
        st.divider()
