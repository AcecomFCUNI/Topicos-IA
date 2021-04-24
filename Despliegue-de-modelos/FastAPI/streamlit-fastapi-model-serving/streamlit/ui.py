import io

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import streamlit as st

# interactuamos con el endpoint de FastAPI
backend = "http://fastapi:8000/segmentation"


def process(image, server_url: str):

    m = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )

    return r


# construimos el título
st.title("Segmentación de imágenes con DeepLabV3")

st.write(
    """Obtenga mapas de segmentación semántica de la imagen en entrada a través de DeepLabV3 implementado en PyTorch.
          Este ejemplo simplificado utiliza un servicio FastAPI como backend.
          Visite esta URL en el puerto`:8000/docs` para obtener documentación de FastAPI."""
)

input_image = st.file_uploader("subir imagen") 

if st.button("Obtener mapa de segmentación"):

    col1, col2 = st.beta_columns(2)

    if input_image:
        segments = process(input_image, backend)
        original_image = Image.open(input_image).convert("RGB")
        segmented_image = Image.open(io.BytesIO(segments.content)).convert("RGB")
        col1.header("Original")
        col1.image(original_image, use_column_width=True)
        col2.header("Segmentacíon")
        col2.image(segmented_image, use_column_width=True)

    else:
        # cuando no insertamos una imagen
        st.write("Agregue una imagen!")
