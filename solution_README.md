## How to run the application

1. Clone the repository
2. Navigate to the root directory
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
4. Run the application
   ```
   python app.py
   ```

## If using Docker

1. Clone the repository
2. Navigate to the root directory
3. Build the Docker Image
   ```
   docker build -t receipt-processor .
   ```
4. Run the Docker container
   ```
   docker run -p 8000:8000 receipt-processor
   ```
