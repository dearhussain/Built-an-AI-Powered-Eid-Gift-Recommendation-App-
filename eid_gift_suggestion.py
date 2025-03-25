import streamlit as st
from langchain_community.llms import Together
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLM using Together AI
llm = Together(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    temperature=0.7
)

# ✅ Define a better prompt template (Fix: Remove placeholders, give clear instructions)
prompt_template = PromptTemplate(
    input_variables=["name", "gender", "age", "country", "interests", "specific_interest", "budget"],
    template=(
        "🌙 Assalamu Alaikum & Eid Mubarak! 🎉 May this Eid bring you joy, peace, and blessings.\n\n"
        "As a {age}-year-old {gender} from {country} who loves {interests}, especially {specific_interest}, "
        "I've selected three thoughtful Eid gifts within your budget of {budget}:\n\n"
        "🎁 Gift 1: A unique and thoughtful gift related to {specific_interest}. Provide a real example and a short reason why it's great.\n"
        "🎁 Gift 2: Another useful gift that matches {specific_interest}. Provide a real example and a short reason why it's great.\n"
        "🎁 Gift 3: One more amazing gift idea that fits {specific_interest}. Provide a real example and a short reason why it's great.\n\n"
        "Each of these gifts is carefully chosen to bring you joy on this special occasion. "
        "Wishing you a wonderful and blessed Eid! ✨\n\n"
        "Sincerely, Your AI Gift Advisor 🎁"
    ),
)

# Initialize the parser
parser = StrOutputParser()

# Streamlit UI
st.title("🎁 Personalized Eid Gift Suggestion")
st.write("Answer a few questions, and we'll suggest **three perfect Eid gifts** for you!")

# Collect user input
user_name = st.text_input("Enter your name:", placeholder="Your name here")
user_gender = st.selectbox("Select your gender:", ["Male", "Female"])
user_age = st.number_input("Enter your age:", min_value=5, max_value=100, step=1)
user_country = st.text_input("Enter your country:")
user_interests = st.multiselect("Select your interests:", ["Books", "Clothes", "Phones", "Accessories", "Gadgets", "Perfumes", "Other"])
budget_range = st.selectbox("Select your budget range:", ["Under $20", "$20-$50", "$50-$100", "Above $100"])

# Further refine specific interest
specific_interest = "General"
if "Books" in user_interests:
    specific_interest = st.selectbox("What type of books do you like?", ["Islamic", "Fiction", "Self-Help", "Biographies", "Educational"])
elif "Clothes" in user_interests:
    if user_gender == "Male":
        specific_interest = st.selectbox("What type of clothes do you prefer?", ["Casual", "Traditional", "Western", "Sportswear"])
    else:
        specific_interest = st.selectbox("What type of clothes do you prefer?", ["Abaya", "Party Wear", "Traditional", "Casual"])
elif "Phones" in user_interests:
    specific_interest = st.selectbox("What type of phone are you interested in?", ["Gaming", "Camera-focused", "Budget", "Flagship"])

# Generate Eid Gift Suggestions
if st.button("Generate Eid Gift Ideas"):
    if not user_name or not user_country or not user_interests:
        st.error("❌ Please fill in all required fields!")
    else:
        # ✅ Format the prompt with user inputs
        final_prompt = prompt_template.format(
            name=user_name,
            gender=user_gender,
            age=user_age,
            country=user_country,
            interests=", ".join(user_interests),
            specific_interest=specific_interest,
            budget=budget_range
        )
        
        # ✅ Call the model
        response = llm.invoke(final_prompt)

        # ✅ Display the response
        st.subheader("🎁 Personalized Eid Gift Suggestions:")
        st.write(response)
