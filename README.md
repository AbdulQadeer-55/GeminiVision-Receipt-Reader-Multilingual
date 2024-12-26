# Vision Analysis Pro 🖼️

A powerful image analysis web application powered by Google's Gemini 1.5 Flash AI model. This application allows users to upload images and ask questions about them, receiving detailed AI-powered analysis and insights.

## 🌟 Features

- **Advanced Image Analysis**: Leverages Google's Gemini 1.5 Flash model for state-of-the-art image understanding
- **Interactive Interface**: Clean and modern UI built with Streamlit
- **Real-time Processing**: Get instant analysis of your uploaded images
- **User-friendly Design**: Intuitive interface with smooth animations and responsive design
- **Flexible Question Handling**: Ask any question about your uploaded image and get detailed responses

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AbdulQadeer-55/GeminiVision-Receipt-Reader-Multilingual.git
cd GeminiVision-Receipt-Reader-Multilingual
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Configuration

1. Obtain a Google API key for Gemini:
   - Visit the [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy your API key

2. Update the API key in the application:
   - Open `app.py`
   - Replace `"YOUR_API_KEY"` with your actual API key

### Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

## 📦 Project Structure

```
vision-analysis-pro/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## 📋 Dependencies

```
streamlit>=1.30.0
Pillow>=10.0.0
google-generativeai>=0.3.0
```

## 💡 Usage

1. Launch the application
2. Upload an image using the file uploader
3. Type your question about the image in the text area
4. Click "Analyze Image" to receive AI-powered insights
5. View the analysis results in the right panel

## 🎨 Customization

The application's appearance can be customized by modifying the CSS styles in the `init_styles()` function. Key customizable elements include:

- Color schemes
- Font styles
- Container layouts
- Animation effects
- Component styling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Abdul Qadeer**

## 🙏 Acknowledgments

- Google Gemini 1.5 Flash for providing the AI capabilities
- Streamlit for the excellent web framework
- The open-source community for various tools and libraries

## ⚠️ Important Notes

- Ensure your API key is kept secure and never commit it to version control
- The application requires an active internet connection for API calls
- Image analysis capabilities depend on the Gemini model's limitations
- Supported image formats: JPG, JPEG, PNG

## 🐛 Troubleshooting

Common issues and solutions:

1. **API Key Issues**:
   - Verify your API key is correctly set
   - Check if you have reached your API quota

2. **Image Upload Problems**:
   - Ensure image format is supported
   - Check if file size is within limits

3. **Performance Issues**:
   - Try reducing image size before upload
   - Check your internet connection
   - Verify system meets minimum requirements

For additional support or issues, please open an issue in the GitHub repository.