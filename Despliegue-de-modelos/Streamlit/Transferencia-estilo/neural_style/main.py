# python3 -m venv venv
# . venv/bin/activate
# pip install streamlit
# pip install torch torchvision
# streamlit run main.py
import streamlit as st
from PIL import Image

import style

st.title('Transferencia de estilo con Pytorch')

img = st.sidebar.selectbox(
    'Selecciona una imagen',
    ('amber.jpg', 'cat.png')
)

style_name = st.sidebar.selectbox(
    'Selecciona un estilo',
    ('candy', 'mosaic', 'rain_princess', 'udnie')
)


model= "saved_models/" + style_name + ".pth"
input_image = "images/content-images/" + img
output_image = "images/output-images/" + style_name + "-" + img

st.write('### Imagen de entrada:')
image = Image.open(input_image)
st.image(image, width=400) # image: arreglo numpy

clicked = st.button('Stylize')

if clicked:
    model = style.load_model(model)
    style.stylize(model, input_image, output_image)

    st.write('### Imagen de salida:')
    image = Image.open(output_image)
    st.image(image, width=400)

