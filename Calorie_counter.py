#Calorie Counter Application

import streamlit as st
import google.genai as genai
import os 
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    layout= "centered")

st.markdown("""
<h1 style="
    text-align:center;
    color:#606c38;
    font-size:48px;
    font-weight:800;
">
🏥 Calorie Counter
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* App background */
.stApp{
    background-color: white;
}

/* Main title */
.title{
    text-align:center;
    color:#606c38;
    font-size:50px;
    font-weight:600;
}

/* Subtitle */
.subtitle{
    text-align:center;
    color:#444;
    font-size:18px;
    font-weight:600;
}

/* All markdown labels */
[data-testid="stMarkdownContainer"] p{
    color:red;
    font-weight:bold;
    font-size:20px;
}

/* Text inside input boxes */
div[data-baseweb="input"] input{
    font-weight:bold;
}

/* Number input text */
input{
    font-weight:bold;
}

/* Selectbox text */
div[data-baseweb="select"]{
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

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
    country = st.text_input("Enter Your Country")

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

    response = client.models.generate_content(
    model = "gemini-3.5-flash",
    contents = prompt )
    st.write(response.text)