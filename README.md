# 🛒 Multi-Tenant E-commerce API with Role-Based Access Control (RBAC)
A scalable, secure Django REST Framework-based API for a multi-tenant e-commerce platform that allows multiple vendors to manage their own products and orders, with advanced role-based access control (RBAC).

---

## 🚀 Features
- 🔐 **JWT Authentication** using `djangorestframework-simplejwt`
- 👤 **Role-Based Access Control**:
  - **Admin**: Manage and view all vendors, products, and orders
  - **Vendor**: Manage only their own products and orders
  - **Customer**: Place orders but cannot modify products
- 🧩 **Multi-Tenant Architecture**
- 📦 **Product and Order Management**
- 🚦 **Throttling & Rate Limiting**
- ⚡ **Optimized Queries & Pagination**
- 🔍 **Search & Filtering Support**
---

## 🏗️ Tech Stack
- Django
- Django REST Framework
- djangorestframework-simplejwt
- SQLite3 (DB)
- Redis (for caching, optional)
- django-filter
- drf-throttling

---


## Installation
1. **Clone the repository:**
 ```sh
https://github.com/Rafiul29/multikart.git
cd multikart
```
2. **Install dependencies:**
```sh
pip install -r requirements.txt
```
3. **Configure SQLite3:**
SQLite3 is the default database for Django, so no additional setup is needed for SQLite. Just ensure that the following is in your settings.py:

settings.py (Database Configuration)
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # This is where the SQLite database file will be stored
    }
}
```


4. **Run migrations:**
Create the necessary database tables by running the following commands:
```sh
python manage.py makemigrations
python manage.py migrate
```

5. **Start the server:**
Start the Django development server:
```sh
python manage.py runserver
```
6. **Access the Application:**
Open your browser and navigate to http://localhost:8000/ to access the API.


--- 
## 🚀 Base URL
`http://127.0.0.1:8000`

## 🔐 User Authentication

### 📌 Register
- **URL:** `api/v1/auth/register/`
- **Method:** `POST`
- **Access:** Public

#### ✅ Request Body
```sh
{
  "username": "rafiul",
  "email": "rafiul123@gmail.com",
  "first_name": "Rafiul",
  "last_name": "Islam",
  "password": "Rafi@#12",
  "confirm_password": "Rafi@#12"
}
```
#### 🟢 Response 201 Created
```sh
{
  "message": "User registered successfully!",
  "tokens": {
    "refresh": "your_refresh_token",
    "access": "your_access_token"
  }
}
```
#### 🔴 Response 400 Bad Request - Missing Fields
```sh
{
  "error": {
    "username": "This field is required.",
    "first_name": "This field is required.",
    "last_name": "This field is required.",
    "email": "This field is required.",
    "password": "This field is required.",
    "confirm_password": "This field is required."
  }
}
```
#### 🔴 Response 400 Bad Request - Existing User
```sh
{
  "error": {
    "username": "A user with that username already exists."
  }
}
```
#### 🔴 Response 400 Bad Request - Email Already Exists
```sh
{
  "error": {
    "email": "Email already exists."
  }
}
```
#### 🔴 Response 400 Bad Request - Password Mismatch
```sh
{
  "error": {
    "password": "Passwords don't match."
  }
}
```
### 🔐 Login
- **URL:** `api/v1/auth/login/`
- **Method:** `POST`
- **Access:** Public

#### ✅ Request Body
```sh
{
  "username": "rafiul",
  "password": "Rafi@#12"
}
```
#### 🟢 Response 200 OK
```sh
{
  "message": "user login successful",
  "data": {
    "id": 1,
    "first_name": "Rafiul",
    "last_name": "Islam",
    "username": "rafiul",
    "email": "rafiul123@gmail.com",
    "role": "customer"
  },
  "tokens": {
    "refresh": "your_refresh_token",
    "access": "your_access_token"
  }
}
```
#### ✅ Request Body
```sh
{ }
```
#### 🔴 Response 400 Bad Request - Missing Fields
```sh
{
    "error": {
        "username": "Username is required.",
        "password": "Password is required."
    }
}
```
#### 🔴 Response 400 Bad Request - 401 Unauthorized
```sh
{
    "error": "please provided valid credentials"
}
```
### 🔐 Logout
- **URL:** `api/v1/auth/login/`
- **Method:** `POST`
- **Access:** Public
#### ❌ Request Body (Missing Refresh Token)
```sh
{}
```
#### 🔴 Response 400 Bad Request - Missing Fields
```sh
{
  "error": "Refresh token is required"
}
```
#### ✅ Request Body
```sh
{
  "refresh": "your_refresh_token"
}
```
#### 🟢 Response 200 OK
```sh
{
  "message": "User logged out successfully"
}
```
#### 🔴 Response  - 401 Unauthorized
```sh
{
    "error": "please provided valid credentials"
}
```

