# Personalized-Workout-Diet-Planner-with-AI-AICTE-BATCH-7-

FitStudent AI Pro 🏋️‍♂️🥗

FitStudent AI Pro is a comprehensive, AI-powered fitness and nutrition assistant built specifically for college and university students. By leveraging the advanced text and vision capabilities of Google's Gemini 2.5 Flash, this application helps students stay healthy without breaking the bank or spending hours meal prepping.

🌟 Key Features

The application features a sleek, dark-themed UI with a sidebar navigation system, offering four distinct tools:

🏋️‍♂️ Standard Planner:

Calculates Total Daily Energy Expenditure (TDEE) based on user metrics.

Generates a personalized 1-day workout and meal plan.

Considers student-specific constraints like dietary preferences, available equipment (e.g., dorm room vs. full gym), and daily budget (in ₹ INR).

Exam Week Mode: A special toggle that forces the AI to suggest quick 15-minute workouts and brain-boosting study snacks.

Includes a downloadable text file option for offline viewing.

🍕 Dining Hall Survival:

Users input the random ingredients available in their campus cafeteria.

The AI generates creative, healthy, and macro-friendly meal combinations to keep diets on track.

📸 AI Fridge Scanner (Vision):

Users upload an image of the random ingredients in their mini-fridge or pantry.

The Gemini Vision model analyzes the image and suggests a quick, healthy recipe along with cooking times.

🍎 Calorie & Macro Estimator (Vision):

Users upload a picture of their plate/meal.

The AI identifies the food, estimates portion sizes, and provides a breakdown of total calories and macronutrients (Protein, Carbs, Fats).

🛠️ Tech Stack

Frontend & Framework: Streamlit (Python)

AI Engine: Google Generative AI (Gemini 2.5 Flash)

Image Processing: Pillow (PIL)

🚀 How to Run Locally

Clone the repository:

git clone [https://github.com/yourusername/fitstudent-ai-pro.git](https://github.com/yourusername/fitstudent-ai-pro.git)
cd fitstudent-ai-pro


Install dependencies:
Make sure you have Python installed, then run:

pip install -r requirements.txt


Get a Gemini API Key:
Get a free API key from Google AI Studio.

Run the app:

streamlit run app.py


Paste your API key into the app's sidebar to start generating plans!

🌐 Deployment

This app is fully optimized for deployment on Streamlit Community Cloud. Simply connect this repository to your Streamlit account, add your GEMINI_API_KEY to the Streamlit Secrets manager, and deploy!

Built for the Modern Student Journey. © 2026
