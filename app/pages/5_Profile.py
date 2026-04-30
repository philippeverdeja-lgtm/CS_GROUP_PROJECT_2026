#this page is about the portfolio analyzer
#The questionary asks 7 questions + how much the user wants to invest
#every question give 1 to 4 points, the higher the points at the end, the higher the risk tolerance 


#this imports streamlit
import streamlit as st


#page configuration and titles
st.set_page_config(page_title="Investor Profile", layout="wide")

st.title("Investor Profile ")
st.write("Answer these questions to find out what type of investor you are.")


#home button
st.page_link("Home.py", label="Go to Homepage")


st.divider()


#monopoly man
st.markdown("""
    <style>
    .monopoly-man {
        position: fixed;
        top: 60px;
        right: 20px;
        width: 150px;
        z-index: 9999;
    }
    </style>
    <img class="monopoly-man" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWtleW5nNnJqdjA1aW5hODRsZGhzZzE5ZTJpcHRydDR4ZDU0Z21qayZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/C8976bDqhEUk40i8XU/giphy.gif">
""", unsafe_allow_html=True)

# Initialize score for each questionary to 0 every time
score = 0

# Question 1: Time Horizon
st.write("**Question 1:** How long until you need this money?")

#using st.radio alows to ask the question and so the user can select one answer
time_horizon = st.radio(
    "Choose one:",
    ["Less than 3 years", "3-7 years", "7-15 years", "More than 15 years"],  #here are the different answer posibilities
    key="q1"    #this is important because it stabilizes the qestionary, every widget has a unique key and stabilizes the widget's identity
                #and preserves its state when other parameters chenge
                #it basically makes sure that answer 1 stays in question 1, answer 2 in question 2 etc. so no values get mixed up
)


#here are the answers attributed to a number of points with a simple if function
if time_horizon == "Less than 3 years":
    score += 1
elif time_horizon == "3-7 years":
    score += 2
elif time_horizon == "7-15 years":
    score += 3
else:
    score += 4

#ever result is always added into the variable score

st.divider()

#the same is happening for all other questions up to question 7


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
monthly_amount = st.number_input("Enter amount:", min_value = 0, step = 100, key="q8") #this is not a st.radio anymore,

#here the user can put in his monthly amount he wants to invest the minimum value is 0, there is no max value for very rich people

#on the right of the intput there is a button that allows to add +100

#this is all stored in the variable "monthly_amount"


st.divider()


st.write(f"**Your Score: {score} / 28**")   #this just writes in numbers the score of the questionary 
st.progress(score / 28) #this shows graphically the result 


if st.button("Show My Profile", type="primary", width="stretch"):    # This is the button to see the results
    
    if monthly_amount == 0: # if the user didn't put in any amount, the appl blocks him before going furhter and shows an error message
                            #such that he must first enter any amount


        st.warning("Please enter your monthly investment amount")

        #if the amount is > 0 this goes:
    else:

#first level, concervative

            #based on each score there are different levels from low to high scores

        if score <= 10: #if the score after the questionary is higher than 10 the different variables 
                        # have these information in them


            profile = "Conservative" #this variable is the name of the profile

            description = "You value safety over growth. You want predictable returns with minimal losses."
            #this variable explains to the user what type of invesotr he is

            allocation = (
                f"- 70% Bonds\n"
                f"- 20% ETFs \n"
                f"- 10 Cash\n"
            )


            #this proposes a simple portfolio allocation

            products = "- Government bonds\n- Bond ETFs (iShares, Vanguard)\n- High-yield savings accounts"
            #this gives example of products the users could invest in

            avoid = "- Individual stocks\n- Crypto\n- Leverage/margin trading"
            #this gives the user advices on investments he should avoid

            monthly_plan = (
         f"- Bonds: $ {int(monthly_amount * 0.7)}\n"
         f"- ETFs: $ {int(monthly_amount * 0.2)}\n"
         f"- Cash: $ {int(monthly_amount * 0.1)}"
         )

         #this calculates a montly plan based on his monthly_amount he put in at the end of the questionary and stores
         #it in the variable monthly_plan 
         #the variable is put into integer to be calculated

                
            
            #the two last variables explains what are the pros and cons of this investment strategy and stores the description 
            #in their variables
            pros = "- Sleep well at night\n- Unlikely to panic\n- Stable and predictable"
            
            cons = "- Low returns (2-4% yearly)\n- Inflation erodes value\n- May miss growth opportunities"
            
            #the same is the repeated for all the other investor profiles / investment strategies