## 🏪 Vendor API
---

### 📥 Create a  Vendors

- **URL:** `/api/v1/vendors/`
- **Method:** `POST`
- **Access:** Admin Only

#### ✅ Request Body
```sh
{
    "store_name":"this is my shop",
    "user_id":5
}
```
### 📥 Create a  Vendors

- **URL:** `/api/v1/vendors/`
- **Method:** `POST`
- **Access:** Customer 

#### ✅ Request Body
```sh
{
    "store_name":"this is my shop",
}
```

### 📥 Get All Vendors

- **URL:** `/api/v1/vendors/`
- **Method:** `GET`
- **Access:** Admin Only

#### ✅ Sample Request
```sh
GET /api/v1/vendors/
```

#### 🟢 Response 200 OK
```json
[
  {
    "id": 1,
    "user": {
      "id": 5,
      "username": "rafiul"
    },
    "store_name": "Rafiul’s Store"
  },
  {
    "id": 2,
    "user": {
      "id": 6,
      "username": "ayesha"
    },
    "store_name": "Ayesha's Shop"
  }
]
```

#### 🔴 Response 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### 🔴 Response 401 Unauthorized
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

### 🔎 Get Vendor by ID

- **URL:** `/api/v1/vendors/<int:id>/`
- **Method:** `GET`
- **Access:** Admin or Vendor own Profile

#### ✅ Sample Request
```sh
GET /api/v1/vendors/1/
```

#### 🟢 Response 200 OK
```json
{
  "id": 1,
  "user": {
    "id": 5,
    "username": "rafiul"
  },
  "store_name": "Rafiul’s Store"
}
```

#### 🔴 Response 404 Not Found
```json
{
  "detail": "Vendor not found."
}
```

### ✏️ Update Vendor

- **URL:** `/api/v1/vendors/<int:id>/`
- **Method:** `PUT` or `PATCH`
- **Access:** Authenticated admin or Vendor  (can only update their own profile)

#### ✅ Sample Request (PATCH)
```json
{
  "store_name": "Updated Store Name"
}
```

#### 🟢 Response 200 OK
```json
{
  "id": 1,
  "user": {
    "id": 5,
    "username": "rafiul"
  },
  "store_name": "Updated Store Name"
}
```

#### 🔴 Response 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### ❌ Delete Vendor

- **URL:** `/api/v1/vendors/<int:id>/`
- **Method:** `DELETE`
- **Access:** Admin Only

#### ✅ Sample Request
```sh
DELETE /api/v1/vendor/1/
```

#### 🟢 Response 204 No Content
```json
{}
```

#### 🔴 Response 404 Not Found
```json
{
  "detail": "Vendor not found."
}
```

#### 🔴 Response 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```


## 🛒 Product API

---

### 📥 Get All Products

- **URL:** `/api/v1/products/`
- **Method:** `GET`
- **Access:** Public Unauthenticated (Customer show all product ) and Private Authenticated (Admin show all product but vendor uuser  show own product )
- **Description:** Supports filtering by minimum and maximum price, ordering, and searching by product name.

#### ✅ Example Request
```sh
GET api/v1/products/?min_price=100&max_price=1000&ordering=price&search=product
```

#### 🔎 Query Parameters:
| Parameter     | Type     | Description                                |
|---------------|----------|--------------------------------------------|
| `min_price`   | float    | Minimum price of the product               |
| `max_price`   | float    | Maximum price of the product               |
| `ordering`    | string   | Sort by field (e.g. `price`, `-price` ,`name`, `-name`)     |
| `search`      | string   | Search by product name or description      |


