# 🛒 E-Commerce Inventory, Cart & Order Management System

A modern full-stack E-Commerce web application built using **Python Flask**, **SQLite**, **Bootstrap 5**, and **Jinja templates**.  
It features **role-based access control**, **shopping cart**, **order checkout**, **admin product & order management**, **product images**, **toast notifications**, **dark/light theme**, and more.

---

## 🚀 Features

### 👤 User Features
- Register / Login / Logout system
- Browse products with search & category filter
- View product details & images
- Add to cart & update item quantities
- Checkout and order placement
- View order history with status tracking
- Dark / Light mode toggle
- Toast alerts & smooth UI interactions

### 🧑‍💼 Admin Features
- Role-based admin account access
- Dashboard analytics (products, orders count, pending orders)
- Manage products (Create, Update, Delete)
- Upload product images
- Manage orders with **status update dropdown**
- Order filtering based on status
- Product stock updates
- Admin-only sidebar navigation

---

## 🗂 Project Structure
```bash
ecommerce-flask/
├── app.py
├── config.py
├── instance/
│ └── ecommerce.db
├── models/
│ └── models.py
├── routes/
│ ├── auth_routes.py
│ ├── product_routes.py
│ ├── cart_routes.py
│ └── admin_routes.py
├── utils/
│ └── helpers.py
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── products.html
│ ├── cart.html
│ ├── checkout.html
│ ├── orders.html
│ └── admin/
│ ├── admin_dashboard.html
│ └── manage_orders.html
├── static/
│ ├── css/style.css
│ ├── js/script.js
│ └── images/
├── requirements.txt
└── README.md
```

---

## 🧠 Database Design (Modern Normalized Schema)

| Table | Description |
|--------|------------|
| users | User accounts with role control |
| products | Product catalog with stock & images |
| categories | Product grouping |
| cart_items | Items added to shopping cart |
| orders | Full order tracking with timestamps |
| order_items | Product-wise quantity & price history |
| payments | Payment record for each order |
| wishlist | Saved items |
| reviews | Ratings and comments |
| addresses | Shipping addresses |
| audit_logs | Admin system activities |

### ER Diagram Overview


users ───< orders ───< order_items >── products ───< categories
└──< cart_items
└──< wishlist
└──< reviews
orders ───< payments
products ───< product_images


---

## ⚙ Installation & Setup

### 1️⃣ Clone repository
```bash
git clone <repo-url>
cd ecommerce-flask
```
### 2️⃣ Create & Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application
```bash
python app.py
```

### 5️⃣ Access in browser
```bash
http://127.0.0.1:5000/
```

###🔐 Admin Account Setup

Option A — via SQLite
```basg
UPDATE users SET is_admin = 1 WHERE email = 'admin@gmail.com';
```

Option B — create from app
```bash
python seed_data.py
```

Admin login:

Email: admin@gmail.com
Password: admin123

## 🛠 Technologies Used

### **Frontend**
- HTML5
- CSS3
- JavaScript (ES6)
- Bootstrap 5
- Jinja2 Template Engine

### **Backend**
- Python Flask Framework

### **Database**
- SQLite (Lightweight relational DB)
- SQLAlchemy ORM for database abstraction

### **Security**
- Werkzeug Security (Password hashing & salting)

### **UI Enhancements**
- Toast Notifications
- Dark / Light Theme Toggle
- Responsive Flexbox Layout
- Sticky Navbar & Smooth Interactions
- Icons (Bootstrap Icons)

### **Other Tools**
- Virtual Environment (venv)
- Git & GitHub for version control
- SQLite3 CLI for DB administration



