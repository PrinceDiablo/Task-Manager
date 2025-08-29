# Task-Manager
A Python Command-Line Interface (CLI) Task Manager. Supports adding, editing, prioritizing, and tracking tasks directly from the terminal.

Task_Manager_Project/
│
├── taskmanager/         
│   ├── task.py            
│   ├── __init__.py         # (FileManager)
│   ├── fileio/
│       ├── csv_io.py
│       ├── json_io.py
│       ├── __init__.py     # (FileIO)
│
├── ui/
│   ├── gui/                # (for future GUI)
│   └── cli/
│       ├── input_task.py
│       ├── input_other.py
│       └── ...             # (other CLI helpers)
│
├── tests/                 
│   ├── __init__            # (blank)      
│   ├── test_task.py
│   ├── conftest.py
│   └── ...                 # (other unit/integration tests)
│
└── main.py                 # (entry point, connects everything)