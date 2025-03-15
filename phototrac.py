import streamlit as st
import requests
import base64
import json
import pandas as pd
import folium
from streamlit_folium import folium_static

def get_geolocation(image_path, api_key):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    url = f"https://dev.geospy.ai/predict?image={encoded_string}&top_k=5"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.post(url, headers=headers)
    return response.json()

st.title("Photo Geolocation Finder")

api_key = st.text_input("Enter your API Key", type="password")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.read())
    
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    st.write("Fetching location data...")
    result = get_geolocation("temp_image.jpg", api_key)
    
    st.subheader("Results:")
    st.json(result)
    
    if "predictions" in result:
        locations = result["predictions"]
        
        st.subheader("Geolocation Map")
        
        map_type = st.selectbox("Select Map Type", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "CartoDB positron", "CartoDB dark_matter"])
        
        m = folium.Map(location=[0, 0], zoom_start=2, tiles=map_type)
        
        for loc in locations:
            lat, lon = loc["latitude"], loc["longitude"]
            folium.Marker([lat, lon], popup=f"{loc['name']}: {loc['score']}").add_to(m)
        
        folium_static(m)
