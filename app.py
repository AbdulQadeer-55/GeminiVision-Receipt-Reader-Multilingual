import streamlit as st
import os
import pathlib
from PIL import Image
import google.generativeai as genai

def init_styles():
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
            padding: 2rem;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 2rem;
            border-radius: 25px;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .css-1v0mbdj.etr89bj1 {
            border-radius: 10px;
            border: 2px solid #e6e6e6;
            padding: 1rem;
        }
        .css-1v0mbdj.etr89bj1:hover {
            border-color: #4CAF50;
        }
        h1 {
            color: #2E4057;
            font-family: 'Helvetica Neue', sans-serif;
            text-align: center;
            margin-bottom: 2rem;
        }
        .footer {
            text-align: center;
            padding: 2rem;
            color: #666;
        }
        .user-info {
            text-align: right;
            color: #666;
            font-style: italic;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    raise FileNotFoundError("No file uploaded")

def main():
    # Direct API key configuration
    GOOGLE_API_KEY = "AIzaSyCiaqnFfhMe0Acscy8MgaF69kioayPX3GY"
    genai.configure(api_key=GOOGLE_API_KEY)
    
    init_styles()
    
    st.markdown("<h1>🤖 Advanced Image Analysis Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<div class='user-info'>Developed by Abdul Qadeer</div>", unsafe_allow_html=True)
    
    with st.container():
        input_text = st.text_input("💭 What would you like to know about the image?", 
                                 placeholder="Enter your question here...",
                                 key="input")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            uploaded_file = st.file_uploader("📎 Upload Image", 
                                          type=["jpg", "jpeg", "png"],
                                          help="Supported formats: JPG, JPEG, PNG")
        
        if uploaded_file:
            with col2:
                image = Image.open(uploaded_file)
                st.image(image, caption="Preview", use_container_width=True)  # Updated parameter
        
        input_prompt = """
        You are an expert in analyzing images and providing detailed, insightful responses.
        Please analyze the provided image and answer the question thoughtfully.
        """
        
        if st.button("🔍 Analyze Image", help="Click to analyze the uploaded image"):
            try:
                with st.spinner("🤔 Analyzing your image..."):
                    image_data = input_image_setup(uploaded_file)
                    response = get_gemini_response(input_prompt, image_data, input_text)
                    
                    st.success("Analysis Complete!")
                    st.markdown("### 📝 Analysis Results")
                    st.markdown(f">{response}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        st.markdown("<div class='footer'>Powered by Google Gemini 1.5 Flash</div>", 
                   unsafe_allow_html=True)

if __name__ == "__main__":
    main()