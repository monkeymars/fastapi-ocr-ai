# FastAPI OCR and Receipt Extraction API

This FastAPI project provides an API for uploading image files, extracting text using EasyOCR, and structuring the extracted data using OpenAI's GPT model.

## Features
- Upload an image file (e.g., a receipt)
- Extract text using EasyOCR
- Process extracted text with OpenAI's GPT-4 to structure receipt data
- Returns structured receipt details including store name, date, items, subtotal, tax, total, and payment method

## Requirements

Ensure you have Python installed. The required dependencies can be installed using:

```sh
pip install fastapi uvicorn openai easyocr pydantic-settings
```

Additionally, you need to set up an OpenAI API key.

## Environment Variables

Set up the OpenAI API key as an environment variable:

```sh
export OPENAI_API_KEY="your_openai_api_key"
```

## Running the API

Start the FastAPI server with:

```sh
uvicorn main:app --reload
```

## API Endpoints

### Root Endpoint
**GET /**

Returns a simple JSON response:

```json
{
  "ocrai": "v1"
}
```

### Upload and Process File
**POST /upload-file/**

#### Request:
- **file** (image file, required): The image containing receipt text.

#### Response:
- Extracted and structured receipt data.

#### Example Request (cURL):
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/upload-file/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@receipt.jpg'
```

#### Example Response:
```json
{
  "filename": "receipt.jpg",
  "analysis": {
    "store_name": "Sample Store",
    "date": "2024-02-06T15:30:00",
    "items": [
      { "item": "Milk", "price": 2.99 },
      { "item": "Bread", "price": 1.49 }
    ],
    "subtotal": 4.48,
    "tax": 0.52,
    "total": 5.00,
    "payment_method": "Credit Card"
  },
  "token_usage": 120
}
```

## Notes
- The API processes only image files.
- Ensure OpenAI API access to use GPT functions.

## License
This project is open-source and available for use and modification.

---

Enjoy using FastAPI for OCR and structured receipt extraction!
