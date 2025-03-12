# 🔍 String Deleter

### A GUI tool for modifying memory strings in running processes using `pymem` and `customtkinter`.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-UI-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🖥️ **Modern GUI** built with `customtkinter`
- 🎨 **Customizable Accent Colors** with real-time updates
- 🌙 **Light/Dark Mode Toggle**
- 🔍 **Modify Memory Strings** of running processes
- 🚀 **Multi-threaded execution** to prevent UI freezing
- 🔔 **System Notifications** on success/failure
- 🔧 **Error handling with message popups**

---

## 📦 Installation

1. **Clone the repository:**
   ```sh
   pip install -r requirements.txt
   py  main.py
   ```

   
## 🔧 Requirements

- Python 3.8+
- Windows OS (pymem is Windows-specific)
- Required Python modules:
- customtkinter
- tkinter
- pymem
- requests
- plyer
- CTkMessagebox

## 🚀 Usage

1. Enter the process name (e.g., example.exe).
2. Specify the memory address (Hex format, e.g., 0x123ABC).
3. Enter the string length to overwrite.
4. Click "Remove String" to replace it with dots (.....).
4. Check notifications & logs for results.

## 🔹 Use with caution! Incorrect memory modifications can crash applications.

### Please dont sue me if you dont know what you do :3

## ⚠️ Disclaimer

This tool is intended for educational and research purposes only.
Modifying memory of running processes can be risky. The author is not responsible for any misuse.



## 📜 License
This project is licensed under the MIT License.
