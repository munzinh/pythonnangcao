/**
 * Main JavaScript for TaskMaster
 * 
 * This file contains the main JavaScript functionality for the todo list application.
 * It handles API interactions, DOM manipulation, and user interactions.
 */

// Global variables
let currentTaskId = null;
let currentFilter = 'all';
let searchTimeout = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    loadTasks();
    setupEventListeners();
    console.log('TaskMaster initialized');
}

/**
 * Setup event listeners for user interactions
 */
function setupEventListeners() {
    // Filter change handlers
    document.querySelectorAll('input[name="filter"]').forEach(radio => {
        radio.addEventListener('change', function() {
            currentFilter = this.value;
            loadTasks();
        });
    });
    
    // Search input handler with debouncing
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.trim()) {
                    searchTasks();
                } else {
                    loadTasks();
                }
            }, 500);
        });
    }
    
    // Task form submission
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        taskForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveTask();
        });
    }
    
    // Modal reset handler
    const taskModal = document.getElementById('taskModal');
    if (taskModal) {
        taskModal.addEventListener('hidden.bs.modal', function() {
            resetTaskForm();
        });
    }
    
    // Delete confirmation handler
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function() {
            confirmDelete();
        });
    }
}

/**
 * Load tasks from the API
 */
function loadTasks() {
    const tbody = document.getElementById('tasksTableBody');
    if (!tbody) return;
    
    showLoading();
    
    let url = '/api/tasks';
    if (currentFilter !== 'all') {
        url += `?completed=${currentFilter}`;
    }
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayTasks(data.data);
            } else {
                showError('Failed to load tasks: ' + data.error);
                displayEmptyState();
            }
        })
        .catch(error => {
            console.error('Error loading tasks:', error);
            showError('Error loading tasks: ' + error.message);
            displayEmptyState();
        });
}

/**
 * Display tasks in the table
 */
function displayTasks(tasks) {
    const tbody = document.getElementById('tasksTableBody');
    if (!tbody) return;
    
    if (tasks.length === 0) {
        displayEmptyState();
        return;
    }
    
    tbody.innerHTML = tasks.map(task => createTaskRow(task)).join('');
}

/**
 * Create HTML for a task row
 */
function createTaskRow(task) {
    const statusClass = task.completed ? 'success' : 'warning';
    const statusText = task.completed ? 'Completed' : 'Pending';
    const priorityColor = getPriorityColor(task.priority);
    const toggleIcon = task.completed ? 'arrow-counterclockwise' : 'check';
    const toggleTitle = task.completed ? 'Mark as Pending' : 'Mark as Completed';
    
    return `
        <tr class="${task.completed ? 'task-completed' : 'task-pending'}">
            <td>${task.id}</td>
            <td>
                <strong>${escapeHtml(task.title)}</strong>
            </td>
            <td>${escapeHtml(task.description || '')}</td>
            <td>
                <span class="badge bg-${priorityColor}">${task.priority}</span>
            </td>
            <td>
                <span class="badge bg-${statusClass}">${statusText}</span>
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="editTask(${task.id})" title="Edit">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-${task.completed ? 'warning' : 'success'}" 
                            onclick="toggleTask(${task.id}, ${!task.completed})" 
                            title="${toggleTitle}">
                        <i class="bi bi-${toggleIcon}"></i>
                    </button>
                    <button class="btn btn-outline-danger" onclick="deleteTask(${task.id})" title="Delete">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `;
}

/**
 * Display empty state when no tasks found
 */
function displayEmptyState() {
    const tbody = document.getElementById('tasksTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted">No tasks found</td></tr>';
}

/**
 * Show loading state
 */
function showLoading() {
    const tbody = document.getElementById('tasksTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = `
        <tr id="loadingRow">
            <td colspan="6" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </td>
        </tr>
    `;
}

/**
 * Search tasks
 */
function searchTasks() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) {
        loadTasks();
        return;
    }
    
    showLoading();
    
    fetch(`/api/tasks/search?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayTasks(data.data);
            } else {
                showError('Search failed: ' + data.error);
                displayEmptyState();
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            showError('Search error: ' + error.message);
            displayEmptyState();
        });
}

