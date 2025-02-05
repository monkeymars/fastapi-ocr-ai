from fastapi import FastAPI, UploadFile, File
import shutil
import os
from openai import OpenAI
import easyocr
import json
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = "***REMOVED***"

settings = Settings()
app = FastAPI()

openai_client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

@app.get("/")
def read_root():
    return {"ocrai": "v1"}


@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Initialize EasyOCR reader
    # Read text from the uploaded image
    reader = easyocr.Reader(['id', 'en'], gpu=False)
    results = reader.readtext(file.filename, detail = 0)

    print(results)

    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"I have extracted the following text from a receipt using OCR: {results}"
            }
        ],
        model="gpt-4-0613",  # Use a model supporting function calling
        functions=[
            {
                "name": "extract_receipt_data",
                "description": "Extract structured data from a receipt text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "store_name": {"type": "string"},
                        "date": {"type": "string", "format": "date-time"},
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "item": {"type": "string"},
                                    "price": {"type": "number"},
                                },
                                "required": ["item", "price"],
                            },
                        },
                        "subtotal": {"type": "number"},
                        "tax": {"type": "number"},
                        "total": {"type": "number"},
                        "payment_method": {"type": "string"},
                    },
                    "required": [
                        "store_name",
                        "date",
                        "items",
                        "subtotal",
                        "tax",
                        "total",
                        "payment_method",
                    ],
                },
            }
        ],
        function_call={"name": "extract_receipt_data"}  # Explicitly request the function
    )


    # Clean up the temporary file
    file_path = str(file.filename)
    os.remove(file_path)

    # Extract the structured arguments from the response
    function_call = chat_completion.choices[0].message.function_call
    if not function_call:
        raise ValueError("Function call is missing in the response.")

    arguments = function_call.arguments
    if not arguments:
        raise ValueError("Arguments are missing in the function call.")

    token_usage = chat_completion.usage
    if not token_usage:
        raise ValueError("Function call is missing in the response.")

    # Parse the arguments (they are returned as a string)
    structured_data = json.loads(arguments)


    return {
        "filename": file.filename,
        "analysis": structured_data,
        "token_usage": token_usage.total_tokens
    }
