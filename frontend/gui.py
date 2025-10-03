"""
Tkinter GUI for To-Do List Application.

This module implements the graphical user interface using Tkinter
with Treeview for task display and various controls for CRUD operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from frontend.api_client import APIClient
from datetime import datetime


class TodoApp:
    """
    Main To-Do List Application GUI.
    
    Implements OOP design with Tkinter for user interface and
    API client for backend communication.
    """
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("To-Do List Application - Đồ án Python Nâng Cao")
        self.root.geometry("1000x700")
        
        self.api_client = APIClient()
        self.selected_task_id = None
        
        self._setup_ui()
        self._load_tasks()
    
    def _setup_ui(self):
        """Setup the user interface components."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        input_frame = ttk.LabelFrame(main_frame, text="Task Information", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(input_frame, text="Priority:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(
            input_frame, 
            textvariable=self.priority_var,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=15
        )
        priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Task", command=self._add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Task", command=self._update_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self._delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self._clear_form).pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.LabelFrame(main_frame, text="Search & Filter", padding="10")
        search_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N), padx=(10, 0), pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(search_frame, text="Search", command=self._search_tasks).grid(row=0, column=2, pady=5)
        
        ttk.Label(search_frame, text="Filter:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(search_frame, text="All", variable=self.filter_var, value="all", command=self._load_tasks).grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(search_frame, text="Completed", variable=self.filter_var, value="completed", command=self._load_tasks).grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(search_frame, text="Pending", variable=self.filter_var, value="pending", command=self._load_tasks).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Button(search_frame, text="Export CSV", command=self._export_csv).grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(search_frame, text="Export JSON", command=self._export_json).grid(row=5, column=0, columnspan=3, pady=(0, 5), sticky=(tk.W, tk.E))
        
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree_scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.task_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Title", "Description", "Priority", "Status", "Created", "Updated"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tree_scroll_y.config(command=self.task_tree.yview)
        tree_scroll_x.config(command=self.task_tree.xview)
        
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Created", text="Created At")
        self.task_tree.heading("Updated", text="Updated At")
        
        self.task_tree.column("ID", width=50, anchor=tk.CENTER)
        self.task_tree.column("Title", width=200)
        self.task_tree.column("Description", width=300)
        self.task_tree.column("Priority", width=80, anchor=tk.CENTER)
        self.task_tree.column("Status", width=100, anchor=tk.CENTER)
        self.task_tree.column("Created", width=150)
        self.task_tree.column("Updated", width=150)
        
        self.task_tree.bind('<<TreeviewSelect>>', self._on_task_select)
        self.task_tree.bind('<Double-1>', self._toggle_complete)
        
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        ttk.Label(main_frame, text="Tip: Double-click a task to toggle completion", 
                 font=('Arial', 9, 'italic')).grid(row=3, column=0, columnspan=2, pady=5)
    
    def _load_tasks(self):
        """Load tasks from API and display in Treeview."""
        try:
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)
            
            filter_value = self.filter_var.get()
            completed = None
            if filter_value == "completed":
                completed = True
            elif filter_value == "pending":
                completed = False
            
            tasks = self.api_client.get_tasks(completed=completed)
            
            for task in tasks:
                status = "Completed" if task['completed'] else "Pending"
                created = self._format_datetime(task.get('created_at', ''))
                updated = self._format_datetime(task.get('updated_at', ''))
                
                self.task_tree.insert('', tk.END, values=(
                    task['id'],
                    task['title'],
                    task.get('description', ''),
                    task.get('priority', 'Medium'),
                    status,
                    created,
                    updated
                ))
            
            self.status_label.config(text=f"Loaded {len(tasks)} tasks")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text=f"Error: {str(e)}")
    
    def _format_datetime(self, dt_string):
        """Format datetime string for display."""
        try:
            if not dt_string:
                return ""
            dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return dt_string
    
    def _add_task(self):
        """Add a new task."""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        
        if not title:
            messagebox.showwarning("Warning", "Title is required!")
            return
        
        try:
            self.api_client.create_task(title, description, priority)
            messagebox.showinfo("Success", "Task added successfully!")
            self._clear_form()
            self._load_tasks()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _update_task(self):
        """Update selected task."""
        if not self.selected_task_id:
            messagebox.showwarning("Warning", "Please select a task to update!")
            return
        
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        
        if not title:
            messagebox.showwarning("Warning", "Title is required!")
            return
        
        try:
            self.api_client.update_task(
                self.selected_task_id,
                title=title,
                description=description,
                priority=priority
            )
            messagebox.showinfo("Success", "Task updated successfully!")
            self._clear_form()
            self._load_tasks()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _delete_task(self):
        """Delete selected task."""
        if not self.selected_task_id:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            try:
                self.api_client.delete_task(self.selected_task_id)
                messagebox.showinfo("Success", "Task deleted successfully!")
                self._clear_form()
                self._load_tasks()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _toggle_complete(self, event):
        """Toggle task completion status on double-click."""
        if not self.selected_task_id:
            return
        
        try:
            selected_item = self.task_tree.selection()[0]
            values = self.task_tree.item(selected_item)['values']
            current_status = values[4]
            
            new_completed = False if current_status == "Completed" else True
            
            self.api_client.update_task(self.selected_task_id, completed=new_completed)
            self._load_tasks()
            self.status_label.config(text="Task status updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _search_tasks(self):
        """Search tasks by query."""
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query!")
            return
        
        try:
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)
            
            tasks = self.api_client.search_tasks(query)
            
            for task in tasks:
                status = "Completed" if task['completed'] else "Pending"
                created = self._format_datetime(task.get('created_at', ''))
                updated = self._format_datetime(task.get('updated_at', ''))
                
                self.task_tree.insert('', tk.END, values=(
                    task['id'],
                    task['title'],
                    task.get('description', ''),
                    task.get('priority', 'Medium'),
                    status,
                    created,
                    updated
                ))
            
            self.status_label.config(text=f"Found {len(tasks)} tasks matching '{query}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _export_csv(self):
        """Export tasks to CSV file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filepath:
            try:
                self.api_client.export_csv(filepath)
                messagebox.showinfo("Success", f"Tasks exported to {filepath}")
                self.status_label.config(text=f"Exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _export_json(self):
        """Export tasks to JSON file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filepath:
            try:
                self.api_client.export_json(filepath)
                messagebox.showinfo("Success", f"Tasks exported to {filepath}")
                self.status_label.config(text=f"Exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _on_task_select(self, event):
        """Handle task selection in Treeview."""
        try:
            selected_item = self.task_tree.selection()[0]
            values = self.task_tree.item(selected_item)['values']
            
            self.selected_task_id = values[0]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[1])
            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, values[2])
            self.priority_var.set(values[3])
            
            self.status_label.config(text=f"Selected Task ID: {self.selected_task_id}")
        except IndexError:
            pass
    
    def _clear_form(self):
        """Clear input form."""
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.selected_task_id = None
        self.status_label.config(text="Form cleared")


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
