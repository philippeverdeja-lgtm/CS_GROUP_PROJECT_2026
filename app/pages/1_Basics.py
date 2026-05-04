"""
This code is part of the Computer Science Project of group 11.05:
Philippe Verdeja, Yannick Hafner, Remi de la Fortelle, Mara Ciglia and Sam Pellaud.
It contains the "Basics"-page, an educational guide split into core concepts, asset types and getting-started tips.
The idea is to give a beginner the foundation he needs to understand investing before using the rest of the website.
On top of that, the page covers compound interest, risk levels and diversification with concrete examples in plain language.
"""

# Import streamlit
import streamlit as st

# Page configuration, title, subtitle and tab icon (logo without text)
# Logo and tab icon by Claude
st.set_page_config(
    page_title="Investment Basics",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjAgMzYwIj48cmVjdCB3aWR0aD0iMzYwIiBoZWlnaHQ9IjM2MCIgcng9IjUwIiBmaWxsPSIjMGQxYjJhIi8+PHJlY3QgeD0iNjAiIHk9IjE4MCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjE1MCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIxNTIiIHk9IjIzMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjEwMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIyNDQiIHk9IjEyMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjIxMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cG9seWxpbmUgcG9pbnRzPSIzNSwyNjAgODcuNSwxODAgMTc5LjUsMjMwIDI4NSwxMDgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzFmOGZmZiIgc3Ryb2tlLXdpZHRoPSIxNCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjg1LDEwOCkgcm90YXRlKC00MS42MykiPjxwb2x5Z29uIHBvaW50cz0iLTI2LC0yMiAyMiwwIC0yNiwyMiIgZmlsbD0iIzFmOGZmZiIgc3Ryb2tlPSIjMWY4ZmZmIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L2c+PC9zdmc+",
    layout="wide"
)

# Title and subtitle of the page
st.title("Investment Basics")
st.markdown("Learn the fundamentals. Grow your money.")


#This is a button to return to the homepage
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

#two introducion columns
col1, col2 = st.columns(2)

#basic intoduciton
with col1:
    st.markdown("""This guide covers the core concepts you need to understand investing and personal finance. 
    Everything here builds on simple ideas.""")


#text effect with st.info and **
with col2:
    st.info("**Pro tip:** Understanding *why* money grows matters more than memorizing formulas.")

st.divider()



# Bullet points of what the app does
st.subheader("What This App Does")
st.markdown("""
With this app you can:
- **Understand** the fundamentals of investing
- **Create** a new portfolio
- **Analyze** your existing portfolio
- **Compare** different companies side by side
- **Find** your investor profile
- **Stay informed** with the most important news
""")

st.divider()

#Here are the core concepts in two columns and titles and different text formats
st.subheader("Core Concepts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Time, Money & Inflation")
    st.markdown("""
    Money today is worth more than money tomorrow! You can invest it to earn interst (more money) today!

    If you invest \$100 today, they might become \$108 in one year. If you keep \$100 in your pocket, they still are \$100 one year from now. The money you're not earning by not investing is called **opportunity cost**.

    You also have to keep in mind that every year **your money loses value** due to **inflation**!

    If you have \$100 today you can buy 100 apples but one year later, your \$100 might only buy 98 apples! Investments are one way of escaping inflation!

    """)

with col2:
    st.markdown("### Interest")
    st.markdown("""
    Interest is what you earn when you lend money or invest it. Think of it as "rent" paid for using your money.
    
    **Simple interest:** You earn the same amount every year.
    
    **Compound interest:** You earn interest on your original money **AND** on the interest already earned. This gets exponential fast.
    """)

st.divider()

col1, col2 = st.columns(2)


#in two columns, concept of risk
with col1:
    st.markdown("### Risk & Return")
    st.markdown("""
    Safe investments (bonds, savings accounts) grow slowly but reliably.
    
    Riskier investments (stocks, crypto) can grow fast but can also lose money.
    
    You can't have both high returns *and* no risk.
    """)
    


with col2:
    st.markdown("### Diversification")
    st.markdown("""
    Don't put all your eggs in one basket.
    
    By spreading money across different types of investments (stocks, bonds, cash), 
    you reduce the damage if one investment tanks.
    """)

st.divider()

# Asset types
st.subheader("Types of Investments")


#with st.tabs i can create different tabs such that the user can navigate through them

tabs = st.tabs(["Stocks", "Bonds", "ETFs", "Cash"],)

with tabs[0]:
    st.markdown("""
    **What they are:** A piece of ownership in a company.
    
    **How you make money:**
    - **Capital gains:** Stock price goes up, you sell for profit
    - **Dividends:** Company pays you a portion of profits
    
    **Risk level:** Medium to high (can lose money short-term, but historically grow long-term)
    
    **Time horizon:** 5+ years recommended
    
    **Example:** You own 10 shares of Apple at \$150/share = \$1,500 invested. 
    If it rises to $200, you have \$2,000 (gain of $500).
    """)

