# AI Medic - Remote Health Monitoring and Diagnosis

AI Medic is a Streamlit application that utilizes Google's Generative AI (Gemini-Pro-Vision model) to provide remote health monitoring and diagnosis services. The application allows users to upload medical images, scans, and videos, or provide a URL to such data. The AI model then analyzes the data and provides a preliminary diagnosis or analysis along with recommendations for further medical consultation.

## Features

- Supports image uploads (JPEG, PNG, GIF)
- Supports video uploads (MP4, AVI, MOV)
- Supports URL input for images and videos
- Real-time facial expression monitoring through camera input
- Text input for providing additional details or asking questions
- Generates clear and actionable feedback based on the provided data
- Maintains a chat history for easy reference

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/rajikudusadewale/AI-Medic---Remote-Health-Monitoring-and-Diagnosis_Gemini_LLMs.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the Google API key:
   - Create a `.env` file in the project root directory.
   - Add your Google API key to the `.env` file in the following format:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

4. Run the application:
   ```
   streamlit run gemini_remote_health_monitor.py
   ```

## Usage

1. Launch the application in your web browser.
2. Click on the "Start Conversation" button to begin interacting with AI Medic.
3. Upload an image, video, or provide a URL to the medical data you want to analyze.
4. Optionally, toggle the camera input for real-time facial expression monitoring.
5. Enter any additional details or ask a question in the text input field.
6. Click on the "Running..." button to initiate the analysis.
7. AI Medic will provide a preliminary diagnosis or analysis along with recommendations.
8. The chat history will be displayed below, allowing you to refer back to previous interactions.
9. Use the "Clear History" button to clear the chat history if needed.
10. Click on the "Quit" button to end the conversation and reset the application.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Google Generative AI](https://cloud.google.com/generative-ai)
- [Streamlit](https://streamlit.io/)
- [Python Imaging Library (PIL)](https://pillow.readthedocs.io/)

## Contact

For any questions or inquiries, please contact [Email](mailto:dedatadude@akraji.com).

---

Developed by DeDataDude
