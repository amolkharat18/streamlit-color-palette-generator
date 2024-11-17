import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

st.title("🎨 Color Palette Generator")

msg = st.text_input("Generate color palette for:")

prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    Your should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 1 and 10 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]


    Desired Format: a JSON array of hexadecimal color codes

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """

def display_colors(colors):
    st.html(
        " ".join(
                f"<span style='display:block; width: 200px; background-color: {color};'>{color}</span>"
                for color in colors
        )
    )

if st.button("Generate") and msg:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],    
        max_tokens=200
    )
    print(response.choices[0].message.content)
    colors = json.loads(response.choices[0].message.content)
    display_colors(colors)
