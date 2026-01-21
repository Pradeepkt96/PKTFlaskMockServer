from flask import Flask, jsonify, request, abort
import json
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path("data/customers.json")

with open(DATA_FILE) as f:
    CUSTOMERS = json.load(f)

@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/api/customers", methods=["GET"])
def get_customers():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit
    data = CUSTOMERS[start:end]

    return jsonify({
        "data": data,
        "total": len(CUSTOMERS),
        "page": page,
        "limit": limit
    })

@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    for customer in CUSTOMERS:
        if customer["customer_id"] == customer_id:
            return jsonify(customer)
    abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
