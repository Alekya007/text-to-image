import streamlit as st
import requests
from PIL import Image
import io

api_key = st.secrets["HF_API_KEY"]  # This fetches the key securely


st.set_page_config(page_title="Text-to-Image Generator", layout="centered")

st.title("🎨 Text-to-Image Generator")

# API Key input
api_key = st.text_input("🔑 Hugging Face API Key", type="password")

# Prompt inputs
prompt = st.text_area("📝 Describe the image you want to generate:", 
                      placeholder="A serene lake surrounded by mountains at sunset, with a small boat in the foreground")

negative_prompt = st.text_area("🚫 Negative prompt (things to avoid):", 
                               placeholder="blurry, distorted, low quality, ugly, bad anatomy")

if st.button("Generate Image"):
    if not api_key:
        st.error("Please enter your Hugging Face API key.")
    elif not prompt.strip():
        st.error("Please enter a description for the image.")
    else:
        with st.spinner("Generating your image... This may take a moment."):
            try:
                response = requests.post(
                    "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "negative_prompt": negative_prompt,
                            "num_inference_steps": 50,
                            "guidance_scale": 7.5
                        }
                    }
                )

                if response.status_code != 200:
                    error_message = response.json().get("error", "Unknown error")
                    st.error(f"Error: {error_message}")
                else:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, caption="Generated Image", use_container_width=True)
                    st.download_button("📥 Download Image", data=response.content, file_name="generated-image.png")
            except Exception as e:
                st.error(f"Error: {str(e)}")
