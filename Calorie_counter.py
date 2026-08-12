#Calorie Counter Application

import streamlit as st
import google.genai as genai
import os 
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
#page configration
st.set_page_config(
    layout= "centered",
    page_title= "Calorie Counter",
    page_icon= "🏥")

#CSS file loader function
def load_css():
    css_file = Path(__file__).parent / "style.css"

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()
#--------------------------------------------------------
#title markdown text
st.markdown("""
<h1 style="
    text-align:center;
    color:#606c38;
    font-size:55px;
    font-weight:800;
">
🏥 Calorie Counter
</h1>
""", unsafe_allow_html=True)


#subtitle markdown text
st.markdown("""
<p class="subtitle">BE YOUR BEST VERSION!</p>
""", unsafe_allow_html=True)


api_key = os.getenv("GOOGLE_API_KEY")

if api_key is None:
    api_key= st.secrets["GOOGLE_API_KEY"]

client = genai.Client(api_key = api_key) 

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Enter Your Weight (KG)**")
    wt = st.number_input("", key="weight")

with col2:
    st.markdown("**Enter Your Height (Meters)**")
    ht = st.number_input("", key="height")

col1, col2 = st.columns(2)

with col1:
    country = st.text_input("Enter Your Country").upper()

with col2:
    gender = st.selectbox(
        "Choose Your Gender",
        ["Male","Female","Other"]
    )


age = st.slider("Select Your Age",1,100)

goalWeight = st.number_input("Enter Your Goal Weight")

workout = st.radio("Do you workout", ["YES", "NO"])

if workout == "YES":
    workoutFeq = st.number_input("How Many Days You Workout")
else:
    workoutFeq = 0

ExceptionalDays = "None"

meal = st.selectbox("Choose Your Meal Type: ", ["Veg", "Nonveg"])

if meal == "Nonveg":
    meal_type = st.selectbox("Preference",["Fully-Non Vegeterian", "Partial-Non Vegeterian"])
    if meal_type == "Partial-Non Vegeterian":
        ExceptionalDays = st.text_input("Enter Days You Don't Eat Non-Veg: ")
        meal_type= "Partial Non-Veg"
    else:
        meal_type = "Non-Veg"
else:
    meal_type = "Full-Veg"

prompt = f"""You are a gym trainer and also a professional nutritionist consider this {wt} kg as weight , {ht} meters as height\n
{age} as age and {gender} as gender, and suggest a planned diet chart to achive this {goalWeight} kg goal weight, and also suggest \n
workouts considering {workoutFeq} no times I workout. Make sure diet plan should be {meal} and meal type {type} and exception of {ExceptionalDays}.\n
make sure the foods should be availble across {country}. Make the diet paln and the workout plan in simple words which can be understood easily and also \n
mention nutrient value for every food option you give.Try to make it a little shorter if you can not necessarily but if you can. """


if st.button("Get Healthier"):

    if wt <= 0 or ht <= 0:
        st.error("Please enter a valid weight and height.")

    else:
        with st.spinner("Creating your personalized calorie plan..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

        st.success("Your calorie plan is ready! 🎉")
        st.markdown(response.text)