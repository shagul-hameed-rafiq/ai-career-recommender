import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "training.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "career_pipeline.pkl")

os.makedirs(os.path.join(os.path.dirname(__file__), "model"), exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA_PATH)
# combine skills + interests into a single text feature
df["text"] = df["skills"].fillna("") + " " + df["interests"].fillna("")

X = df["text"]
y = df["label"]

# 2. train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. pipeline: TF-IDF -> LogisticRegression
pipe = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=3000)),
    ("clf", LogisticRegression(max_iter=1000))
])

pipe.fit(X_train, y_train)

# 4. Evaluate
preds = pipe.predict(X_test)
print("=== Classification Report ===")
print(classification_report(y_test, preds))

# 5. Save pipeline
joblib.dump(pipe, MODEL_PATH)
print(f"Saved model pipeline to {MODEL_PATH}")
