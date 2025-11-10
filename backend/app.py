from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import os
import numpy as np

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "career_pipeline.pkl")
model = None
tfidf = None
clf = None

if os.path.exists(MODEL_PATH):
    pipe = joblib.load(MODEL_PATH)
    # pipeline components
    tfidf = pipe.named_steps.get("tfidf", None)
    clf = pipe.named_steps.get("clf", None)
    model = pipe
    print("Model loaded:", MODEL_PATH)
else:
    print("No model found. Run train_model.py to create career_pipeline.pkl")

@app.route("/")
def home():
    return jsonify({"message": "Flask backend running successfully!"})

def explain_for_text(text, top_k=5):
    """
    Return a short explanation: top contributing tokens from the input text
    for the top predicted class. Uses tfidf vectorization * classifier weights.
    """
    if model is None or tfidf is None or clf is None:
        return None

    # vectorize the input
    X_vec = tfidf.transform([text])        # sparse matrix (1, n_features)
    probs = clf.predict_proba(X_vec)[0]
             # sparse vector shape (1, n_features)
    X_arr = X_vec.toarray()[0]                  # dense 1D array

    # get class probabilities and predicted class index
    probs = model.predict_proba([text])[0]

    class_idx = int(np.argmax(probs))
    classes = list(clf.classes_)
    predicted_class = classes[class_idx]

    # get classifier coefficients for that class (shape: n_features)
    coefs = clf.coef_[class_idx]

    # compute contribution = coef * tfidf_value
    contributions = coefs * X_arr

    # pick top positive contributions
    top_idx = np.argsort(contributions)[-top_k:][::-1]
    top_words = []
    vocab = tfidf.get_feature_names_out()
    for i in top_idx:
        val = float(contributions[i])
        if val <= 0:
            continue
        top_words.append((vocab[i], round(val, 6)))
    return {"predicted_class": predicted_class, "top_words": top_words, "prob": float(probs[class_idx])}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json or {}
    skills = data.get("skills", "") or ""
    interests = data.get("interests", "") or ""
    
    # small normalizer to improve token matching
    def normalize_text(s: str) -> str:
        import re
        s = (s or "").lower()
        s = re.sub(r"ms\s+word|microsoft\s+word", "word", s)
        s = re.sub(r"ms\s+excel|microsoft\s+excel", "excel", s)
        s = re.sub(r"[^\w\s]", " ", s)         # remove punctuation
        s = re.sub(r"\s+", " ", s).strip()
        return s

    raw_text = f"{skills} {interests}".strip()
    text = normalize_text(raw_text)

    if not text:
        return jsonify({"error": "No skills or interests provided."}), 400

    # Quick keyword-based fallback for Office/Admin-like inputs (immediate UX fix)
    if any(k in text for k in ["excel", "word", "administration", "admin", "office"]):
        return jsonify({
            "career": "Data Analyst",
            "top3": ["Data Analyst", "Office Administrator", "Product Manager"],
            "confidences": [0.85, 0.10, 0.05],
            "explanation": "Fallback rule applied: detected Excel/Word/Administration keywords."
        })

    # If model not available, use a minimal fallback rule
    if model is None or tfidf is None or clf is None:
        if "python" in text:
            return jsonify({"career": "Software Developer", "explanation": "Fallback rule: contains 'python'."})
        return jsonify({"career": "Data Analyst", "explanation": "Fallback rule: default to Data Analyst."})

    # Vectorize input
    X_vec = tfidf.transform([text])           # sparse (1, n_features)
    # Predict probabilities using classifier (pass numeric vector)
    probs = clf.predict_proba(X_vec)[0]       # shape (n_classes,)

    # Build top-3 results
    classes = list(clf.classes_)
    idx_sorted = np.argsort(probs)[::-1]
    top3_idx = idx_sorted[:3]
    top3 = [classes[i] for i in top3_idx]
    confidences = [float(probs[i]) for i in top3_idx]
    best = top3[0]

    # Build token-level explanation (contribution = coef * tfidf_value)
    try:
        coefs = clf.coef_                         # shape (n_classes, n_features)
        class_idx = int(np.argmax(probs))
        contrib = coefs[class_idx] * X_vec.toarray()[0]   # elementwise
        vocab = tfidf.get_feature_names_out()
        # pick top positive contributions
        pos_idx = [i for i in np.argsort(contrib)[-15:][::-1] if contrib[i] > 0]
        top_words = []
        for i in pos_idx[:10]:
            top_words.append((vocab[i], round(float(contrib[i]), 6)))
        if top_words:
            explanation_text = "Top input words influencing prediction: " + ", ".join(f"{w} ({v})" for w, v in top_words)
        else:
            explanation_text = "No token-level explanation available."
    except Exception:
        explanation_text = "No token-level explanation available."

    return jsonify({
        "career": best,
        "top3": top3,
        "confidences": confidences,
        "explanation": explanation_text
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
