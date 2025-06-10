import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64

# Add blurred background
def add_bg_from_local(image_file,blur=True):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    blur_css = "backdrop-filter: blur(6px);" if blur else ""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .top-box, .left-box {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 20px;
            margin: 2rem;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            {blur_css}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    

add_bg_from_local("background.jpg")

st.title("📱 Mobile Price Range Predictor")
# Your input + model prediction code goes here...


# Load trained model
model = joblib.load('model.pkl')  # Replace with your actual model filename
feature_names = joblib.load('feature_names.pkl')



# ----- Input fields -----
st.header("Enter Mobile Specifications")

ratings = st.slider("Ratings (1-5)", 1.0, 5.0, 4.0)
ram = st.number_input("RAM (in MB)", min_value=512, max_value=12000, value=4000)
rom = st.number_input("ROM (in MB)", min_value=1000, max_value=256000, value=64000)
mobile_size = st.slider("Screen Size (in inches)", 3.5, 7.0, 6.2)
battery_power = st.number_input("Battery Power (mAh)", min_value=800, max_value=6000, value=4000)

# ----- Brand selection -----
brands = [
    'BlackZone', 'Detel', 'Dublin', 'Easyfone', 'Ecotel', 'Micax', 'Muphone',
    'Mymax', 'Q-Tel', 'Salora', 'Samsung', 'Snexian', 'Ssky', 'Tork', 'Trio'
]

selected_brand = st.selectbox("Select Brand", brands)

# ----- One-hot encoding for brand -----
brand_encoded = {f'Brand_{b}': 0 for b in brands}
brand_encoded[f'Brand_{selected_brand}'] = 1

# ----- Final input dataframe -----
input_dict = {
    'Ratings': ratings,
    'RAM': ram,
    'ROM': rom,
    'Mobile_Size': mobile_size,
    'Battery_Power': battery_power,
    **brand_encoded
}

input_df = pd.DataFrame([input_dict])
# After building input_df:
input_df = input_df.reindex(columns=feature_names, fill_value=0)

# ----- Prediction -----
if st.button("Predict Price Range"):
    prediction = model.predict(input_df)
    st.success(f"Predicted Price Range: {prediction[0]}")

