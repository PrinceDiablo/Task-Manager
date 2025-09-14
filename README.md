# **Task Manager**

**Task Manager** is a Python-based command-line application that helps users manage their tasks easily. It allows you to create, edit, delete, view, and generate reports about your tasks. The main goal of this project is to build a practical tool while learning clean coding practices and good software design.

 **Video Demo:** (https://youtu.be/Tl836Ww09-Q)

---

## **✨ Features**

- ✅ **Add tasks** with details like:
  - Title
  - Start and end dates
  - Priority
  - Status
  - Description
- ✅ **Edit or update tasks** anytime with valid inputs.
- ✅ **View tasks** in multiple ways:
  - All tasks
  - Overdue tasks
  - Tasks sorted by priority
  - Tasks sorted by remaining days
- ✅ **Generate reports** using **pandas** for better data visualization.
- ✅ **Save and load tasks** in **CSV or JSON** formats for data persistence.
- ✅ A **simple CLI interface** that is easy to use without a graphical interface.
- ✅ **Modular and extensible**, making it easier to add more features later.

---

## **📂 File Structure**

### 📂 `task_manager/`
This folder contains the core functionality.

- **`task.py`**  
  Defines the `Task` class, which represents each task. It handles all validations to ensure data is always correct.

- **`fileio/`**  
  Contains file input/output logic.
  - **`csv_io.py`** and **`json_io.py`** handle reading and writing tasks in CSV and JSON formats.
  - **`__init__.py`** manages file format registration.

- **`reports.py`**  
  Creates reports like overdue tasks, priority lists, and remaining days using **pandas**.

---

### 📂 `ui/cli/`
Helps validate and collect user input. It ensures that tasks are created correctly without the user filling out the entire form repeatedly if a mistake is made.

---

### 📂 `tests/`
Includes unit tests using **pytest** to make sure the project functions as expected. It tests features like task creation, validations, and report generation.

---

### 📄 `main.py`
The entry point of the application. It connects all components and manages interactions through the CLI.

---

## **🎨 Design Choices**

- **Modular Code**  
  Each functionality is separated into its own file. This improves readability, maintainability, and makes it easier to extend.

- **Validation within the Task class**  
  All validations are done in the `Task` class using setters and helper methods. This ensures tasks are always valid, no matter how they are created or updated.

- **Reports with pandas**  
  Using **pandas** makes data handling and sorting simple. It is powerful and flexible for future enhancements.

- **CSV and JSON support**  
  Supporting multiple file formats allows flexibility in saving and sharing task data.

- **Simple CLI interface**  
  The CLI is designed to be intuitive and easy for users who prefer terminal-based tools.

---

## **📖 Future Improvements**

- ➕ Add a graphical interface using **Tkinter** or a web-based interface.
- ➕ Allow recurring tasks and notifications.
- ➕ Visualize reports with charts and graphs.
- ➕ Support cloud storage or other file formats.

---

## **🎯 Conclusion**

This project not only solves a real-world problem but also serves as a learning experience. It helped me practice object-oriented programming, clean code, and error handling. The design ensures scalability and simplicity, while the reports provide useful insights into tasks. I’m excited to enhance it further.

---

## **🛠️ Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/PrinceDiablo/Task-Manager.git
   cd Task-Manager

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows


3. Install dependencies:

   ```bash
   pip install -r requirements.txt

---

## **🚀 Usage**

- Run the application with:

   ```bash
   python main.py
  

- Save/load formats: **`.csv`** and **`.json`**

---

## **🔎 Test**
Run tests:
```bash
pytest tests -v
