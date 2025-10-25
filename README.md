# TaskMaster - Todo List Application

A modern, professional Flask web application for managing your tasks with a clean, responsive interface built with Bootstrap 5.

## 🚀 Features

- **Modern Web Interface**: Clean, responsive design with Bootstrap 5
- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Task Management**: Mark tasks as completed, set priorities, add descriptions
- **Search & Filter**: Search tasks by title/description, filter by completion status
- **Export Functionality**: Export tasks to CSV or JSON format
- **RESTful API**: Complete API endpoints for all operations
- **Database Support**: SQLite (default) or MySQL/PostgreSQL
- **Professional Structure**: Organized codebase following Flask best practices

## 📁 Project Structure

```
todo_app/
├── app/                    # Main application package
│   ├── api/               # API blueprint (REST endpoints)
│   │   ├── __init__.py
│   │   └── routes.py      # API routes
│   ├── main/              # Web frontend blueprint
│   │   ├── __init__.py
│   │   └── routes.py      # Web routes
│   ├── errors/            # Error handlers
│   │   ├── __init__.py
│   │   └── handlers.py    # Error handling
│   ├── static/            # Static files
│   │   ├── css/
│   │   │   └── main.css   # Custom styles
│   │   └── js/
│   │       └── main.js    # Frontend JavaScript
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template
│   │   ├── index.html     # Main page
│   │   └── errors/        # Error pages
│   ├── __init__.py        # Application factory
│   ├── config.py          # Configuration
│   ├── extensions.py      # Flask extensions
│   └── models.py          # Database models
├── migrations/            # Database migrations (Flask-Migrate)
├── run.py                 # Application entry point
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd TaskMaster
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URI=sqlite:///todo.db
# For MySQL: DATABASE_URI=mysql+pymysql://user:password@localhost/todo_db
# For PostgreSQL: DATABASE_URI=postgresql://user:password@localhost/todo_db
```

### Step 5: Initialize Database

```bash
# Initialize Flask-Migrate
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## 🚀 Running the Application

### Development Mode

```bash
# Method 1: Using run.py
python run.py

# Method 2: Using Flask CLI
flask run

# Method 3: Using environment variables
export FLASK_APP=run.py
flask run
```

The application will be available at:
- **Web Interface**: http://localhost:5000/
- **API Base**: http://localhost:5000/api/

## 📚 API Documentation

### Task Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/<id>` | Get a specific task |
| PUT | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |
| GET | `/api/tasks/search?q=<query>` | Search tasks |
| GET | `/api/tasks/export/csv` | Export tasks as CSV |
| GET | `/api/tasks/export/json` | Export tasks as JSON |

### Request/Response Examples

#### Create a Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the TaskMaster application",
    "priority": "High"
  }'
```

#### Get All Tasks
```bash
curl http://localhost:5000/api/tasks
```

#### Update a Task
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

## 🎨 Web Interface Features

### Main Dashboard
- **Task List**: View all tasks in a responsive table
- **Add Task**: Modal form for creating new tasks
- **Edit Task**: Click edit button to modify existing tasks
- **Toggle Status**: Mark tasks as completed/pending
- **Delete Task**: Remove tasks with confirmation

### Search & Filter
- **Search**: Real-time search by title or description
- **Filter**: Filter by completion status (All, Pending, Completed)
- **Priority**: Visual priority indicators (High, Medium, Low)

### Export Options
- **CSV Export**: Download tasks as CSV file
- **JSON Export**: Download tasks as JSON file

## 🗄️ Database Configuration

### SQLite (Default)
The application uses SQLite by default, which requires no additional setup.

### MySQL
For MySQL, install the required driver and update your configuration:

```bash
pip install PyMySQL
```

Update your `.env` file:
```env
DATABASE_URI=mysql+pymysql://username:password@localhost/todo_db
```

### PostgreSQL
For PostgreSQL, install the required driver:

```bash
pip install psycopg2-binary
```

Update your `.env` file:
```env
DATABASE_URI=postgresql://username:password@localhost/todo_db
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Flask environment |
| `FLASK_DEBUG` | `True` | Debug mode |
| `SECRET_KEY` | `dev-secret-key...` | Flask secret key |
| `DATABASE_URI` | `sqlite:///todo.db` | Database connection string |

### Configuration Classes

The application supports multiple configuration environments:

- **Development**: Debug enabled, SQLite database
- **Testing**: Test database, debug disabled
- **Production**: Optimized settings, production database

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py
```

## 📦 Deployment

### Production Deployment

1. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URI=your-production-database-url
   ```

2. **Install Production Dependencies**:
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🎯 Roadmap

- [ ] User authentication and authorization
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] File attachments
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] Advanced reporting and analytics

---

**Built with ❤️ using Flask, Bootstrap, and modern web technologies.**