import streamlit as st
import pyttsx3
import threading
import asyncio
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Function to load BLIP model (cached for performance)
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

# Load the BLIP model
processor, model = load_model()

# Function to generate an image caption
def generate_caption(image):
    image = image.convert("RGB")  # Ensure image is in RGB format
    inputs = processor(images=image, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption

# Function to run TTS using asyncio-compatible method
async def speak_text(text):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Streamlit UI
st.title("📷 Image to Speech Converter 🎤")
st.write("Upload an image, generate a description, and listen to it!")

# Image Upload Section
uploaded_file = st.file_uploader("📤 Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # Generate an image description
    with st.spinner("📝 Generating description... ⏳"):
        image_description = generate_caption(image)

    # Display the generated description
    st.subheader("📝 Generated Description:")
    st.write(image_description)

    # Speak Button (Runs in a separate async event loop)
    if st.button("🔊 Speak Description"):
        threading.Thread(target=asyncio.run, args=(speak_text(image_description),)).start()
        st.success("🎙️ Speaking...")

    # Download Audio Button
    if st.button("⬇️ Download Audio"):
        engine = pyttsx3.init()
        engine.save_to_file(image_description, "description.mp3")
        engine.runAndWait()
        with open("description.mp3", "rb") as file:
            st.download_button("Download Audio", file, file_name="image_description.mp3")
