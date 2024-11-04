import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

system_message = """
# system message:
You are a highly specialized Healthcare assistant for Remote Health Monitoring and Diagnosis. Your primary objective is to assist healthcare providers and patients by analyzing medical images, scans, and videos to provide diagnoses and facilitate remote health monitoring. Your responses should be clear, accurate, and focused on providing actionable insights based on the provided data. You are not allowed to perform any tasks or provide any information that is outside the scope of remote health monitoring and diagnosis.

# Persona:
Name: Remote Health Monitor
Role: Specialist in Remote Health Monitoring and Diagnosis with over 20 years of experience
Tone: Professional, informative, empathetic
Expertise: Medical image analysis, symptom detection through video monitoring, telemedicine support

# Few-Shot Prompting:
Example 1
Input:
Patient: I have a skin lesion that has changed in size and color over the past month. Here is an image of the lesion.
Image: [URL to image]

Response:
Diagnosis: The image analysis suggests that the lesion may be indicative of a malignant melanoma. It is characterized by asymmetry, irregular borders, and varied coloration. Immediate consultation with a dermatologist is recommended for further examination and biopsy.

Example 2
Input:
Patient: I have been experiencing persistent chest pain. Here is my latest chest X-ray.
Image: [URL to X-ray image]

Response:
Diagnosis: The chest X-ray analysis reveals a potential abnormality in the lower left lung area, which could indicate the presence of pneumonia or a localized infection. It is advisable to seek immediate medical attention for a thorough evaluation and appropriate treatment.

Example 3
Input:
Patient: My child has been having severe headaches and dizziness. Here is a video showing their current state.
Video: [URL to video]

Response:
Preliminary Analysis: The video monitoring indicates signs of distress and discomfort, evidenced by facial expressions and physical behavior. These symptoms could be related to a neurological issue or severe migraine. An urgent consultation with a pediatrician or neurologist is recommended.

# Chain of Thought:
- Identify the Type of Input: Determine whether the input is an image (e.g., skin lesion, X-ray) or video (e.g., facial expressions indicating pain) or text input.
- Analyze the Input: Use your capabilities as specialized Healthcare assistant for Remote Health Monitoring and Diagnosis to analyze the provided image or video.
- Generate Preliminary Diagnosis or Analysis:
- For images, identify potential conditions based on visual indicators.
- For videos, detect symptoms based on observed behaviors and expressions.
- Provide Clear and Actionable Feedback: Offer a preliminary diagnosis or analysis along with recommendations for further medical consultation.
"""

def ask_and_get_answer(prompt, img=None, url=None, video=None):
    # creating a GenerativeModel instance using the Gemini-Pro-Vision model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", system_instruction=system_message)

    # generate a text response based on the prompt and image or url
    inputs = [prompt]
    if img:
        inputs.append(img)
    elif url:
        inputs.append(url)
    elif video:
        inputs.append(video)
    
    response = model.generate_content(inputs)

    return response.text

# This function converts a Streamlit image upload object (st_image) into a PIL (Python Imaging Lib) Image object.
def st_image_to_pil(st_image):
    import io
    from PIL import Image

    # getting the image data from the BytesIO object.
    image_data = st_image.read()

    # converting the image data to a PIL Image object.
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image

def is_image(file):
    return file.type in ['image/jpeg', 'image/png', 'image/gif']

def is_video(file):
    return file.type in ['video/mp4', 'video/avi', 'video/mov']

# defining application entry point
if __name__ == '__main__':
    # loading the environment variables from the .env file that contains the Google API key.
    load_dotenv(find_dotenv(), override=True)

    # configuring the generative AI model to use the GOOGLE_API_KEY for authentication.
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

    st.title('AI Medic')
    st.image('logo.jpg') 
    st.subheader('Remote Health Monitoring and Diagnosis')


    # creating buttons to start conversation, clear history, and quit
    if st.button('Start Conversation'):
        if 'history' not in st.session_state:
            st.session_state.history = ''
        st.session_state.engaged = True

    if st.button('Clear History'):
        st.session_state.history = ''

    if st.button('Quit'):
        st.session_state.engaged = False
        st.session_state.history = ''

    # Check if the user is engaged with the AI
    if 'engaged' not in st.session_state:
        st.session_state.engaged = False

    if st.session_state.engaged:
        # creating a file upload widget for the user to select an image or video.
        file = st.file_uploader('Select a file (Image, Video, Doc):', type=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'doc', 'docx'], accept_multiple_files=False, key="file_uploader")
        
        # creating a URL input widget for the user to provide a link to an image or video.
        url = st.text_input('Or Enter URL of Image or Video:', key="url_input")

        # button to toggle camera input
        if 'camera_active' not in st.session_state:
            st.session_state.camera_active = False

        if st.button('Toggle Camera'):
            st.session_state.camera_active = not st.session_state.camera_active

        # camera input widget for real-time facial expression monitoring, activated by button
        if st.session_state.camera_active:
            camera_input = st.camera_input('Capture Image for Facial Expression Monitoring', key="camera_input")
        else:
            camera_input = None

        # If the user has selected a file or provided a URL, or used the camera input, we proceed with the analysis.
        if file or url or camera_input:
            pil_image = None
            video_file = None
            
            if file:
                if is_image(file):
                    pil_image = st_image_to_pil(file)
                    st.image(file, caption='Uploaded image.')
                elif is_video(file):
                    video_file = file
                    st.video(file, caption='Uploaded video.')
                else:
                    st.write("Unsupported file type for analysis.")
            
            if url:
                st.text(f'URL: {url}')
            
            if camera_input:
                pil_image = st_image_to_pil(camera_input)
                st.image(camera_input, caption='Captured image.')

            # displaying a text input for the prompt.
            prompt = st.text_area('Enter details or ask a question:')

            # if the user has entered a question, we go ahead and make the API call to Gemini.
            if prompt:
                # creating a spinner
                with st.spinner('Running ...'):
                    # calling ask_and_get_answer().
                    answer = ask_and_get_answer(prompt, pil_image, url, video_file)

                    # displaying the answer in a text area widget.
                    st.text_area('AI Medic:', value=answer, height=300)

                # adding a divider to separate the current answer from the previous ones.
                st.divider()

                # creating a key in the session state called 'history'.
                # the corresponding value will be all the previous questions and answers.
                if 'history' not in st.session_state:
                    st.session_state.history = ''

                # concatenating the current question with its answer.
                value = f'Q: {prompt} \n\n A: {answer}'

                # adding this value before the existing history.
                st.session_state.history = f'{value} \n\n {"-" * 100} \n\n {st.session_state.history}'

                # saving the chat history from the session state into a variable.
                h = st.session_state.history

                # displaying a text area for the chat history.
                st.text_area(label='Chat History', value=h, height=600, key='history')

st.text('Developed By DeDataDude')
# Run the app: streamlit run ./gemini_remote_health_monitor.py
