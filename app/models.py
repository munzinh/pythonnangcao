"""
Model cơ sở dữ liệu dùng SQLAlchemy ORM cho ứng dụng TaskMaster.
Giải thích từng dòng & tối ưu cho trình bày đồ án.
"""

from datetime import datetime  # Thư viện ngày giờ tích hợp
from app.extensions import db    # Kết nối tới SQLAlchemy từ Flask


class Task(db.Model):
    """
    Model đại diện cho 1 task (việc cần làm).
    """
    __tablename__ = 'tasks'  # Tên bảng trong CSDL
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # ID tự tăng
    title = db.Column(db.String(200), nullable=False, index=True)    # Tiêu đề task (bắt buộc)
    description = db.Column(db.Text, nullable=True)                  # Mô tả chi tiết
    completed = db.Column(db.Boolean, default=False, nullable=False, index=True) # Trạng thái hoàn thành
    priority = db.Column(db.String(20), default='Medium', index=True)            # Ưu tiên (Thấp/Trung Bình/Cao)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True) # Ngày tạo
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # Ngày cập nhật cuối

    def to_dict(self):
        """
        Chuyển object Task thành dict dễ serialize sang JSON/truyền qua API.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        # Chuỗi mô tả task khi in ra console/log
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"


class TaskManager:
    """
    Lớp xử lý nghiệp vụ CRUD (tạo, đọc, cập nhật, xoá) cho Task.
    Dễ sử dụng trong API & web.
    """
    @staticmethod
    def create_task(title, description=None, priority='Medium'):
        """
        Tạo task mới (trả về dict dữ liệu task hoặc raise lỗi).
        """
        if not title or not title.strip():
            raise ValueError("Task title không được để trống")
        try:
            task = Task(title=title.strip(), description=description.strip() if description else None, priority=priority)
            db.session.add(task)
            db.session.commit()
            return task.to_dict()  # Trả về dạng dict thuận tiện
        except Exception as e:
            db.session.rollback()
            print(f"Error creating task: {str(e)}")
            raise

    @staticmethod
    def get_all_tasks(completed=None):
        """
        Lấy danh sách tất cả task, có thể lọc theo trạng thái hoàn thành.
        """
        try:
            query = Task.query
            if completed is not None:
                query = query.filter(Task.completed == completed)
            tasks = query.order_by(Task.created_at.desc()).all()
            return [task.to_dict() for task in tasks]
        except Exception as e:
            print(f"Error getting tasks: {str(e)}")
            return []

    @staticmethod
    def get_task_by_id(task_id):
        """
        Lấy 1 task theo ID (dùng cho API xem chi tiết/chỉnh sửa)
        """
        try:
            task = Task.query.filter(Task.id == task_id).first()
            return task.to_dict() if task else None
        except Exception as e:
            print(f"Error getting task: {str(e)}")
            return None

    @staticmethod
    def update_task(task_id, **kwargs):
        """
        Cập nhật thông tin của task (theo key truyền vào).
        """
        try:
            task = Task.query.filter(Task.id == task_id).first()
            if not task:
                return None
            if 'title' in kwargs:
                if not kwargs['title'] or not kwargs['title'].strip():
                    raise ValueError("Task title không được để trống")
                task.title = kwargs['title'].strip()
            if 'description' in kwargs:
                task.description = kwargs['description'].strip() if kwargs['description'] else None
            if 'completed' in kwargs:
                task.completed = bool(kwargs['completed'])
            if 'priority' in kwargs:
                task.priority = kwargs['priority']
            task.updated_at = datetime.utcnow()  # update thời gian chỉnh sửa
            db.session.commit()
            return task.to_dict()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating task: {str(e)}")
            raise

    @staticmethod
    def delete_task(task_id):
        """
        Xoá task bằng ID (trả về True/False tuỳ kết quả).
        """
        try:
            task = Task.query.filter(Task.id == task_id).first()
            if not task:
                return False
            db.session.delete(task)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting task: {str(e)}")
            raise

    @staticmethod
    def search_tasks(query):
        """
        Tìm task theo chuỗi query (trên tiêu đề hoặc mô tả).
        """
        try:
            search_pattern = f"%{query}%"
            tasks = Task.query.filter(
                (Task.title.like(search_pattern)) |
                (Task.description.like(search_pattern))
            ).order_by(Task.created_at.desc()).all()
            return [task.to_dict() for task in tasks]
        except Exception as e:
            print(f"Error searching tasks: {str(e)}")
            return []
