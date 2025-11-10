[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)](https://flask.palletsprojects.com/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](#)
[![Last Commit](https://img.shields.io/github/last-commit/shagul-hameed-rafiq/ai-career-recommender?color=yellow)](https://github.com/shagul-hameed-rafiq/ai-career-recommender/commits/main)


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
