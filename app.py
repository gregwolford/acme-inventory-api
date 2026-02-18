from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = "inventory.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'viewer'
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return jsonify({
        "app": "Acme Inventory API",
        "version": "1.2.0",
        "endpoints": ["/products", "/users", "/search"]
    })


@app.route("/products", methods=["GET"])
def list_products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(row) for row in products])


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    conn = get_db()
    conn.execute(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        (data["name"], data["category"], data["price"], data["stock"])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "created"}), 201


# --- Search endpoint: parameterized query to avoid SQL injection ---
@app.route("/search")
def search_products():
    query = request.args.get("q", "")
    search_pattern = f"%{query}%"
    conn = get_db()
    results = conn.execute(
        "SELECT * FROM products WHERE name LIKE ?",
        (search_pattern,),
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in results])


# --- DELIBERATELY VULNERABLE: hardcoded secret for demo purposes ---
@app.route("/users")
def list_users():
    conn = get_db()
    users = conn.execute("SELECT id, username, email, role FROM users").fetchall()
    conn.close()
    return jsonify([dict(row) for row in users])


@app.route("/admin/export")
def export_data():
    """Export inventory data as CSV."""
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    csv_lines = ["id,name,category,price,stock"]
    for row in products:
        csv_lines.append(f"{row['id']},{row['name']},{row['category']},{row['price']},{row['stock']}")

    return "\n".join(csv_lines), 200, {"Content-Type": "text/csv"}


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
