import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("==================================================")
print("  6G Deep-Predictive ANN Training Module v1.0")
print("==================================================")
print("[*] Loading congestion_dataset.csv...")

df = pd.read_csv('congestion_dataset.csv')
X = df[['Queue_Size(KB)', 'Latency(ms)', 'Bandwidth(Mbps)']]
y = df['Prediction_Action']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("[*] Initializing Artificial Neural Network (Hidden Layers: 2x16)...")
ann_model = MLPClassifier(hidden_layer_sizes=(16, 16), max_iter=1000, random_state=42)

print("[*] Training the ANN on 6G backhaul telemetry...")
ann_model.fit(X_train, y_train)

predictions = ann_model.predict(X_test)
accuracy = accuracy_score(y_test, predictions) * 100

print("==================================================")
print(f"[SUCCESS] ANN Training Complete!")
print(f"[RESULTS] Predictive Accuracy: {accuracy:.2f}%")
print("==================================================")

print("\n[*] 20% TEST SET VERIFICATION: GROUND TRUTH vs. AI PREDICTION")
print(f"{'Queue(KB)':<12} | {'Lat(ms)':<10} | {'BW(Mbps)':<10} | {'Actual (IF/ELSE)':<20} | {'AI Predicted':<20} | Match")
print("-" * 85)

# Loop through the 20% test data to compare answers side-by-side
for i in range(len(predictions)):
    q = X_test.iloc[i]['Queue_Size(KB)']
    l = X_test.iloc[i]['Latency(ms)']
    b = X_test.iloc[i]['Bandwidth(Mbps)']
    actual = y_test.iloc[i]
    pred = predictions[i]
    
    # Add a visual checkmark if the AI got it right
    match = "[MATCH]" if actual == pred else "[FAIL]"
    
    print(f"{q:<12.2f} | {l:<10.2f} | {b:<10.2f} | {actual:<20} | {pred:<20} | {match}")

print("-" * 85)