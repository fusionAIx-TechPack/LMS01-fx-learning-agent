# 🎓 Beginner's Setup & User Guide (Non-Technical Edition)

Welcome to the **FX Learning Studio**! This friendly guide explains what this app does, why it exists, and how to set it up on a new laptop from scratch in simple, everyday language.

---

## 🌟 1. What is this Application and Why Does It Exist?

### The Purpose
Normally, creating an online course inside **Moodle** (the learning software used by schools, universities, and companies worldwide) takes **10 to 20 hours of manual work**. An instructor has to:
1. Research articles and topics.
2. Manually write course summaries and learning goals.
3. Structure chapters, lessons, and reading materials.
4. Write quizzes and assessments.
5. Manually configure Moodle settings.

### What This Tool Does For You
With this tool, you just **copy and paste any website link** (such as a tutorial, blog post, or article):
- 🤖 **AI reads the website** in seconds.
- 📚 **AI designs the curriculum**: It creates chapters, outlines, learning objectives, and practice quizzes.
- 📦 **1-Click Download**: It packs everything into an official Moodle course backup file (`.mbz`).
- 🚀 **Instant Import**: You upload that `.mbz` file directly into Moodle, and your complete course appears instantly!

---

## 💡 2. Why Use "Local Models" on Your Laptop?

- **100% Free**: No monthly subscriptions ($20/month for ChatGPT Plus or Claude is NOT needed).
- **100% Private**: Your data and course materials never leave your laptop.
- **Works Offline**: Once installed, you can generate courses even on an airplane or without internet.

---

## 💻 3. What to Download on Your Friend's Laptop (3 Steps)

You only need **two free programs** installed on Windows:

### Step 1: Install Python (The Engine Runner)
1. Go to: **[https://www.python.org/downloads/](https://www.python.org/downloads/)**
2. Click the big yellow button: **"Download Python"**.
3. Run the installer.
4. ⚠️ **VERY IMPORTANT**: On the first screen of the installer, check the box at the bottom that says:  
   👉 **`[x] Add python.exe to PATH`**  
   *(If you don't check this box, your laptop won't know where Python is).*
5. Click **"Install Now"** and wait for it to finish.

---

### Step 2: Install Ollama (The Free AI Engine)
1. Go to: **[https://ollama.com/download](https://ollama.com/download)**
2. Click **"Download for Windows"**.
3. Run the installer. It will install automatically and place a cute 🦙 (Llama icon) in your taskbar near the clock.
4. **Good news**: Ollama automatically starts in the background every time Windows turns on! You never need to start it manually.

---

### Step 3: Download a Free AI Model (Just Once)
Open your laptop's **Command Prompt** or **PowerShell** (press `Windows Key`, type `cmd`, and press Enter).

Choose the model that fits your friend's laptop:

- **For everyday laptops (8 GB to 16 GB RAM)** — *Fast & Lightweight*:
  ```powershell
  ollama run llama3.2
  ```
  *(Downloads in 2 minutes, takes only ~2 GB of space).*

- **For powerful laptops (16 GB to 32 GB RAM)** — *Highest Quality*:
  ```powershell
  ollama run llama3.1
  ```

Once you see the prompt say `>>> Send a message`, type `/bye` and press Enter. **That's it! The model is saved on your computer forever.**

---

## 🚀 4. How to Run the App (The 1-Click Method)

1. Put the **`LMS01-fx-learning-agent`** folder on your friend's laptop (e.g. on Desktop or `C:\`).
2. Open the folder.
3. **Double-click `start.bat`**.

That's literally all! 
- It will automatically install any required packages.
- It will automatically launch your web browser to: **`http://localhost:8088/`**.

---

## 📱 5. How to Use the App (Step-by-Step)

### Step 1: Paste Any Web Link
1. Open the app in your browser at `http://localhost:8088/`.
2. Find any educational article on the web (e.g., Python tutorial, Wikipedia topic, business guide).
3. Paste the URL into the **Source Learning URL** box.

### Step 2: Click "Analyze & Generate Course Proposal"
- The studio will connect to your local AI model.
- You'll see an animated progress monitor reading the web page and synthesizing course modules.
- *(Bonus: You can test connection and see the cartoon mascot check your models by clicking "Model Settings" in the top bar!)*

### Step 3: Review the Course Blueprint
- Once the AI finishes, you are taken to the **Review Gate**.
- Here you can see:
  - Course Title & Category.
  - Estimated hours to complete.
  - Learning objectives (Bloom's taxonomy).
  - Course outline and topics.
- You can edit any title or text if you want to make changes!

### Step 4: Download Your Moodle Package
- Click **"Build Moodle Course Package"**.
- Click **"Download .mbz"**.
- You now have an official Moodle course backup file on your computer!

---

## 🏫 6. How to Import the File into Moodle

1. Log in to your **Moodle site** as an Instructor or Admin.
2. Go to **Site Administration** $\rightarrow$ **Courses** $\rightarrow$ **Restore Course** (or go into any course and click **Course Management $\rightarrow$ Restore**).
3. Drag and drop your downloaded `.mbz` file into the box.
4. Click **Restore**, follow the 3 next buttons, and click **Perform Restore**.
5. **Done!** Your entire course, lessons, descriptions, and quizzes are now live in Moodle!

---

## ❓ Frequently Asked Questions

### Q: Do I have to pay anything?
**A:** No. Zero dollars. Running local models through Ollama is completely free and requires no credit cards or accounts.

### Q: Does it use my laptop's internet to think?
**A:** No. Once the model is downloaded, the AI runs entirely on your laptop's processor and memory. Internet is only used to scrape the webpage link you provide.

### Q: How do I stop it when I'm done?
**A:** Simply close the black Command Prompt window that opened when you clicked `start.bat`. To free up laptop memory from the AI model, open Command Prompt and type:
```powershell
ollama stop llama3.2
```
*(Or it will automatically unload by itself after 5 minutes of inactivity).*

### Q: Can I use ChatGPT or Claude instead if I prefer?
**A:** Yes! Click the **"Settings"** icon in the top right of the Web Studio, switch to **"Personal Cloud Accounts"**, paste your API key, and it will use cloud models with zero memory usage on your laptop.
