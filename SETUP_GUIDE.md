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

You only need **two free programs** (Windows or Mac):

### Step 1: Install Python (The Engine Runner)
* **On Windows**:
  1. Go to: **[https://www.python.org/downloads/](https://www.python.org/downloads/)**
  2. Click the big yellow button: **"Download Python"**.
  3. ⚠️ **VERY IMPORTANT**: On the first installer screen, check: **`[x] Add python.exe to PATH`**.
  4. Click **"Install Now"**.
* **On Mac**:
  * Download from **[https://www.python.org/downloads/](https://www.python.org/downloads/)** or install via Terminal:
    ```bash
    brew install python
    ```

---

### Step 2: Install Ollama (The Free AI Engine)
* **On Windows**:
  1. Go to: **[https://ollama.com/download/windows](https://ollama.com/download/windows)** (or `winget install Ollama.Ollama`).
  2. Run the installer. It places a 🦙 icon in your taskbar near the clock.
* **On Mac**:
  1. Go to: **[https://ollama.com/download/mac](https://ollama.com/download/mac)** (or `brew install ollama`).
  2. Drag Ollama to your Applications folder and launch it once.

---

### Step 3: Download a Free AI Model (Tailored for 16 GB RAM Laptops)

Open your laptop's **Command Prompt** or **PowerShell** (press `Windows Key`, type `cmd`, and press Enter).

> [!NOTE]
> **Standard Hardware Profile: 16 GB RAM Laptops**  
> On a 16 GB Windows laptop, the operating system and web browser typically use ~5 GB to 6 GB of RAM, leaving **~10 GB of free memory**.  
> The models below are specifically curated in the **3B to 8B parameter range** (using **~2.0 GB to 4.7 GB of RAM**). They run completely in memory with plenty of headroom, meaning your laptop will remain fast, responsive, and cool without freezing or disk swapping.

#### 🏆 Top Models for 16 GB Laptops (Ranked)

| Model | RAM Used | Speed | Best For | 1-Click Install Command |
| :--- | :--- | :--- | :--- | :--- |
| **🥇 Llama 3.1 (8B)** | **~4.7 GB** | ⚡ Fast (10-15s) | **Team Default (Recommended)** · Best overall curriculum taxonomy, syllabus depth & quiz generation | `ollama run llama3.1` |
| **🥈 Qwen 2.5 (7B)** | **~4.5 GB** | ⚡ Fast (8-12s) | **Best for Structured & Tech Courses** · Ranked #1 open model for JSON schema & module outlines | `ollama run qwen2.5:7b` |
| **🥉 Llama 3.2 (3B)** | **~2.0 GB** | ⚡⚡ Instant (3-5s) | **Battery-Saver & Speed** · Uses minimal memory, ideal when running on battery or multitasking heavily | `ollama run llama3.2` |
| **Phi 3.5 (3.8B)** | **~2.2 GB** | ⚡⚡ Instant (4-6s) | **Tutorials & Summaries** · Microsoft's compact reasoning model for clear lesson descriptions | `ollama run phi3.5` |
| **Mistral (7B)** | **~4.1 GB** | ⚡ Fast (10-14s) | **Concise Outlines** · Compact European open model, excellent at concise summaries | `ollama run mistral` |

---

#### 📊 Memory Breakdown on a 16 GB Laptop

Here is why 7B/8B models run safely on your 16 GB laptop:

```text
Total Laptop Memory: 16.0 GB
├── Windows 10/11 & Background Tasks: ~4.5 GB
├── Browser (Edge/Chrome) & FX Studio:  ~1.5 GB
├── AI Model (e.g. Llama 3.1 8B):       ~4.7 GB
└── FREE SAFETY BUFFER REMAINING:      ~5.3 GB  <-- Laptop stays smooth and responsive!
```

---

#### ⚠️ Models to AVOID on 16 GB Laptops
- ❌ **Do NOT run 14B, 32B, or 70B models** (e.g., `qwen2.5:14b`, `llama3.1:70b`, `command-r`).
- These models require 10 GB to 45 GB of RAM. On a 16 GB machine, Windows will run out of physical memory and freeze or heavily page to your SSD.
- **Stick to the 3B to 8B models listed above** for optimal speed and reliability.

---

#### 🚀 Recommended Action for the Team (Run This Once):
Run the default model for the team:
```powershell
ollama run llama3.1
```
*(Once Ollama downloads and prints `>>> Send a message`, type `/bye` and hit Enter. The model is now permanently saved on your computer).*

*(Optional)* If you also want the lightweight speed model for quick testing:
```powershell
ollama run llama3.2
```

#### 💡 How to Switch Models in FX Learning Studio:
1. Open the Web Studio in your browser at `http://localhost:8088/`.
2. Click the **"Settings"** icon or active model name in the top navigation bar.
3. In the **Local Model** dropdown, all models you have downloaded with `ollama run` will appear automatically. Select whichever you want to use!
4. To see which models are currently downloaded on your laptop:
   ```powershell
   ollama list
   ```

---

## 🚀 4. How to Run the App (The 1-Click Method)

1. Put the **`LMS01-fx-learning-agent`** folder on the laptop (e.g. on Desktop).
2. Open the folder.
3. Start the application:
   - **On Windows**: Double-click **`start.bat`**.
   - **On Mac / Linux**: Double-click **`start.sh`** (or open Terminal and run `./start.sh`).

That's literally all! 
- It will automatically verify Python and install any required dependencies.
- It will automatically launch your default web browser to: **`http://localhost:8088/`**.

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