/**
 * Edit a task
 */
function editTask(taskId) {
    currentTaskId = taskId;
    
    fetch(`/api/tasks/${taskId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const task = data.data;
                populateTaskForm(task);
                showTaskModal('Edit Task', 'Update Task');
            } else {
                showError('Failed to load task: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error loading task:', error);
            showError('Error loading task: ' + error.message);
        });
}

/**
 * Populate task form with data
 */
function populateTaskForm(task) {
    document.getElementById('taskTitle').value = task.title;
    document.getElementById('taskDescription').value = task.description || '';
    document.getElementById('taskPriority').value = task.priority;
    document.getElementById('taskCompleted').checked = task.completed;
    document.getElementById('completedField').style.display = 'block';
}

/**
 * Show task modal
 */
function showTaskModal(title, buttonText) {
    document.getElementById('taskModalTitle').textContent = title;
    document.getElementById('taskSubmitBtn').textContent = buttonText;
    new bootstrap.Modal(document.getElementById('taskModal')).show();
}

/**
 * Save task (create or update)
 */
function saveTask() {
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const priority = document.getElementById('taskPriority').value;
    const completed = document.getElementById('taskCompleted').checked;
    
    if (!title) {
        showError('Title is required');
        return;
    }
    
    const taskData = {
        title: title,
        description: description || null,
        priority: priority,
        completed: completed
    };
    
    const url = currentTaskId ? `/api/tasks/${currentTaskId}` : '/api/tasks';
    const method = currentTaskId ? 'PUT' : 'POST';
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(taskData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('taskModal')).hide();
            loadTasks();
            showSuccess(data.message);
        } else {
            showError('Failed to save task: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error saving task:', error);
        showError('Error saving task: ' + error.message);
    });
}

/**
 * Toggle task completion status
 */
function toggleTask(taskId, completed) {
    fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ completed: completed })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            loadTasks();
            showSuccess('Task updated successfully');
        } else {
            showError('Failed to update task: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error updating task:', error);
        showError('Error updating task: ' + error.message);
    });
}

/**
 * Delete a task
 */
function deleteTask(taskId) {
    currentTaskId = taskId;
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

/**
 * Confirm delete action
 */
function confirmDelete() {
    if (!currentTaskId) return;
    
    fetch(`/api/tasks/${currentTaskId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
            loadTasks();
            showSuccess('Task deleted successfully');
        } else {
            showError('Failed to delete task: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error deleting task:', error);
        showError('Error deleting task: ' + error.message);
    });
}

/**
 * Export tasks
 */
function exportTasks(format) {
    window.open(`/api/tasks/export/${format}`, '_blank');
}

/**
 * Reset task form
 */
function resetTaskForm() {
    const form = document.getElementById('taskForm');
    if (form) {
        form.reset();
    }
    document.getElementById('taskModalTitle').textContent = 'Add New Task';
    document.getElementById('taskSubmitBtn').textContent = 'Add Task';
    document.getElementById('completedField').style.display = 'none';
    currentTaskId = null;
}

/**
 * Get priority color class
 */
function getPriorityColor(priority) {
    switch (priority) {
        case 'High': return 'danger';
        case 'Medium': return 'warning';
        case 'Low': return 'success';
        default: return 'secondary';
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show success message
 */
function showSuccess(message) {
    // TODO: Implement toast notifications
    console.log('Success:', message);
    // Temporary alert for now
    if (typeof alert !== 'undefined') {
        alert(message);
    }
}

/**
 * Show error message
 */
function showError(message) {
    // TODO: Implement toast notifications
    console.error('Error:', message);
    // Temporary alert for now
    if (typeof alert !== 'undefined') {
        alert(message);
    }
}
