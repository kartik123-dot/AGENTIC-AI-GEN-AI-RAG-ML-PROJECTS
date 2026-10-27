# Restaurant Reviews: TF-IDF + classification model comparison
# Install if needed:
# python -m pip install pandas scikit-learn matplotlib xgboost lightgbm

import warnings
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, confusion_matrix, roc_auc_score,
    roc_curve, classification_report
)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

# Optional libraries: script continues if either package is not installed.
try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None

try:
    from lightgbm import LGBMClassifier
except ImportError:
    LGBMClassifier = None

warnings.filterwarnings("ignore")

# Change this path to your file location.
FILE_PATH = r"D:\project\resume project feedback\Restaurant_Reviews.tsv"

dataset = pd.read_csv(FILE_PATH, sep="\t", quoting=3)
dataset = dataset.dropna(subset=["Review", "Liked"]).copy()
dataset["Review"] = dataset["Review"].astype(str)
dataset["Liked"] = dataset["Liked"].astype(int)

X = dataset["Review"]
y = dataset["Liked"]

# Keep the same 80/20 split for a fair model comparison.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0, stratify=y
)

models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=0),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Random Forest": RandomForestClassifier(
        n_estimators=300, random_state=0, n_jobs=-1,
        class_weight="balanced"
    ),
    "Decision Tree": DecisionTreeClassifier(
        random_state=0, min_samples_leaf=3, class_weight="balanced"
    ),
    "SVM (RBF)": SVC(kernel="rbf", probability=True, random_state=0),
    "Naive Bayes": MultinomialNB()
}

if XGBClassifier is not None:
    models["XGBoost"] = XGBClassifier(
        n_estimators=250, max_depth=4, learning_rate=0.05,
        subsample=0.9, colsample_bytree=0.9,
        eval_metric="logloss", random_state=0, n_jobs=4
    )
else:
    print("XGBoost skipped: install it with python -m pip install xgboost")

if LGBMClassifier is not None:
    models["LightGBM"] = LGBMClassifier(
        n_estimators=250, learning_rate=0.05,
        num_leaves=15, verbosity=-1, random_state=0, n_jobs=4
    )
else:
    print("LightGBM skipped: install it with python -m pip install lightgbm")

all_results = []
roc_data = {}

# Compare both settings: retain stopwords vs remove English stopwords.
for setting, stop_words in [
    ("Without stopwords", None),
    ("With English stopwords removed", "english")
]:
    vectorizer = TfidfVectorizer(
        stop_words=stop_words,
        lowercase=True,
        ngram_range=(1, 1),
        max_features=10000,
        sublinear_tf=True
    )

    # Fit TF-IDF only on training text to avoid data leakage.
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    for name, model in models.items():
        model.fit(X_train_tfidf, y_train)
        train_pred = model.predict(X_train_tfidf)
        test_pred = model.predict(X_test_tfidf)

        if hasattr(model, "predict_proba"):
            test_scores = model.predict_proba(X_test_tfidf)[:, 1]
        else:
            test_scores = model.decision_function(X_test_tfidf)

        train_accuracy = accuracy_score(y_train, train_pred)
        test_accuracy = accuracy_score(y_test, test_pred)
        auc = roc_auc_score(y_test, test_scores)

        all_results.append({
            "Stopword setting": setting,
            "Algorithm": name,
            # These are accuracy-based proxies, not formal statistical bias/variance.
            "Bias score (train accuracy)": train_accuracy,
            "Variance score (test accuracy)": test_accuracy,
            "Accuracy": test_accuracy,
            "ROC-AUC": auc,
            "Train-test gap": train_accuracy - test_accuracy
        })

        # Keep ROC data to plot the best AUC model in each stopword setting.
        fpr, tpr, _ = roc_curve(y_test, test_scores)
        roc_data[(setting, name)] = (fpr, tpr, auc)

        print(f"\n{setting} | {name}")
        print(f"Train accuracy / bias proxy: {train_accuracy:.3f}")
        print(f"Test accuracy / variance proxy: {test_accuracy:.3f}")
        print(f"ROC-AUC: {auc:.3f}")
        print("Confusion matrix:")
        print(confusion_matrix(y_test, test_pred))

results = pd.DataFrame(all_results)
results = results.sort_values(
    ["Stopword setting", "ROC-AUC"], ascending=[True, False]
)
results.to_csv("restaurant_reviews_tfidf_results.csv", index=False)
print("\n=== Full comparison (sorted by AUC within each setting) ===")
print(results.round(3).to_string(index=False))

# Plot ROC curves for all models, separated by stopword setting.
for setting in results["Stopword setting"].unique():
    plt.figure(figsize=(8, 6))
    for name in models:
        fpr, tpr, auc = roc_data[(setting, name)]
        plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--", label="Random classifier")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC curves - {setting}")
    plt.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    safe_name = setting.lower().replace(" ", "_")
    plt.savefig(f"roc_{safe_name}.png", dpi=150)
    plt.show()
