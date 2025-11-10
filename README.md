[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# AI Career Recommender
Lightweight full-stack demo: **Flask** backend + **React (Vite)** frontend + **scikit-learn** model.  
Predicts likely career paths from user skills & interests.

## Quick start (development)

### Backend
```bash
cd backend
# activate venv (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_model.py    # creates model/career_pipeline.pkl
python app.py            # runs backend on http://127.0.0.1:5000
