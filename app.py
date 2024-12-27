import streamlit as st
import os
import pathlib
from PIL import Image
import google.generativeai as genai

def init_styles():
    st.markdown("""
        <style>
        /* Modern color palette */
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --accent: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --background: #f8fafc;
            --text: #1e293b;
            --text-light: #64748b;
        }

        /* Base styles with smooth scrolling */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        }
        
        /* Animated gradient background for header */
        .stApp header {
            background: linear-gradient(-45deg, #6366f1, #ec4899, #8b5cf6, #6366f1);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Modern glass morphism container */
        .glass-container {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 
                0 4px 6px -1px rgba(0, 0, 0, 0.1),
                0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.7);
        }
        
        /* Floating card effect */
        .content-container {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 
                0 10px 15px -3px rgba(0, 0, 0, 0.1),
                0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(0);
            transition: all 0.3s ease;
        }
        
        .content-container:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        /* Modern button design */
        .stButton > button {
            width: 100%;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            letter-spacing: 0.025em;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -1px rgba(99, 102, 241, 0.5);
        }
        
        /* Animated file uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed var(--primary);
            border-radius: 16px;
            padding: 2rem;
            background: #eef2ff;
            transition: all 0.3s ease;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: var(--secondary);
            background: #fdf2f8;
            transform: scale(1.01);
        }
        
        /* Modern input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 1rem;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }
        
        /* Typography */
        h1, h2, h3 {
            color: var(--text);
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.025em;
        }
        
        h1 { 
            font-size: 3rem; 
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        h2 { font-size: 2.25rem; }
        h3 { font-size: 1.5rem; }
        
        /* Feature cards with hover effects */
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            height: 100%;
            position: relative;
            overflow: hidden;
            transition: all 0.5s ease;
            border: 1px solid #e2e8f0;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            opacity: 0;
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .feature-card:hover::before {
            opacity: 0.1;
        }
        
        .feature-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 
                0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            display: block;
            transform: scale(1);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover .feature-icon {
            transform: scale(1.1);
        }
        
        /* Success/Error messages with animations */
        .stSuccess, .stError {
            border-radius: 12px;
            padding: 1rem;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .stSuccess {
            background: #ecfdf5;
            border: 1px solid var(--success);
            color: #065f46;
        }
        
        .stError {
            background: #fef2f2;
            border: 1px solid var(--error);
            color: #991b1b;
        }
        
        /* Loading spinner animation */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .stSpinner {
            text-align: center;
            padding: 2rem;
            color: var(--primary);
        }
        
        /* Footer with gradient */
        .footer {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-radius: 24px 24px 0 0;
            margin-top: 4rem;
        }
        
        .footer p {
            margin: 0.5rem 0;
            opacity: 0.9;
            font-size: 0.875rem;
            letter-spacing: 0.025em;
        }
        
        /* Image preview container */
        .image-preview {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .image-preview:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Smooth scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-dark);
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


def display_features():
    cols = st.columns(3)
    
    features = [
        {
            "icon": "🧠",
            "title": "AI-Powered Analysis",
            "description": "Advanced image understanding with Gemini 1.5 Flash technology"
        },
        {
            "icon": "⚡",
            "title": "Instant Results",
            "description": "Get detailed insights about your images in seconds"
        },
        {
            "icon": "🎯",
            "title": "Precise Insights",
            "description": "Accurate and detailed analysis for any type of image"
        }
    ]
    
    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"""
                <div class="feature-card">
                    <span class="feature-icon">{feature['icon']}</span>
                    <h3 style="font-size: 1.25rem; margin: 1rem 0;">{feature['title']}</h3>
                    <p style="color: var(--text-light);">{feature['description']}</p>
                </div>
            """, unsafe_allow_html=True)

def main():
    GOOGLE_API_KEY = "AIzaSyCiaqnFfhMe0Acscy8MgaF69kioayPX3GY"
    genai.configure(api_key=GOOGLE_API_KEY)
    
    init_styles()
    
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1>Vision Analysis Pro</h1>
            <p style="font-size: 1.25rem; color: var(--text-light); max-width: 600px; margin: 0 auto;">
                Unlock the power of AI vision analysis with our cutting-edge platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        cols = st.columns([1, 1])
        
        with cols[0]:
            with st.container():
                st.markdown('<div class="content-container">', unsafe_allow_html=True)
                st.markdown("""
                    <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                        📸 Upload Image
                    </h3>
                """, unsafe_allow_html=True)
                uploaded_file = st.file_uploader(
                    "Drop your image here or click to browse",
                    type=["jpg", "jpeg", "png"],
                    help="Supported formats: JPG, JPEG, PNG"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="content-container">', unsafe_allow_html=True)
                st.markdown("""
                    <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                        💭 Ask Question
                    </h3>
                """, unsafe_allow_html=True)
                input_text = st.text_area(
                    "",
                    placeholder="What would you like to know about this image?",
                    height=100
                )
                analyze_button = st.button("✨ Analyze Image")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.markdown("""
                <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                    🔍 Analysis Results
                </h3>
            """, unsafe_allow_html=True)
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.markdown('<div class="image-preview">', unsafe_allow_html=True)
                st.image(image, caption="", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if analyze_button and uploaded_file and input_text:
                try:
                    with st.spinner("🤔 Analyzing your image..."):
                        image_data = input_image_setup(uploaded_file)
                        input_prompt = """
                        You are an expert in analyzing images and providing detailed, insightful responses.
                        Please analyze the provided image and answer the question thoughtfully.
                        """
                        response = get_gemini_response(input_prompt, image_data, input_text)
                        st.success("✨ Analysis Complete!")
                        st.markdown(f">{response}")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h2 style="text-align: center; margin-bottom: 2rem;">
            ✨ Features
        </h2>
    """, unsafe_allow_html=True)
    display_features()
    
    st.markdown("""
        <div class="footer">
            <p>© 2024 Vision Analysis Pro. All rights reserved.</p>
            <p>
            <p>Created by Abdul Qadeer</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
