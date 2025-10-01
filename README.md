# FlaskMarket

A simple Flask web application for buying and selling items.

## Features
- User registration and login
- Purchase and sell items
- Budget management for users
- Display owned and available items

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
2. Navigate to the folder:  
   `cd FlaskMarket`
3. Create and activate virtual environment:  
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
4. Install dependencies:
  pip install -r requirements.txt
5. Run the app:
  python run.py
6. Open: http://127.0.0.1:5000/ in your browser
   
# File Structure
market/ → HTML templates
models.py → Database models
forms.py → WTForms forms
routes.py → Flask routes
run.py → Entry point of the application
requirements.txt → Python dependencies
