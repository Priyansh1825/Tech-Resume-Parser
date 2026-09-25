import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Configuration
DATASET_PATH = "resume_dataset.csv"
MODEL_SAVE_PATH = "role_classifier_model.pkl"

def train_ai_model():
    print("🧠 Initializing AI Training Sequence...")

    # 1. Load the Dataset
    try:
        df = pd.read_csv(DATASET_PATH)
        print(f"📊 Loaded dataset with {len(df)} resumes.")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return

    # 2. Clean the Data
    # Drop any rows where the text might be completely empty
    df = df.dropna(subset=['Resume_Text', 'Job_Role'])
    print(f"🧹 Cleaned dataset. Training on {len(df)} valid resumes.")

    # 3. Split the Data (80% for Training, 20% for Testing)
    # We hide 20% of the resumes from the AI so we can test its true accuracy later.
    X = df['Resume_Text']
    y = df['Job_Role']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"📚 Training AI on {len(X_train)} resumes...")
    print(f"🧪 Reserving {len(X_test)} resumes for accuracy testing...")

    # 4. Build the Machine Learning Pipeline
    # TF-IDF turns words into math. LinearSVC learns the patterns.
    ai_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.85, min_df=3, ngram_range=(1, 2))),
        ('clf', LinearSVC(random_state=42, class_weight='balanced'))
    ])

    # 5. Train the Model! (This is where the actual learning happens)
    print("\n⚙️ Training in progress... (This might take a minute depending on your CPU)")
    ai_pipeline.fit(X_train, y_train)
    print("✅ Training Complete!")

    # 6. Evaluate the Model
    print("\n📈 Evaluating AI Accuracy against the hidden test data...")
    predictions = ai_pipeline.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    print(f"\n🎯 FINAL AI ACCURACY: {round(accuracy * 100, 2)}%")
    
    # 7. Save the trained brain to your hard drive
    joblib.dump(ai_pipeline, MODEL_SAVE_PATH)
    print(f"\n💾 Saved the trained AI model as: {MODEL_SAVE_PATH}")
    print("You can now connect this model directly into your Streamlit app!")

if __name__ == "__main__":
    train_ai_model()