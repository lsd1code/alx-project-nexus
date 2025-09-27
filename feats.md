# E-Commerce Project

1. Core features and User Stories

- Public users (no login required)
    + view paginated page list of available products
    + filter and search products by `category`, or `name`
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
    + ["featured-products/", "GET", "Homepage with featured products", "No auth"] ✅
    + ["products/", "GET", "All products listing", "No auth"] ✅
    + ["products/{product_id}/", "GET", "Individual product details", "No auth"] ✅
    + ["products/?category={slug}/", "GET", "Products filtered by category", "No auth"] ✅
    + ["products/?search={value}/", "GET", "Products matching search query", "No auth"] ✅
    + ["categories/", "GET", "all categories listing", "No auth"] ✅
    + ["categories/{slug}/", "GET", "Products in a specific category", "No auth"] ✅

- Orders
    + ["orders/", "GET", "User's order history", "auth required"] ✅
    + ["orders/", "POST", "Create new user order", "auth required"] ✅
    + ["orders/{order_id}/", "GET", "Get specific order details", "auth required"] ✅
    + ["orders/{order_id}/", "DELETE", "Delete specific order", "auth required"] ✅

- Shopping Cart (Frontend)
    + ["cart/", "GET", "View cart contents", "no auth(session managed)"]
    + ["cart/add/{product_id}", "POST", "Add item to cart", "no auth(session managed)"]
    + ["cart/remove/{item_id}", "DELETE", "View cart contents", "no auth(session managed)"]

---

# Video Script

# 🎥 **5-Minute API Demo Video Script**

## **Video Title: "E-commerce REST API - Complete Backend Demo"**

---

### **0:00-0:25 - Introduction & Architecture**
**[Visual: Project architecture diagram]**

**Script:**
"Hi, I'm [Your Name], and this is my E-commerce REST API built with Django REST Framework. This is a complete backend system that handles user authentication, product management, shopping carts, and secure payments. Let me show you how it works."

---

### **0:25-1:15 - Authentication & User Endpoints**
**[Visual: Postman/Thunder Client - Authentication requests]**

**Script:**
"First, let's look at authentication. I'll register a new user and then log in to get an access token."

**Actions:**
1. `POST /api/auth/register/` 
   - Show: `{"username": "demo_user", "email": "demo@test.com", "password": "secure123"}`
   - Highlight: 201 Created response

2. `POST /api/auth/login/`
   - Show: `{"username": "demo_user", "password": "secure123"}`
   - Highlight: JWT tokens in response

**Script:**
"Now I have an access token that I'll use for authenticated requests. The token automatically expires for security."

---

### **1:15-2:15 - Product Catalog & Features**
**[Visual: Product endpoints demonstration]**

**Script:**
"Next, let's explore the product catalog. These are public endpoints that don't require authentication."

**Actions:**
1. `GET /api/products/` 
   - Show paginated response with 10+ products
   - Highlight: `count`, `next`, `results` structure

2. `GET /api/products/?category=electronics&search=laptop`
   - Demonstrate filtering and search
   - Show how query parameters work

3. `GET /api/products/1/`
   - Show detailed product information
   - Highlight: price, stock, description

**Script:**
"The API supports advanced filtering, search, and pagination - everything needed for a real e-commerce site."

---

### **2:15-3:00 - Shopping Cart Operations**
**[Visual: Cart management endpoints]**

**Script:**
"Now let's add items to the shopping cart. These endpoints require authentication."

**Actions:**
1. `POST /api/cart/items/`
   - Show: `{"product": 1, "quantity": 2}`
   - Demonstrate successful addition

2. `GET /api/cart/`
   - Show current cart with calculated totals
   - Highlight: `subtotal`, `tax`, `total` fields

3. `PUT /api/cart/items/1/` 
   - Update quantity: `{"quantity": 3}`
   - Show real-time total recalculation

**Script:**
"The cart automatically calculates totals and maintains user-specific data across sessions."

---

### **3:00-4:00 - Order Processing & Payments**
**[Visual: Order and payment flow]**

**Script:**
"Time to complete a purchase. I'll convert the cart to an order and process payment."

**Actions:**
1. `POST /api/orders/`
   - Create order from cart
   - Show order ID and status: `"pending_payment"`

2. `POST /api/payments/create-intent/`
   - Create Stripe PaymentIntent
   - Show client secret for frontend integration

3. **Switch to Django Admin**
   - Show the created order in database
   - Demonstrate order-user-product relationships

**Script:**
"The payment system uses Stripe for secure processing. Webhooks handle payment confirmation asynchronously."

---

### **4:00-4:30 - Admin Features & Data Management**
**[Visual: Django admin interface]**

