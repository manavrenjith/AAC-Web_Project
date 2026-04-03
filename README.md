# AAC Web Project

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![License](https://img.shields.io/badge/License-MIT-green)

AAC Web Project is a Flask-based Augmentative and Alternative Communication (AAC) web app that helps users communicate using icons, sentence building, and speech tools.

The app includes role-based flows (user/caregiver) and supports:
- Communication boards with categories
- Sentence builder
- Text-to-speech and speech-to-text
- Caregiver content management (icons, categories, sentences)
- Image-to-text support using BLIP + translation to Malayalam + generated audio

## Tech Stack
- Backend: Python, Flask
- Frontend: HTML (Jinja templates), CSS, JavaScript
- AI/ML: PyTorch, Transformers (BLIP, mBART)
- Speech: gTTS and browser speech APIs
- Storage: JSON file (`data.json`)

## Project Structure

```text
AAC-Web_Project/
|- app.py
|- data.json
|- requirements.txt
|- templates/
|- static/
|  |- css/
|  |- js/
|  |- images/
|  |- audio/
|- add_images.py
```

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd AAC-Web_Project
```

### 2. Create and activate a virtual environment
Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

The app runs at:
- http://127.0.0.1:5000

## Main Features
- User login/register and role-based navigation
- AAC communication board with category filtering
- Sentence creation and playback
- Text-to-speech endpoint (`/tts`) for reliable audio playback
- Speech-to-text input in the browser
- Caregiver dashboard to add/edit/delete icons, sentences, and categories

## Screenshots

### App Logo
![AAC Logo](static/images/aac_logo.svg)

### UI Preview
Add screenshots after taking them from your running app, for example:
- `docs/screenshots/login.png`
- `docs/screenshots/communication-board.png`
- `docs/screenshots/caregiver-dashboard.png`

Example markdown to use:

```md
![Login Page](docs/screenshots/login.png)
![Communication Board](docs/screenshots/communication-board.png)
![Caregiver Dashboard](docs/screenshots/caregiver-dashboard.png)
```

## Demo Credentials
Use this section if you want visitors to test quickly.

```text
Caregiver
Username: your_caregiver_username
Password: your_caregiver_password

User
Username: your_user_username
Password: your_user_password
```

## Notes
- Some features download large model files on first use (Transformers models).
- Uploaded and generated assets are stored in `static/images/custom` and `static/audio`.
- App data is persisted in `data.json`.

## Future Improvements
- Move from JSON storage to a database
- Add tests for routes and data operations
- Add environment-based configuration for production
- Add authentication hardening and password hashing

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE).
