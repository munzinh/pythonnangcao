"""
Giao diện Tkinter cho ứng dụng To-Do List.

Module này triển khai giao diện người dùng đồ họa sử dụng Tkinter
với Treeview để hiển thị danh sách công việc và các điều khiển cho các thao tác CRUD.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from frontend.api_client import APIClient
from datetime import datetime


class TodoApp:
    """
    Giao diện chính của ứng dụng To-Do List.
    
    Triển khai thiết kế OOP với Tkinter cho giao diện người dùng và
    API client để giao tiếp với backend.
    """
    
    def __init__(self, root):
        """
        Khởi tạo ứng dụng.
        
        Args:
            root: Cửa sổ gốc Tkinter
        """
        self.root = root
        self.root.title("To-Do List Application - Đồ án Python Nâng Cao")
        self.root.geometry("1000x700")
        
        self.api_client = APIClient()
        self.selected_task_id = None
        
        self._setup_ui()
        self._load_tasks()
    
    def _setup_ui(self):
        """Thiết lập các thành phần giao diện người dùng."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        input_frame = ttk.LabelFrame(main_frame, text="Thông tin công việc", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Tiêu đề:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(input_frame, text="Mô tả:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(input_frame, text="Độ ưu tiên:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar(value="Trung bình")
        priority_combo = ttk.Combobox(
            input_frame, 
            textvariable=self.priority_var,
            values=["Thấp", "Trung bình", "Cao"],
            state="readonly",
            width=15
        )
        priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Thêm công việc", command=self._add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cập nhật công việc", command=self._update_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa công việc", command=self._delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa form", command=self._clear_form).pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.LabelFrame(main_frame, text="Tìm kiếm & Lọc", padding="10")
        search_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N), padx=(10, 0), pady=(0, 10))
        
        ttk.Label(search_frame, text="Tìm kiếm:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(search_frame, text="Tìm kiếm", command=self._search_tasks).grid(row=0, column=2, pady=5)
        
        ttk.Label(search_frame, text="Lọc:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(search_frame, text="Tất cả", variable=self.filter_var, value="all", command=self._load_tasks).grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(search_frame, text="Hoàn thành", variable=self.filter_var, value="completed", command=self._load_tasks).grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(search_frame, text="Chưa hoàn thành", variable=self.filter_var, value="pending", command=self._load_tasks).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Button(search_frame, text="Xuất CSV", command=self._export_csv).grid(row=4, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(search_frame, text="Xuất JSON", command=self._export_json).grid(row=5, column=0, columnspan=3, pady=(0, 5), sticky=(tk.W, tk.E))
        
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
        self.task_tree.heading("Title", text="Tiêu đề")
        self.task_tree.heading("Description", text="Mô tả")
        self.task_tree.heading("Priority", text="Độ ưu tiên")
        self.task_tree.heading("Status", text="Trạng thái")
        self.task_tree.heading("Created", text="Tạo lúc")
        self.task_tree.heading("Updated", text="Cập nhật lúc")
        
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
        
        self.status_label = ttk.Label(status_frame, text="Sẵn sàng", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        ttk.Label(main_frame, text="Mẹo: Double-click vào công việc để đánh dấu hoàn thành", 
                 font=('Arial', 9, 'italic')).grid(row=3, column=0, columnspan=2, pady=5)
    
    def _load_tasks(self):
        """Tải danh sách công việc từ API và hiển thị trong Treeview."""
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
                status = "Hoàn thành" if task['completed'] else "Chưa hoàn thành"
                created = self._format_datetime(task.get('created_at', ''))
                updated = self._format_datetime(task.get('updated_at', ''))
                
                # Chuyển đổi priority sang tiếng Việt
                priority_map = {
                    'Low': 'Thấp',
                    'Medium': 'Trung bình', 
                    'High': 'Cao'
                }
                priority = priority_map.get(task.get('priority', 'Medium'), task.get('priority', 'Medium'))
                
                self.task_tree.insert('', tk.END, values=(
                    task['id'],
                    task['title'],
                    task.get('description', ''),
                    priority,
                    status,
                    created,
                    updated
                ))
            
            self.status_label.config(text=f"Đã tải {len(tasks)} công việc")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            self.status_label.config(text=f"Lỗi: {str(e)}")
    
    def _format_datetime(self, dt_string):
        """Định dạng chuỗi datetime để hiển thị."""
        try:
            if not dt_string:
                return ""
            dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return dt_string
    
    def _add_task(self):
        """Thêm công việc mới."""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        
        # Chuyển đổi priority từ tiếng Việt sang tiếng Anh
        priority_map = {
            'Thấp': 'Low',
            'Trung bình': 'Medium',
            'Cao': 'High'
        }
        priority = priority_map.get(priority, priority)
        
        if not title:
            messagebox.showwarning("Cảnh báo", "Tiêu đề là bắt buộc!")
            return
        
        try:
            self.api_client.create_task(title, description, priority)
            messagebox.showinfo("Thành công", "Đã thêm công việc thành công!")
            self._clear_form()
            self._load_tasks()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _update_task(self):
        """Cập nhật công việc đã chọn."""
        if not self.selected_task_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để cập nhật!")
            return
        
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        
        # Chuyển đổi priority từ tiếng Việt sang tiếng Anh
        priority_map = {
            'Thấp': 'Low',
            'Trung bình': 'Medium',
            'Cao': 'High'
        }
        priority = priority_map.get(priority, priority)
        
        if not title:
            messagebox.showwarning("Cảnh báo", "Tiêu đề là bắt buộc!")
            return
        
        try:
            self.api_client.update_task(
                self.selected_task_id,
                title=title,
                description=description,
                priority=priority
            )
            messagebox.showinfo("Thành công", "Đã cập nhật công việc thành công!")
            self._clear_form()
            self._load_tasks()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _delete_task(self):
        """Xóa công việc đã chọn."""
        if not self.selected_task_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa công việc này?"):
            try:
                self.api_client.delete_task(self.selected_task_id)
                messagebox.showinfo("Thành công", "Đã xóa công việc thành công!")
                self._clear_form()
                self._load_tasks()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    
    def _toggle_complete(self, event):
        """Chuyển đổi trạng thái hoàn thành của công việc khi double-click."""
        if not self.selected_task_id:
            return
        
        try:
            selected_item = self.task_tree.selection()[0]
            values = self.task_tree.item(selected_item)['values']
            current_status = values[4]
            
            new_completed = False if current_status == "Hoàn thành" else True
            
            self.api_client.update_task(self.selected_task_id, completed=new_completed)
            self._load_tasks()
            self.status_label.config(text="Đã cập nhật trạng thái công việc")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _search_tasks(self):
        """Tìm kiếm công việc theo từ khóa."""
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        
        try:
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)
            
            tasks = self.api_client.search_tasks(query)
            
            for task in tasks:
                status = "Hoàn thành" if task['completed'] else "Chưa hoàn thành"
                created = self._format_datetime(task.get('created_at', ''))
                updated = self._format_datetime(task.get('updated_at', ''))
                
                # Chuyển đổi priority sang tiếng Việt
                priority_map = {
                    'Low': 'Thấp',
                    'Medium': 'Trung bình', 
                    'High': 'Cao'
                }
                priority = priority_map.get(task.get('priority', 'Medium'), task.get('priority', 'Medium'))
                
                self.task_tree.insert('', tk.END, values=(
                    task['id'],
                    task['title'],
                    task.get('description', ''),
                    priority,
                    status,
                    created,
                    updated
                ))
            
            self.status_label.config(text=f"Tìm thấy {len(tasks)} công việc khớp với '{query}'")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def _export_csv(self):
        """Xuất danh sách công việc ra file CSV."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"cong_viec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filepath:
            try:
                self.api_client.export_csv(filepath)
                messagebox.showinfo("Thành công", f"Đã xuất danh sách công việc ra {filepath}")
                self.status_label.config(text=f"Đã xuất ra {filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    
    def _export_json(self):
        """Xuất danh sách công việc ra file JSON."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"cong_viec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filepath:
            try:
                self.api_client.export_json(filepath)
                messagebox.showinfo("Thành công", f"Đã xuất danh sách công việc ra {filepath}")
                self.status_label.config(text=f"Đã xuất ra {filepath}")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    
    def _on_task_select(self, event):
        """Xử lý khi chọn công việc trong Treeview."""
        try:
            selected_item = self.task_tree.selection()[0]
            values = self.task_tree.item(selected_item)['values']
            
            self.selected_task_id = values[0]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[1])
            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, values[2])
            
            # Set priority trực tiếp (đã là tiếng Việt)
            self.priority_var.set(values[3])
            
            self.status_label.config(text=f"Đã chọn công việc ID: {self.selected_task_id}")
        except IndexError:
            pass
    
    def _clear_form(self):
        """Xóa dữ liệu trong form nhập liệu."""
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.priority_var.set("Trung bình")
        self.selected_task_id = None
        self.status_label.config(text="Đã xóa form")


def main():
    """Điểm khởi đầu chính cho ứng dụng GUI."""
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
