import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from seating_arrangement import SeatingArrangement

class SeatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Seating Arrangement")
        self.arrangement = SeatingArrangement()
        
        self.create_widgets()

    def create_widgets(self):
        self.students_label = tk.Label(self.root, text="Enter the list of students separated by commas:")
        self.students_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.students_entry = tk.Entry(self.root, width=50)
        self.students_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.rows_label = tk.Label(self.root, text="Enter the number of rows:")
        self.rows_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.rows_entry = tk.Entry(self.root, width=10)
        self.rows_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        self.cols_label = tk.Label(self.root, text="Enter the number of columns:")
        self.cols_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.cols_entry = tk.Entry(self.root, width=10)
        self.cols_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        self.submit_students_button = tk.Button(self.root, text="Submit Students", command=self.submit_students)
        self.submit_students_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.add_constraints_button = tk.Button(self.root, text="Add Constraints", command=self.add_constraints, state=tk.DISABLED)
        self.add_constraints_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.calculate_button = tk.Button(self.root, text="Calculate Seating", command=self.calculate_seating, state=tk.DISABLED)
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.result_text = tk.Text(self.root, width=60, height=10, wrap='word')
        self.result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.constraints_listbox = tk.Listbox(self.root, width=60, height=10)
        self.constraints_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.remove_constraint_button = tk.Button(self.root, text="Remove Selected Constraint", command=self.remove_constraint)
        self.remove_constraint_button.grid(row=8, column=0, columnspan=2, pady=10)

    def submit_students(self):
        self.arrangement.students = self.students_entry.get().split(',')
        self.arrangement.students = [student.strip() for student in self.arrangement.students]
        self.arrangement.rows = int(self.rows_entry.get())
        self.arrangement.cols = int(self.cols_entry.get())
        
        self.add_constraints_button.config(state=tk.NORMAL)
        self.calculate_button.config(state=tk.NORMAL)
        
        messagebox.showinfo("Success", "Students and classroom dimensions submitted successfully!")

    def add_constraints(self):
        if hasattr(self, 'constraints_window') and self.constraints_window.winfo_exists():
            return
        self.constraints_window = tk.Toplevel(self.root)
        self.constraints_window.title("Add Constraints")

        self.constraints_student = tk.StringVar()
        self.constraints_type = tk.StringVar()
        self.constraints_type.set("not_next_to")

        self.student_label = tk.Label(self.constraints_window, text="Select student:")
        self.student_label.grid(row=0, column=0, padx=10, pady=10)

        self.student_combobox = ttk.Combobox(self.constraints_window, values=self.arrangement.students, textvariable=self.constraints_student)
        self.student_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.constraint_type_label = tk.Label(self.constraints_window, text="Select constraint type:")
        self.constraint_type_label.grid(row=1, column=0, padx=10, pady=10)

        self.constraints_type_menu = tk.OptionMenu(self.constraints_window, self.constraints_type, "not_next_to", "next_to", "preferred_location")
        self.constraints_type_menu.grid(row=1, column=1, padx=10, pady=10)

        self.target_label = tk.Label(self.constraints_window, text="Select target:")
        self.target_label.grid(row=2, column=0, padx=10, pady=10)

        self.target_listbox = tk.Listbox(self.constraints_window, selectmode=tk.MULTIPLE, width=27)
        self.target_listbox.grid(row=2, column=1, padx=10, pady=10)

        self.student_combobox.bind("<<ComboboxSelected>>", self.update_target_listbox)
        self.constraints_type.trace("w", self.update_target_listbox)

        self.add_constraint_button = tk.Button(self.constraints_window, text="Add Constraint", command=self.save_constraint)
        self.add_constraint_button.grid(row=3, column=0, columnspan=2, pady=10)

    def update_target_listbox(self, *args):
        selected_student = self.constraints_student.get()
        constraint_type = self.constraints_type.get()
        
        self.target_listbox.delete(0, tk.END)
        if constraint_type in ["not_next_to", "next_to"]:
            available_students = [student for student in self.arrangement.students if student != selected_student]
            for student in available_students:
                self.target_listbox.insert(tk.END, student)
        elif constraint_type == "preferred_location":
            self.target_listbox.insert(tk.END, "row,col")
        
    def save_constraint(self):
        student = self.constraints_student.get().strip()
        selected_targets = [self.target_listbox.get(i) for i in self.target_listbox.curselection()]
        constraint_type = self.constraints_type.get()

        if constraint_type == "preferred_location":
            try:
                row, col = map(int, selected_targets[0].split(','))
                if row < 0 or row >= self.arrangement.rows or col < 0 or col >= self.arrangement.cols:
                    raise ValueError("Row or column out of range")
                self.arrangement.constraints.append((constraint_type, student, row, col))
                self.constraints_listbox.insert(tk.END, f"{student} prefers location ({row},{col})")
            except ValueError:
                messagebox.showerror("Error", "Invalid row,column format or out of range")
                return
        else:
            if student not in self.arrangement.students:
                messagebox.showerror("Error", "Student not found in the list")
                return
            if any(target not in self.arrangement.students for target in selected_targets):
                messagebox.showerror("Error", "One or more selected students not found in the list")
                return
            self.arrangement.constraints.append((constraint_type, student, selected_targets))
            if constraint_type == "not_next_to":
                self.constraints_listbox.insert(tk.END, f"{student} does not want to sit next to {', '.join(selected_targets)}")
            else:
                self.constraints_listbox.insert(tk.END, f"{student} prefers to sit next to {', '.join(selected_targets)}")
        
        self.target_listbox.selection_clear(0, tk.END)
        messagebox.showinfo("Success", "Constraint added successfully")

    def remove_constraint(self):
        selected_index = self.constraints_listbox.curselection()
        if selected_index:
            self.constraints_listbox.delete(selected_index)
            del self.arrangement.constraints[selected_index[0]]
            messagebox.showinfo("Success", "Constraint removed successfully")

    def calculate_seating(self):
        try:
            best_shibutz = self.arrangement.genetic_algorithm(pop_size=100, generations=50)
            seating = self.arrangement.display_seating(best_shibutz)
            
            result = "\n".join([" ".join([str(seating[row, col]) for col in range(self.arrangement.cols)]) for row in range(self.arrangement.rows)])
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
            rating = simpledialog.askinteger("Rating", "Rate the seating arrangement (0-10):")
            if rating is not None:
                messagebox.showinfo("Rating", f"Thank you for rating the model: {rating}")
            else:
                messagebox.showinfo("Rating", "Rating skipped")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingApp(root)
    root.mainloop()
