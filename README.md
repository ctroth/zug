# 🗂️ Zug File Organizer

Zug File Organizer is a powerful command-line tool built with Python that helps you clean up and organize your **Downloads** folder automatically or manually. It uses `Rich` for a colorful CLI interface and `Watchdog` to monitor changes in real time.

---

## 📦 Features

✅ Organize files by type into folders (Images, Documents, etc.)  
🧹 Automatically clean your Downloads folder with background automation  
📁 List all files and subdirectories  
🔍 Filter files by type  
🔄 Move files and change directories  
🗑️ Delete specific files or groups of files by extension  
📂 Create or remove subdirectories  
🎛️ Interactive, menu-driven CLI with colored output and ASCII art banners

---

## 📁 Folder Structure

```
zug_file_organizer/
│
├── main.py             # Main script with all functions and CLI logic
├── requirements.txt    # Required Python packages
└── README.md           # You're here!
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- A terminal (Windows PowerShell, Git Bash, etc.)

### 📥 Installation

```bash
git clone https://github.com/yourusername/zug_file_organizer.git
cd zug_file_organizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🧠 How It Works

When launched, the program:

1. Greets the user with an ASCII banner using `pyfiglet`.
2. Prompts for your **Windows username** and verifies it exists.
3. Switches to your Downloads folder:  
   `C:/Users/<your_username>/Downloads`
4. Presents an interactive menu to:
   - List files or directories
   - Organize files by type
   - Delete or move files
   - Enable background automation with Watchdog

Automation mode watches the Downloads folder and automatically moves new files to appropriate subfolders (e.g., `.pdf` to `Documents`, `.jpg` to `Images`).

---

## 🕹️ Commands & Options

| Option | Action                            |
|--------|-----------------------------------|
|   1    | View all files                    |
|   2    | List all subdirectories           |
|   3    | List files by type                |
|   4    | Change directory                  |
|   5    | Organize files by type            |
|   6    | Delete files by type              |
|   7    | Delete a specific file            |
|   8    | Delete a subdirectory             |
|   9    | Move a specific file              |
|  10    | Exit program                      |
|  11    | Enable Downloads folder automation|

---

## ⚙️ Automation Mode

Once enabled:

- Watches your Downloads folder
- Organizes new files based on type
- Can be stopped with `CTRL + C`

---

## 🧪 Developer Notes

Current work, ideas and future improvements:

- 🔍 Adding logging for every file operation  
- 🎨 Reducing overuse of red-colored output  
- 🛠️ Debugging all functions
- 🗃️ Tracking actions in a log file (`zug_file_organizer.log`)

---

## 💬 Example Terminal Output

```
Welcome to Zug File Organizer
Monitoring the Downloads folder for changes...
New file found in Downloads folder: cool_image.jpg
File appears to have finished downloading: cool_image.jpg
Moved cool_image.jpg to Images
```

---

## ✅ Tested File Types

- `.jpg`, `.png`, `.gif` → Images  
- `.docx`, `.pdf`, `.txt` → Documents  
- `.exe`, `.msi` → Executables  
- `.zip`, `.tar` → Zip_Files  
- `.mp3`, `.mp4` → Audio  
- `.torrent`, `.iso`, `.xlsx`, `.ini`, `.py`... and more!

---

## 🧹 Sample Folder Creation

Upon organizing, the following folders will be created if needed:

```
Images/
Documents/
Executables/
Zip_Files/
XLSX_Files/
ISO_Files/
Audio/
Torrent/
Ini_Files/
Programming_Files/
Incomplete_Files/
```

---

## 🙏 Acknowledgements

Built using:

- [`rich`](https://github.com/Textualize/rich) for colorful CLI rendering  
- [`watchdog`](https://github.com/gorakhargosh/watchdog) for folder monitoring  
- [`pyfiglet`](https://github.com/pwaller/pyfiglet) for ASCII banners  

---

## 🧾 License

For educational and personal use. Attribution appreciated if reused or modified. 🙌