#### 🟢 Response 200 OK
```json
{
    "data": [
        {
            "id": 5,
            "name": "laptop",
            "description": "this is a laptop",
            "price": "11.00",
            "stock": 11,
            "vendor": {
                "id": 15,
                "store_name": "this is my book",
                "user": {
                    "id": 3,
                    "username": "rafiul1",
                    "email": "rafiul1123@gmail.com",
                    "first_name": "Rafiul",
                    "last_name": "Islam",
                    "role": "vendor"
                }
            }
        }
    ],
    "pagination": {
        "count": 1,
        "next": null,
        "previous": null
    },
    "success": "Fetched vendors successfully."
}
```

### 🔎 Get Product by ID

- **URL:** `/api/v1/products/<int:id>/`
- **Method:** `GET`
- **Access:** Public can customer  but Private Admin and Vendor 

#### ✅ Sample Request
```sh
GET /api/v1/products/1/
```

#### 🟢 Response 200 OK
```json
{
    "data": {
        "id": 7,
        "name": "Product-6CmsAO",
        "description": "Description: xYBZvrvQzza6odLr10jr",
        "price": "4514.00",
        "stock": 10,
        "vendor": {
            "id": 15,
            "store_name": "this is my book",
            "user": {
                "id": 3,
                "username": "rafiul1",
                "email": "rafiul1123@gmail.com",
                "first_name": "Rafiul",
                "last_name": "Islam",
                "role": "vendor"
            }
        }
    },
    "success": "Product updated."
}
```

#### 🔴 Response 404 Not Found
```json
{
  "detail": "Product not found."
}
```

### ➕ Create Product

- **URL:** `/api/v1/products/`
- **Method:** `POST`
- **Access:** Vendor Only

#### ✅ Sample Request
```json
{
  "name": "Mutton Curry",
  "description": "Rich mutton curry with spices",
  "price": 300.00,
  "stock": 20,
}
```

#### 🟢 Response 201 Created
```json
{
    "data": {
        "id": 7,
        "name": "Product-0ZDuFM",
        "description": "Description: qss2gTmjfmcxV9Utsyoc",
        "price": "4453.00",
        "stock": 39,
        "vendor": {
            "id": 15,
            "store_name": "this is my book",
            "user": {
                "id": 3,
                "username": "rafiul1",
                "email": "rafiul1123@gmail.com",
                "first_name": "Rafiul",
                "last_name": "Islam",
                "role": "vendor"
            }
        }
    },
    "success": "Product created."
}
```

#### 🔴 Response 400 Bad Request
```json
{
    "error": {
        "name": "This field is required.",
        "description": "This field is required.",
        "price": "This field is required.",
        "stock": "This field is required.",
        "vendor": "Invalid data. Expected a dictionary, but got int."
    }
}
```

### ✏️ Update Product

- **URL:** `/api/v1/products/<int:id>/`
- **Method:** `PUT` or `PATCH`
- **Access:** Admin and  Vendor (Owner Only)

#### ✅ Sample Request (PATCH)
```json
{
  "price": 275.00,
  "stock": 30
}
```

#### 🟢 Response 200 OK
```json
{
  "id": 1,
  "vendor": {
    "id": 1,
    "store_name": "Rafiul’s Store"
  },
  "name": "Chicken Biryani",
  "description": "Spicy and delicious biryani",
  "price": 275.00,
  "stock": 30,
}
```

#### 🔴 Response 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```



### ❌ Delete Product

- **URL:** `/api/v1/products/<int:id>/`
- **Method:** `DELETE`
- **Access:** Admin or Vendor (Owner Only)

#### ✅ Sample Request
```sh
DELETE /api/v1/products/1/
```

#### 🟢 Response 204 No Content
```json
{}
```

#### 🔴 Response 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```
#### 🔴 Response 404 Not Found
```json
{
  "detail": "Product not found."
}
```

---

## 📦 Orders API

### ✅ Create Order

- **URL:** `/api/v1/orders/`
- **Method:** `POST`
- **Access:** Private (Authenticated users)

#### 📥 Request Body
```json
{
  "items": [
    { "product": 1, "quantity": 2 },
    { "product": 4, "quantity": 1 }
  ]
}

```

#### 🟢 Response 201 Created
```json
{
    "id": 2,
    "customer": 4,
    "created_at": "2025-04-19T06:01:07.049241Z",
    "status": "pending",
    "items": [
        {
            "id": 2,
            "product": 1,
            "product_name": "laptop",
            "quantity": 2,
            "price_at_order": "11.00",
            "total_price": 22
        },
        {
            "id": 3,
            "product": 4,
            "product_name": "laptop",
            "quantity": 1,
            "price_at_order": "11.00",
            "total_price": 11
        }
    ]
}
```