**Script:**
"Let me show you the admin interface where you can manage all data."

**Actions:**
- Navigate through Users, Products, Orders
- Show real-time inventory management
- Demonstrate order status updates
- Show how data relationships work

**Script:**
"The admin panel provides complete control over products, users, and orders with proper permission levels."

---

### **4:30-4:50 - Security & Best Practices**
**[Visual: Code snippets and security highlights]**

**Script:**
"Key security features include JWT authentication, rate limiting, input validation, and CORS configuration."

**Quick Highlights:**
- Show permission classes in code
- Demonstrate error handling for invalid requests
- Mention Stripe webhook signature verification

---

### **4:50-5:00 - Conclusion**
**[Visual: API documentation page]**

**Script:**
"This API provides a complete e-commerce backend with proper documentation, security, and scalability. It's ready to power web, mobile, or third-party applications. Thank you for watching!"

---

## 🛠 **Pre-Recording Checklist**

### **Setup Required:**
```bash
# Have these ready before recording:
✅ Django development server running
✅ Postman/Thunder Client with pre-configured requests
✅ Test users created (demo_user, admin)
✅ Sample products in database
✅ Stripe test mode configured
✅ Django admin logged in (separate tab)
```

### **Test Data to Prepare:**
```python
# Users
demo_user (customer)
admin_user (staff)

# Products
- Laptop (Electronics, $999, stock: 10)
- Smartphone (Electronics, $699, stock: 25)
- T-shirt (Clothing, $29, stock: 100)
```

### **API Endpoints to Pre-load in Postman:**
```
GET    /api/products/
POST   /api/auth/register/
POST   /api/auth/login/
GET    /api/cart/
POST   /api/cart/items/
POST   /api/orders/
```

## 🎬 **Recording Tips for Perfect Timing**

**Pacing Guide:**
- **Introduction:** 25 seconds (keep it snappy)
- **Authentication:** 50 seconds (practice token flow)
- **Products:** 60 seconds (smooth transitions)
- **Cart:** 45 seconds (demonstrate calculations)
- **Orders/Payments:** 60 seconds (key highlight)
- **Admin/Security:** 30 seconds (quick but impactful)
- **Conclusion:** 10 seconds (clean ending)

