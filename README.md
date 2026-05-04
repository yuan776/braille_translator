# English to Braille Translator
## BCA Invention Convention Project by Melinda Yuan

A simple Flask web application that translates English text to Braille. This project was created to help the blind and visually impaired access written information more easily.

### Mission

Melinda Yuan developed this translator as part of the BCA Invention Convention to showcase innovation dedicated to helping people in need. With 285 million blind and visually impaired people worldwide, improving accessibility through technology is crucial. This tool bridges the gap by converting digital text to Grade 1 Unified English Braille.

## Features

- Clean, modern web interface
- Real-time Braille translation using Grade 1 Unified English Braille
- Copy Braille text to clipboard
- Responsive design for mobile and desktop
- No external dependencies required for translation
- Supports letters, numbers, and common punctuation

## Local Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone or download this repository:
```bash
cd braille_translator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install gunicorn  # For production
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment to Render

### Step 1: Prepare Your Repository

1. Initialize a Git repository (if not already done):
```bash
git init
git add .
git commit -m "Initial commit"
```

2. Push to GitHub:
   - Create a new repository on GitHub
   - Add the remote and push:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/braille_translator.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com)
2. Sign up or log in with your GitHub account
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure your service:
   - **Name**: `braille-translator` (or your choice)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"
7. Render will deploy your app automatically!

Your app will be available at a URL like: `https://braille-translator.onrender.com`

### Step 3: Keep Your App Awake (Optional)

Render's free tier puts apps to sleep after 15 minutes of inactivity. To prevent this:

1. Go to [cron-job.org](https://cron-job.org)
2. Create a new cron job
3. Set it to ping your Render URL every 14 minutes
4. Your app will stay active!

## How It Works

- **Frontend**: HTML/CSS/JavaScript for a responsive user interface
- **Backend**: Flask server that receives translation requests
- **Translation**: Uses a built-in Grade 1 Braille character mapping to convert English to Braille Unicode patterns
- **API Endpoint**: `/api/translate` accepts POST requests with JSON data

## API Usage

### Endpoint: POST `/api/translate`

**Request:**
```json
{
  "text": "Hello world"
}
```

**Response:**
```json
{
  "original": "Hello world",
  "braille": "⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙"
}
```

## Project Structure

```
braille_translator/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── runtime.txt           # Python version
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Main web page
└── static/
    ├── style.css         # Styling
    └── script.js         # Frontend JavaScript
```

## Technologies Used

- **Flask**: Web framework
- **Built-in Braille Character Mapping**: Grade 1 Braille translation using Unicode Braille patterns
- **HTML/CSS/JavaScript**: Frontend
- **Render**: Hosting platform

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Translation not working
- Check your internet connection
- Try with a simpler text input first
- Check the browser console for errors (F12)

### App is slow on Render
- This is normal for free tier. Use the Cron-job.org tip to keep it warm!

## Contributing

Feel free to submit issues or pull requests to improve this project!