#second level, balanced

        elif score <= 14:
            profile = "Balanced"

            description = "You want both growth and safety. You accept some risk for better long-term returns."

            allocation = (
                f"- 50% Growth\n"
                f"- 40% Bonds\n"
                f"- 10% Cash\n"
            )
            

            
            products = "- Index ETFs (VTI, VTSAX)\n- Bond ETFs (BND, VBTLX)\n- Dividend ETFs"
            
            avoid = "- Individual stocks (unless experienced)\n- Crypto/speculative assets\n- Frequent trading"
                        
            monthly_plan = (
         f"- Growth: $ {int(monthly_amount * 0.5)}\n"
         f"- Bonds: $ {int(monthly_amount * 0.4)}\n"
         f"- Cash: $ {int(monthly_amount * 0.1)}"
         )

            pros = "- Good growth (5-7% yearly)\n- Manageable volatility\n- Flexible and balanced"
            
            cons = "- May feel conflicted during crashes\n- Temptation to 'do something'\n- Less growth than aggressive"
            

#third level, growth

        elif score <= 21:
            profile = "Growth-Focused"

            description = "You're return-oriented and handle volatility. You believe in long-term investing."
           
            allocation = (
                f"- 75% Growth\n"
                f"- 20% Bonds\n"
                f"- 5% Opportunistic"                    

            )
            
            

           
            products = "- Total market ETF (VTI, ITOT)\n- Tech ETF (QQQ)\n- International ETF (VXUS)\n- Dividend stocks"
           
            avoid = "- Leverage/margin trading\n- Crypto (unless you understand it)\n- Over-concentrated bets\n- Day trading"
                      
            monthly_plan = (
         f"- Growth: $ {int(monthly_amount * 0.75)}\n"
         f"- Bonds: $ {int(monthly_amount * 0.2)}\n"
         f"- Opportunistic: $ {int(monthly_amount * 0.05)}"
         )

            pros = "- High returns (8-10% yearly)\n- Weather downturns well\n- Build real wealth"
           
            cons = "- Experience 20-30% drops regularly\n- Requires discipline\n- Temptation to over-trade"
            

#fourth level, aggressive

        else:
            profile = "Aggressive"

            description = "You chase maximum returns and handle major swings. You have real investment experience."
            
            allocation = (
                f"- 60% ETFs\n"
                f"- 20% Growth Sectors\n"
                f"- 10% Stocks\n"
                f"- 5% Crypto\n"
                f"- 5% Cash"

            )
            

            
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
        



        # This the displays th results.$
        #since all the results are stored in different variables, here we just need to call them. Further since they are only 
        #assigned in the different score levels, at the end of the questionary, every variable is correctly assigned with the if
        #statements
        #ex.  score = 15 
        # first level is not assigned so program goes to the second level where all variables are assigned to the strings


        st.title(f"Your Profile: :blue[_{profile}_]") #title with cool text effect from variable profile
        st.write(f"**Description:** {description}") #variable description
        st.divider()
        
        # Here are the pros and cons with subheaders
        col1, col2 = st.columns(2)
        with col1:
            st.header(":green[**Strengths:**]")
            st.write(pros)     #here also the variable is just pulled and displayed as text
        with col2:
            st.header(":red[**Challenges:**]")
            st.write(cons)#same
        st.divider()
        
        # here is an portfolio allocation recommendantion
        st.header("**Proposed Portfolio Allocation:**")
        st.write(allocation) #same principle as the others
        st.divider()
        
        # Here are some propositions of products to integrate in the portfolio
        st.header("**Investment Products to Consider:**")
        st.write(products)# same as before
        st.divider()
        
        # Here are some recommendations of things to avoid
        st.header("**What to Avoid:**")
        st.write(avoid)#same
        st.divider()
        
        # Here is a recommendation of how much to invest in what each month
        st.header(f"**Your Monthly Plan (${monthly_amount:,}):**")
        st.markdown(monthly_plan)
        st.divider()
