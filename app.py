import streamlit as st
import os
import pathlib
from PIL import Image
import google.generativeai as genai

def init_styles():
    st.markdown("""
        <style>
        /* Base styles */
        .stApp {
            background-color: #f8fafc;
        }
        
        /* Header and footer gradient */
        .stApp header, .stApp footer {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        }
        
        /* Container styling */
        .content-container {
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        /* Glass effect container */
        .glass-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(79, 70, 229, 0.1);
            border: 1px solid rgba(79, 70, 229, 0.1);
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
        }
        
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            border: 2px dashed #cbd5e1;
            border-radius: 0.75rem;
            padding: 1.5rem;
            background: #f8fafc;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: #4f46e5;
            background: #eef2ff;
        }
        
        /* Text input/area styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 0.5rem;
            border: 1px solid #cbd5e1;
            padding: 0.75rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #4f46e5;
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1e293b;
            font-family: 'Helvetica Neue', sans-serif;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        h1 { font-size: 2.5rem; }
        h2 { font-size: 2rem; }
        h3 { font-size: 1.5rem; }
        
        /* Feature cards */
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            text-align: center;
            height: 100%;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e2e8f0;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(79, 70, 229, 0.1);
            border-color: #4f46e5;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        /* Success/Error messages */
        .stSuccess {
            border-radius: 0.5rem;
            background: #ecfdf5;
            border: 1px solid #34d399;
            color: #065f46;
        }
        
        .stError {
            border-radius: 0.5rem;
            background: #fef2f2;
            border: 1px solid #f87171;
            color: #991b1b;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            position: relative;
            margin-top: 3rem;
        }
        
        .footer p {
            margin: 0.5rem 0;
            opacity: 0.9;
        }
        
        /* Spinner/Loading state */
        .stSpinner {
            text-align: center;
            padding: 2rem;
            color: #4f46e5;
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
            "icon": "🚀",
            "title": "Advanced AI",
            "description": "Powered by state-of-the-art Gemini 1.5 Flash technology"
        },
        {
            "icon": "⚡",
            "title": "Fast Analysis",
            "description": "Get instant insights about your images"
        },
        {
            "icon": "🎯",
            "title": "Accurate Results",
            "description": "Precise and detailed analysis every time"
        }
    ]
    
    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"""
                <div class="feature-card">
                    <span class="feature-icon">{feature['icon']}</span>
                    <h3 style="font-size: 1.25rem; margin: 1rem 0;">{feature['title']}</h3>
                    <p style="color: #64748b;">{feature['description']}</p>
                </div>
            """, unsafe_allow_html=True)

def main():
    # Configure API key
    GOOGLE_API_KEY = "AIzaSyCiaqnFfhMe0Acscy8MgaF69kioayPX3GY"
    genai.configure(api_key=GOOGLE_API_KEY)
    
    init_styles()
    
    # Header
    st.markdown('<div style="text-align: center; padding: 2rem 0;">', unsafe_allow_html=True)
    st.markdown("<h1>Vision Analysis Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.25rem; color: #64748b;'>Powered by Google Gemini 1.5 Flash</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        cols = st.columns([1, 1])
        
        with cols[0]:
            with st.container():
                st.markdown('<div class="content-container">', unsafe_allow_html=True)
                st.markdown("### Upload Image")
                uploaded_file = st.file_uploader(
                    "Choose an image file",
                    type=["jpg", "jpeg", "png"],
                    help="Supported formats: JPG, JPEG, PNG"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="content-container">', unsafe_allow_html=True)
                st.markdown("### Ask Question")
                input_text = st.text_area(
                    "",
                    placeholder="What would you like to know about the image?",
                    height=100
                )
                analyze_button = st.button("Analyze Image")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown('<div class="content-container">', unsafe_allow_html=True)
            st.markdown("### Analysis Results")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
            
            if analyze_button and uploaded_file and input_text:
                try:
                    with st.spinner("🔍 Analyzing your image..."):
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
    
    # Features section
    st.markdown("<h2>Features</h2>", unsafe_allow_html=True)
    display_features()
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>© 2024 Vision Analysis Pro. All rights reserved.</p>
            <p>Created by Abdul Qadeer</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()