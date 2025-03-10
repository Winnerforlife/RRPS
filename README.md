# Refund Request Processing System (RRPS) 🏦💰

A Django-based system for processing refund requests, including IBAN validation and automated email notifications.

## 🚀 Features
- User authentication (SignUp, Login, Logout, Password Reset)
- Refund request submission and tracking
- IBAN validation via API
- Email notifications on status updates
- Admin panel for managing refund requests

---

## 📌 Getting Started

### 1️⃣ **Clone the repository**
```bash
git clone https://github.com/Winnerforlife/RRPS.git
cd rrps
```
or by ssh:

```bash
git clone git@github.com:Winnerforlife/RRPS.git
cd rrps
```

### 2️⃣ **Create and activate a virtual environment**
#### **For macOS & Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```
#### **For Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Configure environment variables**
Create a `.env` file in the root directory and add your API keys & database settings:
```
SECRET_KEY='your-secret-key'
DEBUG=True

DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='127.0.0.1'
DB_PORT=5432

IBAN_API_KEY='your-api-key'
IBAN_API_URL='your-api-url'

DEFAULT_FROM_EMAIL='your-email@example.com'
```

### 5️⃣ **Run migrations**
```bash
python manage.py migrate
```

### 6️⃣ **Create a superuser**
```bash
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### 7️⃣ **Start the development server**
```bash
python manage.py runserver
```
Now open your browser and go to:  
🔜 **http://127.0.0.1:8000/accounts/login/**  

---

## 🔥 Running Tests
To ensure everything works correctly, run:
```bash
python manage.py test
```

---

## 📌 Admin Panel
To manage refund requests, log in as a superuser at:
🔜 **http://127.0.0.1:8000/admin/**

---

## 📌 API Integration (IBAN Validation by [abstractapi.com](https://www.abstractapi.com/api/iban-validation))
The project integrates with an IBAN validation API. Ensure you have a valid **IBAN_API_KEY** in `.env`.

---

## 🤝 Contributing
1. Fork the repository
2. Create a new branch: `git checkout -b feature/branch-name`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature/branch-name`
5. Create a Pull Request 🚀

---

## 📩 Contact
If you have any questions, feel free to reach out:
- 📧 Email: 1stanislavshevchuk@gmail.com
- 🐙 GitHub: [Winnerforlife](https://github.com/Winnerforlife)

