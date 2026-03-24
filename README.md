# 🎧 Dictation App (Docker)

Simple TOEIC dictation 

---

## 🚀 Quick Start (Beginner Friendly)

If you are new to Docker, just copy & run:

```bash
docker run -p 5001:5001 cuxuanthoai/dictation-app
```

Then open your browser:

👉 [http://localhost:5001](http://localhost:5001)

---

## 🧭 Common Options (Easy to Understand)

### 🔹 1. Run in background (recommended)

```bash
docker run -d -p 5001:5001 cuxuanthoai/dictation-app
```

👉 App runs in background (no terminal blocking)

---

### 🔹 2. Give your container a name

```bash
docker run -d -p 5001:5001 --name dictation-app cuxuanthoai/dictation-app
```

👉 easier to manage later

---

### 🔹 3. Stop the app

```bash
docker stop dictation-app
```

---

### 🔹 4. Start again (after stop)

```bash
docker start dictation-app
```

---

### 🔹 5. Remove container

```bash
docker rm dictation-app
```

---

### 🔹 6. Change port (if 5001 is busy)

```bash
docker run -p 8080:5001 cuxuanthoai/dictation-app
```

👉 access at: [http://localhost:8080](http://localhost:8080)

---


## 🌐 Access the App

Default:

👉 [http://localhost:5001](http://localhost:5001)

---

## 📦 Features

* 🎧 Audio-based dictation practice (TOEIC style)
* 🔁 Auto next / loop playback
* ✅ Instant answer checking
* 📊 Progress tracking

---

## ❗ Troubleshooting (Quick Fix)

### App not opening?

* Check Docker is running
* Try another port (8080)

### Port already in use?

```bash
docker run -p 8080:5001 cuxuanthoai/dictation-app
```

---
