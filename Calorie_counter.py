# Calorie Counter Application

import streamlit as st
import google.genai as genai
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    layout="centered",
    page_title="Calorie Counter",
    page_icon="🏥"
)


# =========================
# CSS FILE LOADER
# =========================

def load_css():
    css_file = Path(__file__).parent / "style.css"

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# =========================
# PAGE STATE
# =========================

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "plan_data" not in st.session_state:
    st.session_state["plan_data"] = {}

if "diet_plan" not in st.session_state:
    st.session_state["diet_plan"] = ""

if "swapped_plan" not in st.session_state:
    st.session_state["swapped_plan"] = ""

# =========================
# HOME PAGE
# =========================

if st.session_state["page"] == "home":

    st.markdown(
        '<h1 class="title">🏥 Calorie Counter</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Your Personal Health Assistant</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ New Plan", use_container_width=True):
            st.session_state["page"] = "new_plan"
            st.rerun()

    with col2:
        if st.button("⚖️ BMI Calculator", use_container_width=True):
            st.session_state["page"] = "bmi"
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✏️ Swap Meal", use_container_width=True):
            st.session_state["page"] = "meal_swap"
            st.rerun()

    with col2:
        if st.button("🛒 Grocery List", use_container_width=True):
            st.session_state["page"] = "grocery"
            st.rerun()


# =========================
# NEW PLAN PAGE
# =========================

elif st.session_state["page"] == "new_plan":

    if st.button("← Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()

    # Gemini API
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    if api_key is None:
        api_key = st.secrets["GOOGLE_API_KEY"]

    client = genai.Client(api_key=api_key)


    # New Plan title
    st.markdown(
        '<h1 class="title">🏥 Create Your Calorie Plan</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">BE YOUR BEST VERSION!</p>',
        unsafe_allow_html=True
    )


    # Weight and Height
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Enter Your Weight (KG)**")
        wt = st.number_input("", key="weight")

    with col2:
        st.markdown("**Enter Your Height (Meters)**")
        ht = st.number_input("", key="height")


    # Country and Gender
    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox("Country",["INDIA"])

    with col2:
        gender = st.selectbox(
            "Choose Your Gender",
            ["Male", "Female", "Other"]
        )


    # Age
    age = st.slider("Select Your Age", 1, 100)


    # Goal weight
    goalWeight = st.number_input("Enter Your Goal Weight")


    # Workout
    workout = st.radio(
        "Do you workout",
        ["YES", "NO"]
    )

    if workout == "YES":
        workoutFeq = st.number_input("How Many Days You Workout")
    else:
        workoutFeq = 0


    # Meal type
    ExceptionalDays = "None"

    meal = st.selectbox(
        "Choose Your Meal Type:",
        ["Veg", "Nonveg"]
    )

    if meal == "Nonveg":

        meal_type = st.selectbox(
            "Preference",
            ["Fully-Non Vegeterian", "Partial-Non Vegeterian"]
        )

        if meal_type == "Partial-Non Vegeterian":

            ExceptionalDays = st.text_input(
                "Enter Days Don't You Eat Non-Veg:"
            )

            meal_type = "Partial Non-Veg"

        else:
            meal_type = "Non-Veg"

    else:
        meal_type = "Full-Veg"


    # Gemini prompt
    prompt = f"""
    You are a gym trainer and also a professional nutritionist.
    Weight: {wt} kg
    Height: {ht} meters
    Age: {age}
    Gender: {gender}
    Goal Weight: {goalWeight} kg
    Workout Frequency: {workoutFeq}
    Meal: {meal}
    Meal Type: {meal_type}
    Exceptions: {ExceptionalDays}
    Country: {country}
    Suggest a planned diet chart to achieve the goal weight
    and also suggest workouts.Make sure the foods are available across {country}.
    Make the diet plan and workout plan simple and easy to understand.
    Mention the nutrient value for every food option.
    Try to keep the response reasonably short.
    """


    # Generate plan
    if st.button("Get Healthier"):

        if wt <= 0 or ht <= 0:
            st.error("Please enter a valid weight and height.")

        else:

            with st.spinner(
                "Creating your personalized calorie plan..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                st.session_state["diet_plan"] = response.text
                st.success("Your calorie plan is ready! 🎉")
                st.markdown(response.text)

# =========================
# BMI PAGE
# =========================

elif st.session_state["page"] == "bmi":

    if st.button("← Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()

    st.markdown(
        '<h1 class="title">⚖️ BMI Calculator</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Know Your BMI!</p>',
        unsafe_allow_html=True
    )

    # =========================
    # WEIGHT AND HEIGHT
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Enter Your Weight (KG)**")
        wt = st.number_input(
            "Weight",
            min_value=0.0,
            step=0.1,
            key="bmi_weight"
        )

    with col2:
        st.markdown("**Enter Your Height (Meters)**")
        ht = st.number_input(
            "Height",
            min_value=0.0,
            step=0.01,
            key="bmi_height"
        )

    # =========================
    # CALCULATE BUTTON
    # =========================

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        if st.button("Calculate BMI"):

            if wt <= 0:
                st.error("Please enter a valid weight.")

            elif ht <= 0:
                st.error("Please enter a valid height.")

            else:
                BMI = round(wt / (ht ** 2), 1)

                if BMI < 18.5:
                    category = "Under-weight"

                elif BMI < 25:
                    category = "Healthy-weight"

                elif BMI < 30:
                    category = "Over-weight"

                else:
                    category = "Obese-Class"

                # =========================
                # BMI RESULT BOX
                # =========================

                with st.container(border=True):

                    st.markdown(
    f"""
    <div class="bmi-box">
        <div class="bmi-title">Your BMI</div>
        <div class="bmi-value">{BMI:.1f}</div>
        <div class="bmi-category">{category}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# GROCERY LIST BUTTON
# =========================
elif st.session_state["page"] == "grocery":

    st.title("🛒 Grocery List")

    if st.button("← Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()

    if not st.session_state["diet_plan"]:

        st.warning("Please create a diet plan first.")

    else:

        if st.button("Get Grocery List"):

            api_key = os.getenv("GOOGLE_API_KEY")

            if api_key is None:
                api_key = st.secrets["GOOGLE_API_KEY"]

            client = genai.Client(api_key=api_key)

            grocery_prompt = f"""
            Read the following diet plan:

            {st.session_state["diet_plan"]}

            Extract the grocery items from this diet plan.

            Rules:
            - Use ONLY foods mentioned in the diet plan.
            - Do not add new foods.
            - Combine repeated items where possible.
            - Give quantities where mentioned.
            - Categorize the items.
            - Keep the grocery list simple.
            """

            with st.spinner("Preparing your grocery list..."):

                grocery_response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=grocery_prompt
                )

            st.subheader("🛒 Your Grocery List")
            st.markdown(grocery_response.text)

# =========================
# Swap Meal Button
# =========================

elif st.session_state["page"] == "meal_swap":
    st.subheader("🔄 Swap a Meal")

    if st.button("← Back to Home"):
        st.session_state["page"]="home"
        st.rerun()
    

    day = st.selectbox(
        "Select Day",
        [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
        ]
        )
    meal = st.selectbox(
        "Select Meal",
        [
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snacks"
        ]
        )
    if st.button("🔄 Find Alternatives"):

        if not st.session_state["diet_plan"]:
            st.warning("Please create a diet plan first.")

        else:

            st.write(f"You selected {meal} on {day}.")

            api_key = os.getenv("GOOGLE_API_KEY")

            if api_key is None:
                api_key = st.secrets["GOOGLE_API_KEY"]

            client = genai.Client(api_key=api_key)

            swap_prompt = f"""
            You are a professional nutritionist.

            The user has an existing diet plan:

            {st.session_state["diet_plan"]}

            The user wants to replace:

            Day: {day}
            Meal: {meal}

            Generate 3 alternative meals for the selected meal.

            Requirements:
            - Keep calories reasonably similar to the original meal.
            - Keep protein reasonably similar.
            - Foods should be easily available.
            - Do NOT change any other meal in the diet plan.
            - Give the approximate calories and protein for each alternative.
            - Keep the alternatives simple.

            Show the alternatives clearly so the user can choose one.
            """

            with st.spinner("Finding suitable alternatives..."):

                swap_response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=swap_prompt
                )

                st.subheader("🔄 Meal Alternatives")
                st.markdown(swap_response.text)