# Address Line Splitter API

A FastAPI-based REST API that intelligently splits single-line addresses into three equally distributed lines. Perfect for forms, shipping labels, or any application that requires multi-line address formatting.

## Features

- **Intelligent Distribution**: Splits addresses into 3 lines with balanced character counts
- **Smart Parsing**: Recognizes common delimiters (commas, semicolons) and word boundaries
- **RESTful API**: Easy-to-use HTTP endpoints
- **Interactive Documentation**: Built-in Swagger UI
- **Robust Error Handling**: Graceful handling of edge cases

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/address-line-splitter.git
cd address-line-splitter
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn pydantic
```

## Usage

### Starting the Server

Run the API server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Interactive Documentation

Access the auto-generated API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### GET /

Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Address Line Splitter API",
  "endpoints": {
    "/split": "POST - Split address into 3 lines",
    "/docs": "Interactive API documentation"
  }
}
```

### POST /split

Splits a single address line into three equally distributed lines.

**Request Body:**
```json
{
  "address": "123 Main Street, Apartment 4B, Springfield, IL 62701, United States"
}
```

**Response:**
```json
{
  "address_line_1": "123 Main Street, Apartment 4B",
  "address_line_2": "Springfield, IL 62701",
  "address_line_3": "United States",
  "original_address": "123 Main Street, Apartment 4B, Springfield, IL 62701, United States"
}
```

## Examples

### Using cURL

```bash
curl -X POST "http://localhost:8000/split" \
  -H "Content-Type: application/json" \
  -d '{"address": "Plot No. 45, Sector 12, Near City Mall, Gurgaon, Haryana 122001"}'
```

### Using Python

```python
import requests

url = "http://localhost:8000/split"
data = {
    "address": "Flat 301, Krishna Towers, MG Road, Bangalore 560001"
}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript (fetch)

```javascript
fetch('http://localhost:8000/split', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    address: 'Building A, Floor 3, Office 302, Tech Park, Whitefield, Bangalore'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## How It Works

The API uses an intelligent algorithm to split addresses:

1. **Normalization**: Cleans up whitespace and formats the input
2. **Delimiter Detection**: Identifies natural breaks (commas, semicolons)
3. **Equal Distribution**: Calculates target character length for each line
4. **Smart Word Wrapping**: Ensures words aren't split and content is balanced
5. **Fallback Logic**: Handles edge cases like very short addresses

## Testing

Run the built-in tests:

```bash
python main.py
```

This will execute test cases with sample addresses and display the results.

## Project Structure

```
address-line-splitter/
├── main.py           # Main API application
├── README.md         # This file
└── requirements.txt  # Python dependencies (optional)
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications

Create a `requirements.txt` file:
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

## Configuration

The server runs on `0.0.0.0:8000` by default. Modify the configuration in `main.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Successful address split
- `400`: Bad request (invalid input)
- `422`: Validation error (missing required fields)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

Built with FastAPI and modern Python best practices.
