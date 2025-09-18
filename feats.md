# E-Commerce Project

1. Core features and User Stories

- Public users (no login required)
    + view paginated page list of available products
    + filter and search products by `category`, `price range`, or `name`
    + view detailed product pages with `descriptions`, `images`, and `stock status`
    + add products to a shopping cart
    + view and update their cart (change quatities, remove items)

- Registered users (logged in)
    + all abilities of public users
    + have a persistent cart that is saved between sessions
    + proceed through a checkout flow to `purchase` items 
    + view basic order history

- Admin users
    + full CRUD operations on products, categories
    + manage customer orders


2. API Endpoints Reference

- Authentication & User Management
    + ["accounts/register/", "POST", "Create new user acc", "No auth"]
    + ["accounts/login/", "POST", "User Authentication", "No auth"]
    + ["accounts/logout/", "POST", "Logout user", "auth required"]
    + ["accounts/profile/", "GET", "User profile page", "auth required"]
    + ["accounts/profile/", "PUT", "Update user profile", "auth required"]

- Product Catalogue 
    + ["featured-products/", "GET", "Homepage with featured products", "No auth"]
    + ["products/", "GET", "All products listing", "No auth"]
    + ["products/{product_id}/", "GET", "Individual product details", "No auth"]
    + ["products/?category={slug}/", "GET", "Products filtered by category", "No auth"]
    + ["products/?search={value}/", "GET", "Products matching search query", "No auth"]
    + ["categories/", "GET", "all categories listing", "No auth"]
    + ["categories/{slug}/", "GET", "Products in a specific category", "No auth"]

- Order History
    + ["accounts/orders/", "GET", "User's order history", "auth required"]
    + ["accounts/orders/{order_id}/", "GET", "Get specific order details", "auth required"]

- Shopping Cart (Frontend)
    + ["cart/", "GET", "View cart contents", "no auth(session managed)"]
    + ["cart/add/{product_id}", "POST", "Add item to cart", "no auth(session managed)"]
    + ["cart/remove/{item_id}", "DELETE", "View cart contents", "no auth(session managed)"]




    































