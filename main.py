import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os

MAIN_FONT = "PT Serif"

class ProjectMatchingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student-Project Matching System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # self.root.update_idletasks()
        
        self.csv_file_path = tk.StringVar()
        self.csv_file_name = tk.StringVar()
        self.csv_data = None

        self.user_inputs = {} # Variables provided by professor to create groups

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
        self.configure_and_generate_group(main_frame)

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

        note_label = tk.Label(parent, text="Note: Your CSV file should look like the table above", font=(MAIN_FONT, 9, "italic"), fg="gray")
        note_label.pack(anchor=tk.W)

    def create_upload_section(self, parent):
        # File upload section
        upload_frame = tk.Frame(parent, padx=15, pady=15)
        upload_frame.pack(fill=tk.X, pady=(20, 10))

        upload_button = tk.Button(upload_frame, text="Upload CSV File", command=self.upload_csv_file, bg="#f0f0f0", font=(MAIN_FONT, 10))
        upload_button.pack(anchor="w", pady=(0, 15))
        
        file_display_frame = tk.Frame(upload_frame)
        file_display_frame.pack(fill=tk.X)

        tk.Label(file_display_frame, text="Selected file:", font=(MAIN_FONT, 10)).pack(side=tk.LEFT, padx=(0, 5))

        self.file_entry = tk.Entry(file_display_frame, textvariable=self.csv_file_name, state='readonly', font=(MAIN_FONT, 10), width=60)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

    
    def upload_csv_file(self):
        """Opens a file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_file_path.set(file_path)
            filename = os.path.basename(file_path)
            self.csv_file_name.set(filename)

    def open_input_popup(self):
        if not self.csv_file_path.get():
            messagebox.showwarning("No File Selected", "Please upload a CSV file first.")
            return

        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Configure Matching Parameters")
        popup.geometry("600x650")
        popup.resizable(True, True)
        popup.grab_set()  # Make popup modal

        # Center the popup
        popup.transient(self.root)
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Create a canvas and scrollbar
        canvas = tk.Canvas(popup)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((popup.winfo_width() // 2, 20), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Title
        title = tk.Label(scrollable_frame, text="Matching Parameters", font=(MAIN_FONT, 14, "bold"))
        title.pack(pady=(0, 20))

        # Instructions
        instructions = tk.Label(
            scrollable_frame, 
            text="Please configure the parameters for the matching algorithm",
            font=(MAIN_FONT, 10),
            wraplength=450,
            justify=tk.LEFT
        )
        instructions.pack(pady=(0, 15), anchor=tk.W)
        
        # Input fields frame
        inputs_frame = tk.Frame(scrollable_frame)
        inputs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dictionary to store entry widgets
        self.input_entries = {}
        
        # Define input fields
        input_fields = [
            {
                "label": "Maximum Students per Project:",
                "key": "capacity",
                "type": "int",
                "default": "5",
                "tooltip": "Maximum number of students that can be assigned to one project"
            },
            {
                "label": "Exceptions for Maximum Students per Project:",
                "key": "capacity_exceptions",
                "type": "list",
                "item": {
                    "group": {"type": "string", "label": "Project/Group"},
                    "capacity": {"type": "int", "label": "Max Students"}
                },
                "tooltip": "Customize maximum number of students for specific projects (e.g. ProjectA : 2)"
            },
            {
                "label": "Preference Range:",
                "key": "preference_range",
                "type": "range",
                "item": {
                    "min": {"type": "int", "label": "Minimum Preferences", "default": 1},
                    "max": {"type": "int", "label": "Maximum Preferences", "default": 16}
                },
                "tooltip": "Minimum and maximum preference range of students to be matched to. The smallest value of max can be set to the highest minimum rank found among all projects."
            },
            {
                "label": "Preassigned Students:",
                "key": "preassigned_students",
                "type": "list",
                "item": {
                    "student_id": {"type": "string", "label": "Student ID"},
                    "group": {"type": "string", "label": "Preassigned Groups"}
                },
                "tooltip": "Preassign students to a particular group by Student ID (e.g. 12345678: ProjectA)"
            }
        ]

        # Create input fields
        row = 0
        for field in input_fields:
            # Label
            label = tk.Label(
                inputs_frame, 
                text=field["label"], 
                font=(MAIN_FONT, 10),
                anchor=tk.W
            )
            label.grid(row=row, column=0, sticky=tk.W, pady=(10, 5), padx=(0, 10))
            
            # Input widget
            if field["type"] == "bool":
                var = tk.BooleanVar(value=field["default"])
                checkbox = tk.Checkbutton(
                    inputs_frame,
                    variable=var,
                    font=(MAIN_FONT, 10)
                )
                checkbox.grid(row=row, column=1, sticky=tk.W, pady=(10, 5))
                self.user_inputs[field["key"]] = var
            elif field["type"] == "list":
                list_frame = tk.Frame(inputs_frame)
                list_frame.grid(row=row+1, column=0, sticky="we", pady=(0, 5), columnspan=2)

                self.user_inputs[field["key"]] = []

                def add_row(val1="", val2=""):
                    row_frame = tk.Frame(list_frame)
                    row_frame.pack(fill=tk.X, pady=2)

                    first_entry = tk.Entry(row_frame, width=20)
                    first_entry.insert(0, val1)
                    first_entry.pack(side=tk.LEFT, padx=(0,5))

                    tk.Label(row_frame, text=":", font=(MAIN_FONT, 10)).pack(side=tk.LEFT, padx=(0, 5))

                    second_entry = tk.Entry(row_frame, width=20)
                    second_entry.insert(0, val2)
                    second_entry.pack(side=tk.LEFT)

                    # store this row
                    self.user_inputs[field["key"]].append((first_entry, second_entry))

                # Button to add more rows
                add_button = tk.Button(list_frame, text="+", command=lambda: add_row("", ""))
                add_button.pack(anchor = "w")
            
                add_row("","")
               
            elif field["type"] == "range":
                range_frame = tk.Frame(inputs_frame)
                range_frame.grid(row=row+1, column=0, sticky=tk.W+tk.E, pady=(0, 5), columnspan=2)
                
                tk.Label(range_frame, text="Min:", font=(MAIN_FONT, 9)).pack(side=tk.LEFT, padx=(0, 5))
                min_entry = tk.Entry(range_frame, font=(MAIN_FONT, 10), width=8)
                min_entry.insert(0, "1")
                min_entry.pack(side=tk.LEFT, padx=(0, 15))
                
                tk.Label(range_frame, text="Max:", font=(MAIN_FONT, 9)).pack(side=tk.LEFT, padx=(0, 5))
                max_entry = tk.Entry(range_frame, font=(MAIN_FONT, 10), width=8)
                max_entry.insert(0, "5")
                max_entry.pack(side=tk.LEFT)
                
                self.user_inputs[field["key"]] = {"min": min_entry, "max": max_entry}

            else:
                entry = tk.Entry(inputs_frame, font=(MAIN_FONT, 10), width=20)
                entry.insert(0, field["default"])
                entry.grid(row=row, column=1, sticky=tk.W+tk.E, pady=(10, 5))
                self.user_inputs[field["key"]] = entry

            row += 1 
            
            # Tooltip
            tooltip_label = tk.Label(
                inputs_frame,
                text=field["tooltip"],
                font=("Arial", 8, "italic"),
                fg="gray",
                wraplength=400,
                justify=tk.LEFT
            )
            tooltip_label.grid(row=row+1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
            
            row += 2
        
        inputs_frame.columnconfigure(1, weight=1)
        
        button_frame = tk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy,
            bg="#f44336",
            fg="white",
            font=(MAIN_FONT, 10),
            padx=20,
            pady=5
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # # Run button
        # run_btn = tk.Button(
        #     button_frame,
        #     text="Run Matching",
        #     command=lambda: self.collect_inputs_and_run(popup),
        #     bg="#4CAF50",
        #     fg="white",
        #     font=(MAIN_FONT, 10, "bold"),
        #     padx=20,
        #     pady=5
        # )
        # run_btn.pack(side=tk.LEFT)


    def configure_and_generate_group(self, parent):
        """Button to configure variables and generate groups"""
        button_frame = tk.Frame(parent, pady=20)
        button_frame.pack(fill=tk.X)
        run_btn = tk.Button(
            button_frame, 
            text="Configure & Generate Groups", 
            command=self.open_input_popup,
            bg="#4CAF50",
            fg="black",
            font=(MAIN_FONT, 12, "bold"),
            padx=30,
            pady=10,
            cursor="hand2"
        )
        run_btn.pack()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectMatchingGUI(root)
    root.mainloop()


    # TODO: create another button to validate csv file before matching (?) 
    # TODO: do we want to ask user about how many max students per projects, 
    # or project exceptions with capacity, what student's information are included, 
    # projects to exclude from matching, preassigned students?
    # TODO: create a button to run the matching algorithm in scripts/script.py
    # which saves the file to their downloads