#### 🔴 Response 400 Bad Request
```json
{
    "error": "Invalid product ID or quantity."
}
```
#### 🔴 Response 403 Forbidden 
```json
{
    "detail": "Only customers can place orders."
}
```

### 📄 Get All Orders

- **URL:** `/api/v1/orders/`
- **Method:** `GET`
- **Access:** Private ( Admin  can see all orders, vendor can see Own Product Orders and Customr sees their own orders)

#### 🟢 Response 200 OK
```json
{
    "data": [
        {
            "id": 1,
            "customer": {
                "id": 4,
                "username": "rafiul12",
                "email": "rafiul1e23@gmail.com",
                "first_name": "Rafiul",
                "last_name": "Islam"
            },
            "created_at": "2025-04-19T05:17:29.962655Z",
            "status": "pending",
            "items": [
                {
                    "id": 1,
                    "product": 1,
                    "product_name": "laptop",
                    "quantity": 1,
                    "price_at_order": "100.00",
                    "total_price": 100
                }
            ]
        },
        {
            "id": 2,
            "customer": {
                "id": 4,
                "username": "rafiul12",
                "email": "rafiul1e23@gmail.com",
                "first_name": "Rafiul",
                "last_name": "Islam"
            },
            "created_at": "2025-04-19T06:01:07.049241Z",
            "status": "pending",
            "items": [
                {
                    "id": 2,
                    "product": 1,
                    "product_name": "laptop",
                    "quantity": 2,
                    "price_at_order": "11.00",
                    "total_price": 22
                },
                {
                    "id": 3,
                    "product": 4,
                    "product_name": "laptop",
                    "quantity": 1,
                    "price_at_order": "11.00",
                    "total_price": 11
                }
            ]
        }
    ],
    "pagination": {
        "count": 3,
        "next": "http://127.0.0.1:8000/api/v1/orders/?page=2",
        "previous": null
    },
    "success": "Fetched orders successfully."
}
```


#### 🔴 Response 401 Unauthorized
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

### 📋 Get Single Order

- **URL:** `/api/v1/orders/<int:id>/`
- **Method:** `GET`
- **Access:**  Private ( Admin  can see  order, vendor can see Own Product Order and Customr sees their own order)

#### 🟢 Response 200 OK
```json
{
    "id": 5,
    "customer": {
        "id": 5,
        "username": "sadman",
        "email": "sadman@gmail.com",
        "first_name": "sadman",
        "last_name": "abir"
    },
    "created_at": "2025-04-19T11:37:37.212150Z",
    "status": "pending",
    "items": [
        {
            "id": 6,
            "product": 8,
            "product_name": "Product-5Jmzpj",
            "quantity": 5,
            "price_at_order": "1946.00",
            "total_price": 9730.0
        },
        {
            "id": 7,
            "product": 9,
            "product_name": "Product-vZYXhj",
            "quantity": 2,
            "price_at_order": "270.00",
            "total_price": 540.0
        }
    ]
}
```
#### 🔴 Response 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```


### 📌 Update Order Status
- **URL:** `/api/v1/orders/<int:id>/`
- **Method:** `PATCH`
- **Access:** Private (Customer can update to "canceled", Admin/Vendor can update to other statuses)
### Explanation:
- The customer can only update the order status to "canceled" by sending the status in the request body.
- Admins or vendors can update the order status to other valid values (e.g., "delivered", "processing").

#### ✅ Request Body (Customer - Cancelling the Order)
```json
{
  "status": "canceled"
}
```

#### ✅ Request Body (Admin/Vendor - Updating to other status)
```sh
{
  "status": "delivered"
}
```

#### 🟢 Response 200 OK (Customer Cancels the Order)
```sh
{
  "message": "Order successfully canceled."
}
```
#### 🔴 Response 403 Forbidden (Unauthorized to change status)
```sh
{
  "error": "You do not have permission to update this order."
}
```


### ❌ Delete Order

- **URL:** `/api/v1/orders/<int:id>/`
- **Method:** `DELETE`
- **Access:** Private (Admin and Vendor Owner only)

#### 🟢 Response 204 No Content
```json
{}
```

#### 🔴 Response 403 Forbidden
```json
{
  "error": "You do not have permission to delete this order."
}
```

#### 🔴 Response 404 Not Found
```jso
{
    "error": "Order not found."
}
```

