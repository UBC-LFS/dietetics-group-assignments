import tkinter as tk
from tkinter import ttk

MAIN_FONT = "PT Serif"

class ProjectMatchingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student-Project Matching System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
    
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="Welcome to Student-Project Matching System!", font=(MAIN_FONT, 18, "bold"))
        title_label.pack(pady=(0, 20))

        subtitle_label = tk.Label(main_frame, text="Before you start, please read the CSV File Format Requirements.", font=(MAIN_FONT, 15, "bold"), padx=10, pady=10,justify="left")
        subtitle_label.pack(pady=(0, 20))
        
        format_frame = tk.LabelFrame(main_frame, text="CSV File Format Requirements", font=(MAIN_FONT, 12, "bold"), padx=20, pady=10)
        format_frame.pack(fill=tk.X, pady=(0, 20))
    
        self.create_instructions(format_frame)
        self.create_example_table(format_frame)
        self.create_upload_section(main_frame)

    def create_instructions(self, parent):
        instructions = """
            • Column headers must be in the first row
            • Required columns: student_id, student_first_name, student_last_name, project
            • No empty rows between data
        """
        instructions_label = tk.Label(parent, text=instructions, justify=tk.LEFT, font=(MAIN_FONT, 10))
        instructions_label.pack(anchor=tk.W)


    def create_example_table(self, parent):
        table_frame = tk.Frame(parent)
        table_frame.pack(fill=tk.X, pady=(0, 10))
        
        columns = ("Student ID", "First Name", "Last Name", "Project 1", "Project 2", "Project 3")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=4)

        column_widths = {
            "Student ID": 80,
            "First Name": 100,
            "Last Name": 100,
            "Project 1": 120,
            "Project 2": 120,
            "Project 3": 120
        }
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths[col], minwidth=60)
    
        example_data = [
            ("12345", "John", "Smith", "1", "2", "3"),
            ("12346", "Jane", "Doe", "3", "1", "2"),
            ("12347", "Bob", "Johnson", "2", "3", "1")
        ]
        
        for row in example_data:
            tree.insert('', tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True)

        note_label = tk.Label(parent, text="Note: Your CSV file should look like the table above", font=("Arial", 9, "italic"), fg="gray")
        note_label.pack(anchor=tk.W)

    def create_upload_section(self, parent):
        # File upload section
        upload_frame = tk.Label(parent, text="Upload Student Data", font=(MAIN_FONT, 12, "bold"), padx=15, pady=15)
        upload_frame.pack(fill=tk.X, pady=(20, 10))

        # File selection row
        file_row = tk.Frame(upload_frame)
        file_row.pack(fill=tk.X, pady=(0, 15))
        
        # File path display
        tk.Label(file_row, text="Selected file:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        
        file_display_frame = tk.Frame(file_row)
        file_display_frame.pack(fill=tk.X)
        
        



if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectMatchingGUI(root)
    root.mainloop()
