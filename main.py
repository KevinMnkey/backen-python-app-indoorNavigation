from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from image_processing.process_image import process_image
from image_processing.convert_to_svg import image_to_svg
# from image_processing.generate_3d_model import convert_svg_to_stl
# from image_processing.stl_to_obj import convert_stl_to_obj  # Importamos la función

app = FastAPI()

UPLOAD_FOLDER = 'uploads/'
RESULTS_FOLDER = 'results/'
SVG_FOLDER = 'svg/'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(SVG_FOLDER, exist_ok=True)

@app.post("/process-image/")
async def handle_image(image: UploadFile = File(...)):
    if image.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")

    file_path = os.path.join(UPLOAD_FOLDER, image.filename)

    # Guardar el archivo de imagen
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    # Define paths for processed image, SVG file, STL file, and OBJ file
    processed_image_path = os.path.join(RESULTS_FOLDER, 'contour_image_filled.png')
    svg_file_path = os.path.join(SVG_FOLDER, 'contours_filled.svg')
    stl_file_path = os.path.join(RESULTS_FOLDER, 'extruded_model_walls.stl')
    obj_file_path = os.path.join(RESULTS_FOLDER, 'model.obj')  # Agregar ruta del OBJ

    # Procesar la imagen
    process_image(file_path, processed_image_path)

    # Convertir la imagen procesada a SVG
    image_to_svg(processed_image_path, svg_file_path)

    # Convertir el SVG a STL (comentar si no se utiliza)
    # convert_svg_to_stl(svg_file_path, stl_file_path)

    # Convertir el STL a OBJ (comentar si no se utiliza)
    # convert_stl_to_obj(stl_file_path, obj_file_path)

    # Retornar el archivo SVG
    return FileResponse(svg_file_path, media_type="image/svg+xml", filename='contours_filled.svg')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
