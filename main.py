from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
 
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request):
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == "application/json":
            data = await request.json()
            print("Received JSON data:", data)  # Log the JSON data
            return JSONResponse(status_code=200, content={"message": "JSON received successfully"})
        else:
            raw_data = await request.body()
            print("Received Non-JSON data:", raw_data.decode())  # Log raw data
            return JSONResponse(status_code=200, content={"message": "Non-JSON received successfully"})
    except Exception as e:
        print("Error processing request:", str(e))  # Log any errors
        return JSONResponse(status_code=400, content={"message": "Bad request"})


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
    