**Pro Tips:**
- Pre-type API requests to avoid typos
- Use zoom effects to highlight important areas
- Keep browser dev tools open to show network requests
- Practice the token refresh timing
- Have error scenarios prepared (but don't show unless they happen naturally)

This script ensures you cover all critical API functionality while staying within the 5-minute limit. Practice the flow 2-3 times before recording to ensure smooth delivery!





---
# 🎥 **Screen Recording & Voice-Over Guide**

Here's a step-by-step process to record your screen first and add professional voice-over later:

## **Method 1: All-in-One Free Solution (OBS Studio)**

### **Step 1: Record Your Screen**
```bash
# Download OBS Studio (Free & Cross-Platform)
https://obsproject.com/

# Setup:
1. Install OBS Studio
2. Add "Display Capture" source for your screen
3. Add "Audio Input Capture" for system audio (optional)
4. **IMPORTANT: Mute your microphone** during recording
5. Record in MP4 format (Settings → Output → Recording)
```

### **Step 2: Add Voice-Over Later**
```bash
# Using OBS Studio's Studio Mode:
1. Open your recorded video as a "Media Source"
2. Add a new "Audio Input Capture" for your microphone
3. Use "Studio Mode" to preview before recording
4. Play the video and record your voice simultaneously
5. Export final video with synchronized audio
```

## **Method 2: Separate Recording & Editing (Recommended)**

### **Step 1: Record Screen Only**
**Option A: Quick & Simple (Built-in Tools)**
- **Windows:** `Win + Alt + R` (Xbox Game Bar)
- **Mac:** `Cmd + Shift + 5` (QuickTime Player)
- **Linux:** Use Kazam or SimpleScreenRecorder

**Option B: Professional Quality**
```bash
# Use OBS Studio for higher quality:
- Resolution: 1920x1080
- Frame rate: 30 fps
- Format: MP4
- Bitrate: 2500-4000 Kbps
```

### **Step 2: Record Voice-Over Separately**
```bash
# Tools for Voice Recording:
1. **Audacity** (Free, professional audio editor)
2. **Voice Memos** (Mac/iPhone)
3. **Windows Voice Recorder** (Windows)
4. **Online-voice-recorder.com** (Web-based)

# Recording Tips:
- Use a quiet room with minimal echo
- Speak close to the microphone (6-8 inches)
- Record in WAV format for best quality
- Keep a glass of water nearby
```

### **Step 3: Combine Video & Audio**
**Free Video Editors:**

**Option A: DaVinci Resolve (Professional Quality)**
```bash
# Steps:
1. Import your screen recording
2. Import your voice recording
3. Drag video to timeline
4. Drag audio to separate track
5. Sync voice with video actions
6. Export as MP4
```

**Option B: Shotcut (Simple & Free)**
```bash
# Simple workflow:
1. File → Open File (your screen recording)
2. Drag video to timeline
3. File → Open File (your voice recording)
4. Drag audio to timeline below video
5. Adjust audio levels if needed
6. Export → YouTube 1080p
```

**Option C: Online Editors (No Installation)**
- **Clipchamp** (Free with watermark)
- **Canva Video Editor** (Simple editing)
- **Kapwing** (Web-based)

## **🎤 Professional Voice-Over Recording Tips**

### **Script Preparation:**
```markdown
# Format your script for easy reading:
[0:00] - "Welcome to my API demo..."
[0:25] - "First, let's look at authentication..."
[1:15] - "Now, exploring product catalog..."

# Practice reading with timing marks
```

### **Recording Setup:**
```bash
# Improve Audio Quality:
1. Use headphones to prevent echo
2. Record in a closet or small room (reduces echo)
3. Put your phone on silent mode
4. Close windows to block outside noise
5. Use a pop filter or sock over microphone
```

### **Voice Recording Script:**
```python
# Sample recording process:
def record_voice_over():
    # 1. Watch your screen recording 2-3 times
    # 2. Mark timings for each section
    # 3. Record in small segments (easier to re-do)
    # 4. Leave 1-second gaps between segments
    # 5. Save each segment separately
```

## **📋 Step-by-Step Workflow**

### **Day 1: Screen Recording**
```bash
1. ✅ Prepare your demo environment
2. ✅ Practice the flow 2-3 times
3. ✅ Close unnecessary applications
4. ✅ Clean up your desktop background
5. ✅ Record screen (mute microphone)
6. ✅ Review recording for mistakes
```

### **Day 2: Voice Recording**
```bash
1. ✅ Watch screen recording and time each section
2. ✅ Write speaking script with timestamps
3. ✅ Set up quiet recording environment
4. ✅ Record voice in small segments
5. ✅ Listen back and re-record if needed
```

### **Day 3: Editing & Export**
```bash
1. ✅ Import screen recording to video editor
2. ✅ Import voice recordings to separate tracks
3. ✅ Sync audio with video actions
4. ✅ Add intro/outro screens if desired
5. ✅ Export final video (MP4, 1080p)
6. ✅ Upload to YouTube/Google Drive
```

## **⚡ Quick 30-Minute Method**

### **For a fast turnaround:**
```bash
# Using OBS Studio only:
1. Record screen with OBS (mute mic)
2. Open recorded video in VLC player
3. Use OBS "Studio Mode":
   - Source 1: Your video file
   - Source 2: Microphone
4. Play video and record voice simultaneously
5. Export final version
```

## **🎚️ Audio Quality Improvements**

### **Free Audio Enhancements:**
```bash
# In Audacity (post-processing):
1. Effects → Noise Reduction (capture noise profile first)
2. Effects → Compressor (even out volume)
3. Effects → Equalization → Bass Boost (optional)
4. Effects → Normalize (set to -1.0 dB)
```

### **Quick Audio Fixes:**
```bash
# If voice is too quiet:
- Increase gain by 3-6 dB
- Use compression to reduce peaks

# If background noise:
- Use noise reduction gently (avoid robotic sound)
- Re-record in quieter environment if possible
```

## **📹 Sample Recording Setup**

### **Ideal Screen Layout:**
```
┌─────────────────────────────────────┐
│           POSTMAN WINDOW            │  ← Main focus (75% of screen)
│   Making API requests to your app   │
└─────────────────────────────────────┘
┌───────┐ ┌───────┐
│ BROWSER│ │ TERM  │                   ← Secondary windows
│ Admin │ │ Server│
└───────┘ └───────┘
```

### **Voice Recording Script Template:**
```markdown
[0:00-0:25]
"Hello, I'm [Name] and this is my E-commerce API demo. 
I built this using Django REST Framework to handle..."

[0:25-1:15]
"Let's start with authentication. I'm sending a POST request
to the registration endpoint with user data..."

[PAUSE - wait for API response to show on screen]

"As you can see, we get a 201 Created response..."
```

This approach gives you maximum control over quality and lets you re-record just the audio if you make mistakes, without having to redo the entire screen recording!

Would you like me to elaborate on any specific part of this process?    































