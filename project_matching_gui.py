import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path

MAIN_FONT = "PT Serif"
HEADER_FONT_SIZE = 18
SUBHEADER_FONT_SIZE = 15
REGULAR_FONT_SIZE = 12
BUTTON_BACKGROUND_COLOR = '#f0f0f0'
BUTTON_TEXT_COLOR = 'black'

class ProjectMatchingGUI:
    def __init__(self, root, callback=None):
        self.root = root
        self.callback = callback
        self.root.title("Student-Project Matching System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.csv_file_path = tk.StringVar()
        self.csv_file_name = tk.StringVar()
        self.csv_data = None

        self.output_folder_path = tk.StringVar()

        self.user_inputs = {}
        self.folder_name = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="Welcome to Student-Project Matching System!", font=(MAIN_FONT, HEADER_FONT_SIZE, "bold"))
        title_label.pack(pady=(0, 20))

        subtitle_label = tk.Label(main_frame, text="Before you start, please read the README.txt file in the directory.", font=(MAIN_FONT, SUBHEADER_FONT_SIZE, "bold"), padx=10, pady=10,justify="left")
        subtitle_label.pack(pady=(0, 20))
        
        self.create_upload_section(main_frame)
        self.configure_and_generate_group(main_frame)

    def create_upload_section(self, parent):
        upload_frame = tk.Frame(parent, padx=15, pady=15)
        upload_frame.pack(fill=tk.X, pady=(20, 10))

        upload_button = tk.Button(upload_frame, text="Upload CSV File", command=self.upload_csv_file, bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_TEXT_COLOR, font=(MAIN_FONT, REGULAR_FONT_SIZE))
        upload_button.pack(anchor="w", pady=(0, 15))
        
        file_display_frame = tk.Frame(upload_frame)
        file_display_frame.pack(fill=tk.X)

        tk.Label(file_display_frame, text="Selected file:", font=(MAIN_FONT, REGULAR_FONT_SIZE)).pack(side=tk.LEFT, padx=(0, 5))

        self.file_entry = tk.Entry(file_display_frame, textvariable=self.csv_file_name, state='readonly', font=(MAIN_FONT, REGULAR_FONT_SIZE), width=60)
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

        popup = tk.Toplevel(self.root)
        popup.title("Configure Matching Parameters")
        popup.geometry("800x750")
        popup.resizable(True, True)
        popup.grab_set()  
        popup.transient(self.root)

        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2 )- (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)

        popup.geometry(f"+{x}+{y}")
        
        canvas = tk.Canvas(popup)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((popup.winfo_width() // 2, 20), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        title = tk.Label(scrollable_frame, text="Matching Parameters", font=(MAIN_FONT, HEADER_FONT_SIZE, "bold"))
        title.pack(pady=(0, 20), anchor="center")

        instructions = tk.Label(
            scrollable_frame, 
            text="Please configure the parameters for the matching algorithm",
            font=(MAIN_FONT, SUBHEADER_FONT_SIZE),
            wraplength=650,
            justify=tk.CENTER
        )
        instructions.pack(pady=(0, 15), anchor=tk.W)
        
        inputs_frame = tk.Frame(scrollable_frame)
        inputs_frame.pack(fill=tk.BOTH, expand=True)
        
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
                "key": "student_group_inclusions",
                "type": "list",
                "item": {
                    "student": {"type": "string", "label": "Student ID"},
                    "projects": {"type": "string", "label": "Preassigned Groups"}
                },
                "tooltip": "Specify projects that the student can only be matched to by Student ID (e.g. 12345678: ProjectA, ProjectB)"
            },
            {
                "label": "Prohibited Projects:",
                "key": "student_group_exclusions",
                "type": "list",
                "item": {
                    "student": {"type": "string", "label": "Student ID"},
                    "projects": {"type": "string", "label": "Excluded Projects"}
                },
                "tooltip": "Specify projects that the student must not be assigned to by Student ID (e.g. 12345678: ProjectA, ProjectB)"
            },
        ]

        row = 0
        for field in input_fields:
            label = tk.Label(
                inputs_frame, 
                text=field["label"], 
                font=(MAIN_FONT, REGULAR_FONT_SIZE),
                anchor=tk.W
            )
            label.grid(row=row, column=0, sticky=tk.W, pady=(10, 5), padx=(0, 10))
            
            if field["type"] == "bool":
                var = tk.BooleanVar(value=field["default"])
                checkbox = tk.Checkbutton(
                    inputs_frame,
                    variable=var,
                    font=(MAIN_FONT, REGULAR_FONT_SIZE)
                )
                checkbox.grid(row=row, column=1, sticky=tk.W, pady=(10, 5))
                self.user_inputs[field["key"]] = var
            elif field["type"] == "list":
                list_frame = tk.Frame(inputs_frame)
                list_frame.grid(row=row+1, column=0, sticky="we", pady=(0, 5), columnspan=2)

                self.user_inputs[field["key"]] = []

                def add_row(val1="", val2="", lf = list_frame, key=field["key"]):
                    row_frame = tk.Frame(lf)
                    row_frame.pack(fill=tk.X, pady=2)

                    first_entry = tk.Entry(row_frame, width=20)
                    first_entry.insert(0, val1)
                    first_entry.pack(side=tk.LEFT, padx=(0,5))

                    tk.Label(row_frame, text=":", font=(MAIN_FONT, REGULAR_FONT_SIZE)).pack(side=tk.LEFT, padx=(0, 5))

                    second_entry = tk.Entry(row_frame, width=20)
                    second_entry.insert(0, val2)
                    second_entry.pack(side=tk.LEFT)

                    self.user_inputs[key].append((first_entry, second_entry))

                def remove_row(key=field["key"]):
                       if self.user_inputs[key]:
                            first_entry, second_entry = self.user_inputs[key].pop()
                            first_entry.master.destroy()

                button_frame = tk.Frame(list_frame)
                button_frame.pack(anchor="w", pady=2) 

                add_button = tk.Button(button_frame, text="+", bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_TEXT_COLOR, command=lambda f=add_row: f("", ""))
                add_button.pack(side=tk.LEFT, padx=(0, 5))

                remove_button = tk.Button(button_frame, text="-", bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_TEXT_COLOR, command=remove_row)
                remove_button.pack(side=tk.LEFT)
            
               
            elif field["type"] == "range":
                range_frame = tk.Frame(inputs_frame)
                range_frame.grid(row=row+1, column=0, sticky=tk.W+tk.E, pady=(0, 5), columnspan=2)
                
                tk.Label(range_frame, text="Min:", font=(MAIN_FONT, REGULAR_FONT_SIZE)).pack(side=tk.LEFT, padx=(0, 5))
                min_entry = tk.Entry(range_frame, font=(MAIN_FONT, REGULAR_FONT_SIZE), width=8)
                min_entry.insert(0, field["item"]["min"]["default"])
                min_entry.pack(side=tk.LEFT, padx=(0, 15))
                
                tk.Label(range_frame, text="Max:", font=(MAIN_FONT, REGULAR_FONT_SIZE)).pack(side=tk.LEFT, padx=(0, 5))
                max_entry = tk.Entry(range_frame, font=(MAIN_FONT, REGULAR_FONT_SIZE), width=8)
                max_entry.insert(0, field["item"]["max"]["default"])
                max_entry.pack(side=tk.LEFT)
                
                self.user_inputs[field["key"]] = {"min": min_entry, "max": max_entry}

            else:
                entry = tk.Entry(inputs_frame, font=(MAIN_FONT, REGULAR_FONT_SIZE), width=8)
                entry.insert(0, field["default"])
                entry.grid(row=row, column=1, pady=(10, 5))
                self.user_inputs[field["key"]] = entry

            row += 1 
            
            tooltip_label = tk.Label(
                inputs_frame,
                text=field["tooltip"],
                font=("Arial", 11, "italic"),
                fg="gray",
                wraplength=650,
                justify=tk.LEFT
            )
            tooltip_label.grid(row=row+1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
            
            row += 2

        folder_path_btn = tk.Button(
            scrollable_frame,
            text="Choose a directory to save the generated CSV file",
            command=self.select_folder_path,
            bg=BUTTON_BACKGROUND_COLOR, 
            fg=BUTTON_TEXT_COLOR,
            font=(MAIN_FONT, REGULAR_FONT_SIZE),
            padx=20,
            pady=5
        )
        folder_path_btn.pack(anchor="w", pady=(20, 0))

        folder_path_display_frame = tk.Frame(scrollable_frame)
        folder_path_display_frame.pack(fill = tk.X)

        tk.Label(folder_path_display_frame, text="Selected Directory:", font=(MAIN_FONT, REGULAR_FONT_SIZE)).pack(side=tk.LEFT, padx=(0, 5))

        self.folder_entry = tk.Entry(folder_path_display_frame, textvariable=self.output_folder_path, state='readonly', font=(MAIN_FONT, REGULAR_FONT_SIZE), width=60)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        row_frame = tk.Frame(scrollable_frame)
        row_frame.pack(fill=tk.X, pady = (5,10))

        label = tk.Label(row_frame, text = "Save as (folder name):", font=(MAIN_FONT, REGULAR_FONT_SIZE))
        label.pack(side=tk.LEFT, padx=(0, 5))

        self.folder_name = tk.Entry(row_frame, font=(MAIN_FONT, REGULAR_FONT_SIZE), width=8)
        self.folder_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        button_frame = tk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy,
            bg=BUTTON_BACKGROUND_COLOR, 
            fg=BUTTON_TEXT_COLOR,
            font=(MAIN_FONT, REGULAR_FONT_SIZE),
            padx=20,
            pady=5
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_btn = tk.Button(
            button_frame,
            text="Generate Groups",
            command=lambda: self.collect_inputs_and_run(popup),
            bg=BUTTON_BACKGROUND_COLOR, 
            fg=BUTTON_TEXT_COLOR,
            font=(MAIN_FONT, REGULAR_FONT_SIZE, "bold"),
            padx=20,
            pady=5
        )
        generate_btn.pack(side=tk.LEFT)

    def select_folder_path(self):
        folder = filedialog.askdirectory(
            title="Select folder to save CSV files",
            initialdir=Path.home() / "Downloads"
        )
        if folder:
            self.output_folder_path.set(folder)

    def configure_and_generate_group(self, parent):
        """Button to configure variables and generate groups"""
        button_frame = tk.Frame(parent, pady=20)
        button_frame.pack(fill=tk.X)
        run_btn = tk.Button(
            button_frame, 
            text="Configure & Generate Groups", 
            command=self.open_input_popup,
            bg=BUTTON_BACKGROUND_COLOR, 
            fg=BUTTON_TEXT_COLOR,
            font=(MAIN_FONT, REGULAR_FONT_SIZE, "bold"),
            padx=30,
            pady=10,
            cursor="hand2"
        )
        run_btn.pack()

    def collect_inputs_and_run(self, popup = None):
        if not self.output_folder_path.get():
            messagebox.showwarning("No Directory Selected", "Please select a directory first.")
            return
        
        if not self.folder_name.get():
            messagebox.showwarning("No Folder Name entered", "Please enter a folder name before proceeding.")
            return
        
        collected_user_inputs = {}

        for key, widget in self.user_inputs.items():
            if isinstance(widget, tk.BooleanVar):
                collected_user_inputs[key] = widget.get()

            elif isinstance(widget, list):
                if widget and isinstance(widget[0], tuple) and len(widget[0]) == 2: # check if value in list is type (a,b):
                    results = {}
                    for a, b in widget:
                        v1, v2 = a.get().strip(), b.get().strip()
                        if v1 and v2:
                            results[v1] = v2
                    collected_user_inputs[key] = results
                elif widget:
                    collected_user_inputs[key] = [w.get() if hasattr(w, "get") else w for w in widget]
                else:
                    collected_user_inputs[key] = {}
                    
            elif isinstance(widget, dict): # only range for now
                collected_user_inputs[key] = {
                    "min": widget["min"].get(),
                    "max": widget["max"].get()
                }
            else:
                collected_user_inputs[key] = widget.get()

        collected_user_inputs['csv_file_path'] = self.csv_file_path.get()
        collected_user_inputs['csv_file_name'] = self.csv_file_name.get()
        collected_user_inputs['output_folder_path'] = self.output_folder_path.get()
        collected_user_inputs['output_folder_name'] = self.folder_name.get()

        if self.callback:
            self.callback(collected_user_inputs)

        popup.destroy()
