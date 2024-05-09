from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()




@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request):
    content_type = request.headers.get('Content-Type')
    
    if content_type == "application/json":
        data = await request.json()
        alert_message = data.get("text", "No text provided")
    elif content_type == "text/plain":
        data = await request.body()
        alert_message = data.decode("utf-8")
    else:
        return JSONResponse(status_code=400, content={"message": "Unsupported content type"})
    
    # Here you would handle the alert based on `alert_message`
    # For example, logging it or triggering another action
    print("Received alert:", alert_message)
    
    # Optional: Send notification (via email, SMS, etc.)
    # send_email("New TradingView Alert", alert_message)
    # send_sms(alert_message)

    return JSONResponse(status_code=200, content={"message": "Received successfully"})


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
    
