import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FitStudent AI Pro",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE SETUP ---
if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = None
if "generated_dining" not in st.session_state:
    st.session_state.generated_dining = None
if "generated_fridge" not in st.session_state:
    st.session_state.generated_fridge = None
if "generated_calories" not in st.session_state:
    st.session_state.generated_calories = None

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b0f0c !important; 
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }

    .st-emotion-cache-12w0qpk, .st-emotion-cache-1r6slb0 {
        background-color: #161d18 !important; 
        border: 1px solid #232d26;
        border-radius: 15px;
        padding: 20px;
    }

    div.stButton > button[kind="primary"] {
        background-color: #00e676 !important; 
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 12px 30px !important;
        text-transform: uppercase;
        width: 100%;
        transition: transform 0.2s;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(0, 230, 118, 0.4);
    }

    div.stDownloadButton > button {
        background-color: #1c2620 !important;
        color: #00e676 !important;
        border: 1px solid #00e676 !important;
        border-radius: 30px !important;
        width: 100%;
    }

    .main-title { font-size: 3rem; font-weight: 800; color: #ffffff; margin-bottom: 0px; }
    .highlight-green { color: #00e676; }
    
    .section-header {
        font-size: 1.5rem; font-weight: 600; color: #ffffff;
        border-left: 4px solid #00e676; padding-left: 15px; margin: 20px 0;
    }

    .stTextInput input, .stSelectbox div, .stTextArea textarea, .stNumberInput input {
        background-color: #1c2620 !important; color: white !important;
        border-radius: 10px !important; border: 1px solid #333 !important;
    }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- GEMINI API SETUP ---
apiKey = os.environ.get("GEMINI_API_KEY", "")

with st.sidebar:
    st.title("⚙️ Settings & Tools")
    user_api_key = st.text_input("Enter Gemini API Key", value=apiKey, type="password")
    if user_api_key:
        genai.configure(api_key=user_api_key)
    
    st.divider()
    
    st.markdown("### Select Tool")
    app_mode = st.radio("App Mode", [
        "🏋️‍♂️ Standard Planner", 
        "🍕 Dining Hall Survival", 
        "📸 AI Fridge Scanner",
        "🍎 Calorie & Macro Estimator"
    ], label_visibility="collapsed")

# --- HELPER FUNCTIONS ---
def calculate_tdee(gender, weight_kg, height_cm, age, activity_level):
    if gender == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    multipliers = {
        "Sedentary (mostly sitting)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725
    }
    return int(bmr * multipliers[activity_level])

# --- AI GENERATION FUNCTIONS ---
def generate_standard_plan(goal, dietary, budget, equipment, tdee, exam_mode):
    model = genai.GenerativeModel('gemini-2.5-flash')
    exam_prompt = "THIS STUDENT IS IN EXAM WEEK. Keep workouts to 15-minute high-intensity sessions that can be done near a desk, and include healthy late-night study snacks." if exam_mode else ""
    
    prompt = f"""
    You are FitStudent AI, a professional fitness and nutrition coach.
    Create a personalized 1-day plan based on these constraints:
    - Primary Goal: {goal}
    - Calculated TDEE: ~{tdee} calories
    - Dietary Preference: {dietary}
    - Daily Food Budget: {budget}
    - Available Equipment: {equipment}
    
    {exam_prompt}

    Format the response strictly in Markdown:
    1. **Target Macros & Calories**
    2. **Workout of the Day**
    3. **Budget-Friendly Meals**
    4. **Auto-Grocery List**
    """
    return model.generate_content(prompt).text

def generate_dining_hall(ingredients):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"I am a college student. My dining hall currently has these items: {ingredients}. Generate 2 creative, healthy, and macro-friendly meal combinations I can make using ONLY these items. Give me the protein/carb/fat breakdown estimates for each."
    return model.generate_content(prompt).text

def generate_fridge_meal(image):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = "Look at the food items in this image. I am a busy college student. What is the quickest, healthiest meal I can cook using mostly what is visible here? Provide a brief recipe and estimated cooking time."
    return model.generate_content([prompt, image]).text

def estimate_calories(image):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = """
    Analyze this food image. Provide a highly structured breakdown including:
    1. **Identified Food Item(s):** 2. **Estimated Portion Size:** 3. **Estimated Total Calories:** 4. **Macronutrient Breakdown:** Estimate Protein (g), Carbohydrates (g), and Fats (g).
    """
    return model.generate_content([prompt, image]).text

# --- MAIN UI LAYOUT: ROUTING ---

if app_mode == "🏋️‍♂️ Standard Planner":
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<p class="main-title">Student-Specific <br><span class="highlight-green">Fitness, Powered by AI</span></p>', unsafe_allow_html=True)
        st.write("Personalized workout and diet plans that respect your budget, culture, and busy campus life.")
        
        st.markdown('<p class="section-header">1. Your Body Profile</p>', unsafe_allow_html=True)
        with st.container():
            c1, c2, c3, c4 = st.columns(4)
            p_gender = c1.selectbox("Gender", ["Male", "Female"])
            p_age = c2.number_input("Age", min_value=16, max_value=60, value=20)
            p_weight = c3.number_input("Weight (kg)", min_value=40, max_value=150, value=70)
            p_height = c4.number_input("Height (cm)", min_value=140, max_value=220, value=175)
            p_activity = st.selectbox("Current Activity Level", ["Sedentary (mostly sitting)", "Lightly Active (1-3 days/week)", "Moderately Active (3-5 days/week)", "Very Active (6-7 days/week)"])

        st.markdown('<p class="section-header">2. Plan Preferences</p>', unsafe_allow_html=True)
        with st.container():
            f_goal = st.selectbox("Primary Fitness Goal", ["Bulking", "Cutting", "Maintenance", "Strength Training"])
            f_diet = st.multiselect("Dietary Preferences", ["No Preference", "Vegan", "Halal", "Gluten-Free", "Vegetarian"])
            f_budget = st.selectbox("Daily Food Budget", ["₹150 - ₹300", "₹300 - ₹500", "₹500 - ₹1000", "₹1000+"])
            f_equip = st.radio("Available Equipment", ["Full Gym", "Home Gym / Dumbbells", "No Equipment (Bodyweight)"], horizontal=True)
            
            st.markdown("---")
            exam_week = st.toggle("🚨 Exam Week Mode (15-min workouts & study snacks)")
            
            generate_btn = st.button("Build My Plan Now", type="primary")

    with col2:
        st.image("https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1000&auto=format&fit=crop", caption="Optimized for Student Life", use_container_width=True)
        st.markdown("""
        <div style="background-color: #161d18; padding: 20px; border-radius: 15px; border: 1px solid #232d26;">
            <h4 style="color: #00e676; margin-top:0;">Pro Features Added:</h4>
            <p style="font-size: 0.9rem;">
            🔥 <b>TDEE Calculator:</b> Perfect calorie targets.<br>
            🍎 <b>Snap & Track:</b> Upload food pics for macros.<br>
            📚 <b>Exam Week Mode:</b> Quick workouts and brain food.<br>
            ⬇️ <b>Downloadable:</b> Save plans to your phone.</p>
        </div>
        """, unsafe_allow_html=True)

    if generate_btn:
        if not user_api_key:
            st.error("⚠️ Please provide a Gemini API key in the sidebar.")
        else:
            with st.spinner("Calculating macros and generating your custom student plan..."):
                tdee = calculate_tdee(p_gender, p_weight, p_height, p_age, p_activity)
                try:
                    st.session_state.generated_plan = generate_standard_plan(f_goal, f_diet, f_budget, f_equip, tdee, exam_week)
                except Exception as e:
                    st.error(f"API Error: {e}")

    if st.session_state.generated_plan:
        st.markdown('<p class="section-header">Your Personalized AI Plan</p>', unsafe_allow_html=True)
        st.markdown(st.session_state.generated_plan)
        
        st.download_button(
            label="💾 Download Plan as Text File",
            data=st.session_state.generated_plan,
            file_name="FitStudent_Plan.txt",
            mime="text/plain",
        )

elif app_mode == "🍕 Dining Hall Survival":
    st.markdown('<p class="main-title">Dining Hall <span class="highlight-green">Survival Mode</span></p>', unsafe_allow_html=True)
    dh_ingredients = st.text_area("What foods are available right now?", height=100)
    dh_btn = st.button("HACK MY MEAL", type="primary")
    
    if dh_btn:
        if not user_api_key:
            st.error("⚠️ Please provide a Gemini API key in the sidebar.")
        elif not dh_ingredients:
            st.warning("Please enter some ingredients first!")
        else:
            with st.spinner("Analyzing dining hall options..."):
                try:
                    st.session_state.generated_dining = generate_dining_hall(dh_ingredients)
                except Exception as e:
                    st.error(f"API Error: {e}")
                    
    if st.session_state.generated_dining:
        st.markdown('<p class="section-header">Your Cafeteria Hacks</p>', unsafe_allow_html=True)
        st.markdown(st.session_state.generated_dining)

elif app_mode == "📸 AI Fridge Scanner":
    st.markdown('<p class="main-title">AI <span class="highlight-green">Fridge Scanner</span></p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image of your ingredients", type=["jpg", "jpeg", "png"], key="fridge_upload")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Ingredients", width=400)
        scan_btn = st.button("SCAN AND COOK", type="primary")
        
        if scan_btn:
            if not user_api_key:
                st.error("⚠️ Please provide a Gemini API key in the sidebar.")
            else:
                with st.spinner("Gemini is looking at your fridge..."):
                    try:
                        st.session_state.generated_fridge = generate_fridge_meal(image)
                    except Exception as e:
                        st.error(f"API Error: {e}")
                        
        if st.session_state.generated_fridge:
            st.markdown('<p class="section-header">Recipe Suggestion</p>', unsafe_allow_html=True)
            st.markdown(st.session_state.generated_fridge)

elif app_mode == "🍎 Calorie & Macro Estimator":
    st.markdown('<p class="main-title">Snap & <span class="highlight-green">Track Macros</span></p>', unsafe_allow_html=True)
    food_file = st.file_uploader("Upload an image of your meal", type=["jpg", "jpeg", "png"], key="calorie_upload")
    
    if food_file is not None:
        food_image = Image.open(food_file)
        st.image(food_image, caption="Your Meal", width=400)
        analyze_btn = st.button("ESTIMATE CALORIES & MACROS", type="primary")
        
        if analyze_btn:
            if not user_api_key:
                st.error("⚠️ Please provide a Gemini API key in the sidebar.")
            else:
                with st.spinner("Analyzing food items and calculating macros..."):
                    try:
                        st.session_state.generated_calories = estimate_calories(food_image)
                    except Exception as e:
                        st.error(f"API Error: {e}")
                        
        if st.session_state.generated_calories:
            st.markdown('<p class="section-header">Nutritional Breakdown</p>', unsafe_allow_html=True)
            st.markdown(st.session_state.generated_calories)

# Footer
st.divider()
st.caption("FitStudent AI Pro © 2026")