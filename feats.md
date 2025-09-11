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
