# Holoholo - E-commerce Website

A full-featured e-commerce website built with Flask, featuring Amazon/Flipkart-like functionality with a modern, responsive design.

## 🌟 Features

### 🛍️ Shopping Features
- **Product Catalog**: Browse products by categories with filtering and sorting
- **Product Details**: Detailed product pages with images, descriptions, and reviews
- **Shopping Cart**: Add, update, and remove items from cart
- **Wishlist**: Save products for later purchase
- **Checkout System**: Complete checkout process with shipping details
- **Order History**: View past orders and track their status

### 🔐 Authentication & User Management
- **User Registration & Login**: Secure authentication system
- **Role-based Access**: Customer and Admin roles
- **Profile Management**: User profile and order history
- **Password Security**: Hashed password storage

### 📊 Admin Panel
- **Dashboard**: Overview of sales, orders, and user statistics
- **Product Management**: Add, edit, and delete products
- **Order Management**: View and update order statuses
- **User Management**: Manage customer accounts
- **Inventory Tracking**: Monitor product stock levels

### 🔍 Search & Discovery
- **Search Functionality**: Find products with autocomplete
- **Category Browsing**: Browse products by category
- **Filtering & Sorting**: Filter by price, category, and sort options
- **Product Reviews**: Customer rating and review system

### 🎨 User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Bootstrap 5 with custom styling
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Accessibility**: Keyboard navigation and screen reader support

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd holoholo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the website**
   - Open your browser and go to `http://localhost:5000`
   - Admin login: `admin` / `admin123`

## 📁 Project Structure

```
holoholo/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   └── uploads/          # Product images
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── products.html     # Product listing
│   ├── product_detail.html # Product details
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout process
│   ├── order_history.html # Order history
│   ├── search_results.html # Search results
│   └── admin/            # Admin templates
│       ├── dashboard.html
│       ├── products.html
│       ├── add_product.html
│       ├── orders.html
│       └── users.html
└── holoholo.db          # SQLite database (created automatically)
```

## 🗄️ Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: User role (customer/admin)
- `created_at`: Account creation timestamp

### Categories
- `id`: Primary key
- `name`: Category name
- `description`: Category description

### Products
- `id`: Primary key
- `name`: Product name
- `description`: Product description
- `price`: Product price
- `stock`: Available quantity
- `image_url`: Product image URL
- `category_id`: Foreign key to categories
- `created_at`: Product creation timestamp

### Orders
- `id`: Primary key
- `user_id`: Foreign key to users
- `total_amount`: Order total
- `status`: Order status (pending/processing/shipped/delivered/cancelled)
- `shipping_address`: Delivery address
- `created_at`: Order timestamp

### Order Items
- `id`: Primary key
- `order_id`: Foreign key to orders
- `product_id`: Foreign key to products
- `quantity`: Item quantity
- `price`: Item price at time of purchase

### Reviews
- `id`: Primary key
- `user_id`: Foreign key to users
- `product_id`: Foreign key to products
- `rating`: Star rating (1-5)
- `comment`: Review text
- `created_at`: Review timestamp

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///holoholo.db
UPLOAD_FOLDER=static/uploads
```

### Database Configuration
The application uses SQLite by default. For production, you can switch to PostgreSQL:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/holoholo'
```

## 🛠️ Customization

### Adding New Categories
Categories are automatically created when the application starts. You can modify the sample categories in `app.py`.

### Styling
- Custom CSS is in `static/css/style.css`
- Bootstrap 5 is used for the base framework
- Font Awesome icons are included

### JavaScript Features
- Search autocomplete
- Cart animations
- Form validation
- Lazy loading
- Smooth scrolling

## 🔒 Security Features

- **Password Hashing**: Passwords are hashed using Werkzeug
- **CSRF Protection**: Built-in CSRF protection with Flask-WTF
- **Session Management**: Secure session handling
- **Input Validation**: Form validation and sanitization
- **Role-based Access**: Admin-only routes protection

## 📱 Responsive Design

The website is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Different screen sizes and orientations

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:

1. **WSGI Server**: Use Gunicorn or uWSGI
2. **Web Server**: Nginx as reverse proxy
3. **Database**: PostgreSQL for better performance
4. **Environment**: Set `FLASK_ENV=production`
5. **SSL**: Enable HTTPS with SSL certificates

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## 🔮 Future Enhancements

- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Product recommendations
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Analytics dashboard
- [ ] Inventory alerts
- [ ] Bulk product import/export
- [ ] Advanced admin features

## 📊 Sample Data

The application comes with sample data:
- 5 product categories
- 8 sample products
- Admin user (admin/admin123)

You can modify the sample data in the `app.py` file under the database initialization section.

---

**Happy Shopping! 🛍️** 