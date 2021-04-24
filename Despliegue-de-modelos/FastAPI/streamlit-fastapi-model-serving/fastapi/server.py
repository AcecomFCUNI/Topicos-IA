import io

from segmentation import get_segmentator, get_segments
from starlette.responses import Response

from fastapi import FastAPI, File

model = get_segmentator()

app = FastAPI(
    title="Segmentación con DeepLabV3",
    description="""Obtenga mapas de segmentación semántica de la imagen de entrada a través de DeepLabV3 implementado en PyTorch.
                            Visite esta URL en el puerto 8501 para ver la interfaz optimizada.""",
    version="0.1.0",
)


@app.post("/segmentation")
def get_segmentation_map(file: bytes = File(...)):
    """Obtenemos el mapa de segmentación de la imagen"""
    segmented_image = get_segments(model, file)
    bytes_io = io.BytesIO()
    segmented_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")
