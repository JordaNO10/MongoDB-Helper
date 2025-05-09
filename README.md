# MongoDB JSON Importer (Executable App) 🧩

A lightweight, intuitive desktop application for importing, overwriting, and deleting JSON collections in MongoDB — all through a graphical interface.  
No command-line work required. Just open the `.exe` and go.

---

## 💡 What This App Does

- 📥 **Import** a `.json` file into a MongoDB collection  
- 🔁 **Overwrite** existing collections with new data  
- 🗑️ **Delete** unwanted collections from your database  
- ✅ Automatically checks for valid JSON and existing names  
- 🖱️ Fully GUI-based — simple and user-friendly  

---

## 🛠 Requirements

- ✅ **MongoDB** installed and running locally (`localhost:27017`)
- ✅ Windows OS (for `.exe` file)
- ❌ No need to install Python or any libraries

---

## 🚀 How to Use

1. **Open the `.exe` file** (double-click it).
2. Choose one of the main actions:
   - **Create/Overwrite Collection**  
     → Select a database, choose or create a collection, then pick a `.json` file to import
   - **Delete Collection**  
     → Select the database and collection you want to remove
   - **Exit**
3. Follow the on-screen prompts — all actions include confirmations.

---

## 📄 JSON File Format

Please use files that contain an **array of objects**:

✅ Correct:
```json
[
  { "name": "Alice", "age": 30 },
  { "name": "Bob", "age": 25 }
]

👨‍💻 Created By
Yarden Halely
🛠 Version: 2.0
📍 Made with Python, Tkinter & MongoDB
