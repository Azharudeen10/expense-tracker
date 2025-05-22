from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
DATA_FILE = 'data/expenses.csv'

os.makedirs('data',exist_ok=True)
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['amount','category','date'])
    df.to_csv(DATA_FILE, index=False)
    
    
@app.route('/add_expense', methods=["POST"])
def add_expense():
    data = request.json
    try:
        data['amount'] = int(data['amount'])  # Force numeric type
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount format'}), 400

    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    df.to_csv(DATA_FILE, index=False)
    return jsonify({'message': 'Expense added successfully'})


@app.route('/summary', methods=['GET'])
def summary():
    df = pd.read_csv(DATA_FILE)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    summary = df.groupby('category')['amount'].sum().reset_index()
    total = summary['amount'].sum()
    summary['percentage'] = (summary['amount'] / total * 100).round(2)
    return jsonify(summary.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)