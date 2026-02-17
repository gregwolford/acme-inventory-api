# Acme Inventory API

A Flask-based REST API for managing product inventory and users. This demo application showcases GitHub Advanced Security (GHAS) features including CodeQL, Secret Scanning, Dependabot, and Copilot Autofix.

## 🎯 Purpose

This repository is designed to demonstrate GitHub's native security capabilities in an enterprise setting. It intentionally contains vulnerabilities for detection and remediation demos:
- SQL injection vulnerability (CodeQL detection)
- Vulnerable dependencies (Dependabot alerts)
- Secret detection capabilities (Push Protection)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/gregwolford/acme-inventory-api.git
cd acme-inventory-api

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### Root
```
GET /
```
Returns API information and available endpoints.

### Products
```
GET /products          # List all products
POST /products         # Add a new product
GET /search?q={term}   # Search products (⚠️ Contains SQL injection vulnerability)
```

**Example: Add a product**
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "category": "Electronics",
    "price": 999.99,
    "stock": 50
  }'
```

### Users
```
GET /users             # List all users
```

### Admin
```
GET /admin/export      # Export inventory as CSV
```

## 🗄️ Database

Uses SQLite with two tables:
- **products** — id, name, category, price, stock
- **users** — id, username, email, role

The database is automatically initialized on first run.

## 🔒 Security Features Demonstrated

### 1. CodeQL Analysis
- **Finding:** SQL injection in `/search` endpoint (line 76)
- **Detection:** Automated via GitHub Actions workflow
- **Fix:** Copilot Autofix suggests parameterized queries

### 2. Secret Scanning & Push Protection
- Prevents hardcoded secrets from entering git history
- Blocks commits containing AWS keys, API tokens, etc.
- **Demo:** Try committing a file with `AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"`

### 3. Dependabot Alerts
- Monitors `requirements.txt` for vulnerable dependencies
- Auto-generates PRs with version bumps
- **Current alerts:** Multiple CVEs in older package versions

### 4. Copilot Code Agent
- Can autonomously fix issues from GitHub Issues
- Creates branches, writes fixes, runs tests, opens draft PRs
- **Demo:** Assign issue "Fix SQL injection" to Copilot

## 🧪 Testing

```bash
# Run tests (if tests are configured)
python -m pytest tests/
```

## ⚠️ Known Vulnerabilities (Intentional)

This is a **demo application** with deliberate security issues:

1. **SQL Injection** — `/search` endpoint uses string concatenation
2. **Outdated Dependencies** — requirements.txt contains vulnerable packages
3. **Debug Mode** — Flask runs with `debug=True` in production config

**DO NOT use this code in production.**

## 📋 Demo Workflow

For interview/demo purposes:

1. **Enable GHAS features** in repo Settings > Security
2. **Wait for CodeQL** to run and detect SQL injection
3. **Show Copilot Autofix** suggestion for remediation
4. **Demonstrate Push Protection** by attempting to commit a secret
5. **Review Dependabot PRs** for dependency updates

See `DEMO_SCRIPT.md` for detailed demo flow.

## 🛠️ Technology Stack

- **Framework:** Flask 2.3.2
- **Database:** SQLite3
- **Python:** 3.8+
- **CI/CD:** GitHub Actions
- **Security:** GitHub Advanced Security (CodeQL, Dependabot, Secret Scanning)

## 📄 License

MIT License - This is demo/training material.

## 👤 Author

Greg Wolford

**🎓 Learning Resources:**

- [GitHub Advanced Security Docs](https://docs.github.com/en/code-security)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Copilot Autofix Guide](https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/about-autofix-for-codeql-code-scanning)