with tabs[1]:
    st.markdown("""
    **What they are:** A loan you give to a company or government. They promise to pay you back with interest.
    
    **How you make money:**
    - **Interest payments:** Regular payments while you hold the bond
    - **Principal:** Get your money back when the bond matures
    
    **Risk level:** Low to medium (safer than stocks, but less growth potential)
    
    **Time horizon:** Varies (can be 1 year to 30+ years)
    
    **Example:** Buy a government bond for $1,000 at 3% annual interest. 
    You get $30/year for 10 years, then get your $1,000 back.
    """)

with tabs[2]:
    st.markdown("""
    **What they are:** A basket of stocks or bonds bundled together. One fund might contain 500 different companies.
    
    **How you make money:** Same as stocks/bonds, but diversified.
    
    **Why they're great:**
    - **Instant diversification:** Own dozens or hundreds of companies with one purchase
    - **Low fees:** Usually cheaper than picking individual stocks
    - **Less stress:** Less likely to lose everything if one company fails
    
    **Risk level:** Low to medium (depends on what's in the ETF)
    
    **Example:** VWRL is a global ETF that owns thousands of stocks across 45+ countries. 
    One share gives you exposure to the whole world.
    """)

with tabs[3]:
    st.markdown("""
    **What they are:** Money in a savings account or money market fund. The safest option.
    
    **How you make money:** Interest earned from the bank (usually very low, 1-4% depending on the bank).
    
    **Why it matters:** Cash is your emergency fund. Don't invest money you need within 2 years.
    
    **Risk level:** Virtually zero (banks are insured up to certain limits)
    
    **Downside:** Doesn't keep up with inflation, so you slowly lose buying power over decades.
    """)

st.divider()

# Compound interest example
st.subheader("Why Compound Interest is Magic")

st.markdown("""
This is the single most important concept in personal finance. Let me show you why.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Scenario:** Invest 10,000 CHF at 7% annual return")
    
    years_data = {
        "Year": [1, 5, 10, 20, 30],
        "Value": [10_700, 14_026, 19_672, 38_697, 76_123],
        "Growth": [700, 4_026, 9_672, 28_697, 66_123]
    }
    
    import pandas as pd
    df = pd.DataFrame(years_data)
    
    st.dataframe(
        df.style.format({
            "Value": "CHF {:,.0f}",
            "Growth": "CHF {:,.0f}"
        }),
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.markdown("""
    Notice:
    - After 10 years: roughly doubled (10k → 19.6k)
    - After 20 years: roughly quadrupled (10k → 38.6k)
    - After 30 years: roughly 7.6x (10k → 76k)
    
    You only added 10,000 CHF once. The rest came from compound growth.
    
    **Key insight:** Time is your most valuable asset when you're young. 
    Starting 10 years earlier nearly doubles your final wealth.
    """)

st.info("📌 This is why starting early (even with small amounts) beats starting late with big amounts.")

st.markdown("---")

# Risk tiers
st.subheader("Risk Levels Explained")

risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:
    st.markdown("### 🟢 Low Risk")
    st.markdown("""
    **Investments:** Cash, bonds, stable funds
    
    **Annual return:** 1-4%
    
    **Best for:** Money you need within 2 years, or if you can't sleep at night losing 10%
    
    **Downside:** Barely beats inflation
    """)

with risk_col2:
    st.markdown("### 🟡 Medium Risk")
    st.markdown("""
    **Investments:** Balanced ETFs (60% stocks, 40% bonds)
    
    **Annual return:** 5-7%
    
    **Best for:** Most people with a 5-10 year horizon
    
    **Downside:** You'll see 15-20% drops sometimes
    """)

with risk_col3:
    st.markdown("### 🔴 High Risk")
    st.markdown("""
    **Investments:** 100% stocks, growth ETFs, individual stocks
    
    **Annual return:** 8-12%+ (or losses)
    
    **Best for:** People who won't panic if markets drop 40%
    
    **Downside:** Could lose half your money in bad years
    """)

st.markdown("---")

# Getting started
st.subheader("Getting Started")

st.markdown("""
1. **Decide your time horizon.** When do you need this money?
   - Less than 2 years? → Stay in cash
   - 5-10 years? → Medium risk (balanced fund)
   - 10+ years? → Can handle more risk (stock-heavy)

2. **Choose your strategy.** Most people benefit from:
   - **Dollar-cost averaging (DCA):** Invest the same amount every month, regardless of price
   - **Buy and hold:** Invest lump sum, ignore short-term noise
   - **Rebalance annually:** Keep your allocation stable over time

3. **Start small.** Even 100 CHF/month compounds into serious wealth.

4. **Don't panic sell.** Biggest mistake people make? Selling when markets crash.
   The market always recovers. History shows it.
""")

st.success("💪 You now understand the basics. Ready to experiment with the Portfolio Analyzer?")
