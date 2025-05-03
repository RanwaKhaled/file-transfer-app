# File Transfer Web Application

A web application for uploading, listing, and downloading files using Flask (Python) for the backend and HTML/CSS/JavaScript for the frontend. The app integrates with Amazon S3 for file storage.

![Screenshot 2025-04-22 000504](https://github.com/user-attachments/assets/96952936-bd4b-46e5-ac86-8d3156b74740)

## Features

- **File Upload**: Upload files directly to Amazon S3 using pre-signed URLs
- **Progress Tracking**: Real-time upload progress bar
- **File Listing**: View all uploaded files with their names and sizes
- **Download Files**: Download files directly from S3
- **Flash Messages**: User feedback for success/error messages
- **Responsive Design**: Clean UI with CSS styling

## Technology Stack

**Frontend:**
- HTML5
- CSS3
- JavaScript (Vanilla JS with AJAX)

**Backend:**
- Python 3
- Flask framework
- Jinja2 templating

**Cloud Storage:**
- Amazon S3

## Project Structure

```
file-transfer-app/
├── app.py                # Flask application
├── static/               # Static files (CSS, JS)
│   ├── style.css
│   └── script.js
├── templates/            # HTML templates
│   └── index.html
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/RanwaKhaled/file-transfer-app.git
   cd file-transfer-app
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file with your S3 configuration:
   ```
   S3_BUCKET=your_bucket_name
   S3_REGION=your_region
   ```

5. **Run the application**
   ```bash
   flask run
   ```

6. **Access the application**
   Open your browser and visit `http://localhost:5000`


