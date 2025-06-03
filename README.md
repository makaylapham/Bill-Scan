# Bill Scanning API

A Flask-based REST API that processes images of bills/receipts and extracts relevant information using OCR (Optical Character Recognition). Users can upload photos of their bills through the mobile app, and the API will extract and store the bill details.

## Features

- Image upload and processing
- OCR text extraction from bills
- Data parsing for common bill formats
- Extracted information storage
- Historical bill tracking
- Support for multiple image formats (JPEG, PNG, HEIC)

## Setup

1. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your configuration
TESSDATA_PREFIX=/usr/local/share/tessdata  # Path to Tesseract OCR data
STORAGE_PATH=./uploads                      # Path to store uploaded images
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Bill Processing

#### Upload and scan a bill
```
POST /bills/scan
Content-Type: multipart/form-data

Parameters:
- image: File (required) - The bill image file
- user_id: String (required) - ID of the user uploading the bill
- scan_type: String (optional) - Type of bill (utility, restaurant, retail)
```

#### Get processed bill details
```
GET /bills/<bill_id>
```

#### Get user's bill history
```
GET /bills/user/<user_id>
```

### Image Management

#### Get original bill image
```
GET /bills/<bill_id>/image
```

#### Get processed bill image (with highlights)
```
GET /bills/<bill_id>/image/processed
```

## Supported Bill Types

- Restaurant receipts
- Utility bills
- Retail receipts
- Grocery receipts
- Service invoices

## Extracted Information

The API attempts to extract the following information from bills:

- Merchant name and details
- Date and time of purchase
- Total amount
- Individual item details (when available)
- Tax amounts
- Payment method
- Receipt/bill number

## Example Usage

1. Upload and scan a bill:
```bash
curl -X POST http://localhost:5000/bills/scan \
    -F "image=@path/to/bill.jpg" \
    -F "user_id=USER_ID" \
    -F "scan_type=restaurant"
```

2. Get processed bill details:
```bash
curl http://localhost:5000/bills/BILL_ID
```

3. Get user's bill history:
```bash
curl http://localhost:5000/bills/user/USER_ID
```

## Mobile App Integration

The API is designed to work with mobile apps. Here are some integration tips:

1. Image Guidelines:
   - Ensure good lighting
   - Capture the entire bill
   - Avoid blurry images
   - Recommended resolution: 1080p or higher

2. Error Handling:
   - Handle network timeouts
   - Implement retry logic
   - Cache images locally before upload
   - Show processing status to users

3. Security:
   - Implement user authentication
   - Use HTTPS for all requests
   - Don't store sensitive bill data locally

## Development Notes

This is a development version. For production use, consider:

### Security Considerations
- Implementing user authentication
- Adding API key validation
- Encrypting sensitive bill data
- Implementing rate limiting
- Adding request validation

### Performance Optimizations
- Image compression before upload
- Caching processed results
- Background job processing
- Load balancing for high traffic

### Storage Considerations
- Cloud storage for images
- Database for extracted data
- Regular backups
- Data retention policies

### Additional Features to Consider
- PDF bill support
- Multiple currency support
- Export functionality
- Expense categorization
- Budget tracking integration
- Machine learning for improved accuracy

## Troubleshooting

Common issues and solutions:

1. Poor OCR Results:
   - Ensure good image quality
   - Check lighting conditions
   - Verify image is not skewed
   - Confirm bill format is supported

2. Upload Errors:
   - Check file size limits
   - Verify supported file formats
   - Ensure stable network connection
   - Validate user credentials

3. Processing Errors:
   - Check server logs
   - Verify OCR service status
   - Ensure sufficient storage space
   - Validate input parameters
