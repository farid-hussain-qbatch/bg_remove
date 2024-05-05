from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))
    output_image = remove(input_image)  # rembg returns a PIL Image, not bytes

    # Save the output to a file
    output_path = 'output.png'
    output_image.save(output_path, format='PNG')  # Save the Image object directly

    # Return the saved file as a response
    return FileResponse(output_path, media_type='image/png', filename='output.png')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
