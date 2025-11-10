import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "career_pipeline.pkl")
if not os.path.exists(MODEL_PATH):
    raise SystemExit(f"No model found at {MODEL_PATH}. Run train_model.py first.")

pipe = joblib.load(MODEL_PATH)
print("Loaded pipeline:", pipe)

# components
tfidf = pipe.named_steps["tfidf"]
clf = pipe.named_steps["clf"]

# classes
classes = list(clf.classes_)
print("\nClasses (labels):")
for i,c in enumerate(classes):
    print(i, "-", c)

# vocabulary size and sample words
vocab = tfidf.get_feature_names_out()
print(f"\nTF-IDF vocab size: {len(vocab)}")
print("Sample vocabulary (first 20):", vocab[:20].tolist())

# show top positive weights (features) for each class
coef = clf.coef_  # shape: (n_classes, n_features)
if coef.shape[1] != len(vocab):
    print("Warning: coef/features length mismatch")

print("\nTop features per class (words that push prediction toward the class):")
top_k = 15
for idx, cls in enumerate(classes):
    coefs = coef[idx]
    top_idx = np.argsort(coefs)[-top_k:][::-1]
    top_words = [vocab[i] for i in top_idx]
    top_vals = [float(coefs[i]) for i in top_idx]
    print(f"\n{cls} (top {top_k}):")
    for w, v in zip(top_words, top_vals):
        print(f"  {w}  ({v:.4f})")


import joblib, os
pipe = joblib.load("backend/model/career_pipeline.pkl")
tfidf = pipe.named_steps["tfidf"]
vocab = set(tfidf.get_feature_names_out())
for token in ["excel","word","microsoft","administration","ms word","ms excel"]:
    print(token, "IN VOCAB?" , token in vocab)
