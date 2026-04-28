import streamlit as st

st.set_page_config(page_title="Investor Profile", layout="wide")

st.title("Investor Profile ")
st.write("Answer these questions to find out what type of investor you are.")
st.divider()

# Initialize score for each questionary
score = 0

# Question 1: Time Horizon
st.write("**Question 1:** How long until you need this money?")
time_horizon = st.radio(
    "Choose one:",
    ["Less than 3 years", "3-7 years", "7-15 years", "More than 15 years"],
    key="q1"
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

# Question 8: Monthly Investment Amount
st.write("**Question 8:** How much can you invest per month? (USD)")
monthly_amount = st.number_input("Enter amount:", min_value=0, max_value=100000, step=100, key="q8")
st.divider()

# Show progress
st.write(f"**Your Score: {score} / 28**")
st.progress(score / 28)

# Button to see results
if st.button("Show My Profile", type="primary", use_container_width=True):
    
    if monthly_amount == 0:
        st.warning("Please enter your monthly investment amount")
    else:
        # Determine profile based on score
        if score <= 10:
            profile = "Conservative"

            description = "You value safety over growth. You want predictable returns with minimal losses."

            allocation = "70% Bonds, 20% ETFs, 10% Cash"

            products = "- Government bonds\n- Bond ETFs (iShares, Vanguard)\n- High-yield savings accounts"

            avoid = "- Individual stocks\n- Crypto\n- Leverage/margin trading"

            monthly_plan = "Bonds: $" {int(monthly_amount * 0.7)} and " ETFs: $" {int(monthly_amount * 0.2)} and "Cash: $" {int(monthly_amount * 0.1)}
            
            

            pros = "- Sleep well at night\n- Unlikely to panic\n- Stable and predictable"
            cons = "- Low returns (2-4% yearly)\n- Inflation erodes value\n- May miss growth opportunities"
            
        elif score <= 14:
            profile = "Balanced"

            description = "You want both growth and safety. You accept some risk for better long-term returns."
            allocation = "50% Growth, 40% Bonds, 10% Cash"
            products = "- Index ETFs (VTI, VTSAX)\n- Bond ETFs (BND, VBTLX)\n- Dividend ETFs"
            avoid = "- Individual stocks (unless experienced)\n- Crypto/speculative assets\n- Frequent trading"
            monthly_plan = f"Growth: ${int(monthly_amount * 0.5):,}\nBonds: ${int(monthly_amount * 0.4):,}\nCash: ${int(monthly_amount * 0.1):,}"
            pros = "- Good growth (5-7% yearly)\n- Manageable volatility\n- Flexible and balanced"
            cons = "- May feel conflicted during crashes\n- Temptation to 'do something'\n- Less growth than aggressive"
            
        elif score <= 21:
            profile = "Growth-Focused"

            description = "You're return-oriented and handle volatility. You believe in long-term investing."
            allocation = "75% Growth, 20% Bonds, 5% Opportunistic"
            products = "- Total market ETF (VTI, ITOT)\n- Tech ETF (QQQ)\n- International ETF (VXUS)\n- Dividend stocks"
            avoid = "- Leverage/margin trading\n- Crypto (unless you understand it)\n- Over-concentrated bets\n- Day trading"
            monthly_plan = f"Growth: ${int(monthly_amount * 0.75):,}\nBonds: ${int(monthly_amount * 0.2):,}\nOpportunistic: ${int(monthly_amount * 0.05):,}"
            pros = "- High returns (8-10% yearly)\n- Weather downturns well\n- Build real wealth"
            cons = "- Experience 20-30% drops regularly\n- Requires discipline\n- Temptation to over-trade"
            
        else:
            profile = "Aggressive"

            description = "You chase maximum returns and handle major swings. You have real investment experience."
            allocation = "60% ETFs, 20% Growth Sectors, 10% Stocks, 5% Crypto, 5% Cash"
            products = "- Growth ETFs (QQQ, VUG)\n- Individual high-conviction stocks\n- Bitcoin/Ethereum (small portion)\n- Emerging markets ETF"
            avoid = "- Leverage (unless experienced)\n- Penny stocks\n- 100% crypto portfolio\n- All-in on single stocks"
            monthly_plan = f"Core ETFs: ${int(monthly_amount * 0.6):,}\nGrowth Sectors: ${int(monthly_amount * 0.2):,}\nIndividual Stocks: ${int(monthly_amount * 0.1):,}\nCrypto: ${int(monthly_amount * 0.05):,}\nCash: ${int(monthly_amount * 0.05):,}"
            pros = "- Potential 10-15%+ returns yearly\n- See downturns as opportunities\n- Not constrained by traditional assets"
            cons = "- Experience 40-50%+ drawdowns\n- Individual stock picks can fail\n- Requires discipline and risk management"
        
        # Display results
        st.success(f"Your Profile: {profile}")
        st.write(f"**Description:** {description}")
        st.divider()
        
        # Pros and Cons
        col1, col2 = st.columns(2)
        with col1:
            st.write("**✅ Strengths:**")
            st.write(pros)
        with col2:
            st.write("**⚠️ Challenges:**")
            st.write(cons)
        st.divider()
        
        # Allocation
        st.write("**Your Allocation:**")
        st.write(allocation)
        st.divider()
        
        # Products
        st.write("**Investment Products to Consider:**")
        st.write(products)
        st.divider()
        
        # What to Avoid
        st.write("**What to Avoid:**")
        st.write(avoid)
        st.divider()
        
        # Monthly Plan
        st.write(f"**Your Monthly Plan (${monthly_amount:,}):**")
        st.write(monthly_plan)
        st.divider()