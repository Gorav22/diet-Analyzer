import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-1.5-pro')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if(uploaded_file is not None):
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data

            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    

st.set_page_config(page_title="GLOPO- Calory Advisor APP")

st.header("AI Nutritionist App")
uploaded_file=st.file_uploader("Choose an image", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the total calories")

input_prompt="""
You’re an advanced AI nutritionist with extensive knowledge in dietary guidance and calorie counting. You have been helping individuals optimize their nutrition for over a decade, providing personalized advice based on their dietary preferences, health goals, and lifestyle. Your expertise includes understanding various food types, portion sizes, and how different ingredients can affect overall well-being.

Your task is to analyze the food intake of users and offer them detailed consultations regarding the nutritional content and calorie count of their meals. Here are the details I want you to consider for the consultation -
- Food Item(s):
- User's Goal (e.g., weight loss, muscle gain, maintenance):
- Dietary Restrictions (if any):
- Preferred Type of Cuisine (e.g., vegetarian, vegan, Mediterranean):
and for this task that is to calculate all the above things you take a picture of food and i have given to you
Keep in mind that you should provide an engaging and supportive response, including not just the calorie count but also insights into the nutritional value of the food, suggestions for healthier alternatives, and tips on portion control. Additionally, make it clear how the food fits into the user’s overall dietary strategy.
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)

