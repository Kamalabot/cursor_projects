from flask import Flask, render_template
from redis import Redis
import json
from datetime import datetime, timedelta
from app import app as main_app
import threading
import time

# Create a new Flask app for the dashboard
dashboard = Flask(__name__)

# Redis connection
redis_client = Redis(host='localhost', port=6379, db=0)

# Redis keys
TOTAL_TASKS_KEY = "metrics:total_tasks"
COMPLETED_TASKS_KEY = "metrics:completed_tasks"
ACTIVE_USERS_KEY = "metrics:active_users"
USER_ACTIVITY_KEY = "metrics:user_activity"
TASK_CREATION_HISTORY = "metrics:task_creation_history"

# Instrument the main app with Redis metrics
def instrument_main_app():
    # Note: These view functions need to match the route names defined in app.py
    # For example, if your routes are defined as:
    # @app.route('/add_task', methods=['POST'])
    # @app.route('/toggle_task/<int:task_id>', methods=['POST']) 
    # @app.route('/delete_task/<int:task_id>', methods=['POST'])
    # @app.route('/login', methods=['GET', 'POST'])
    # @app.route('/logout')
    original_add_task = main_app.view_functions['add_task']
    original_toggle_task = main_app.view_functions['toggle_task'] 
    original_delete_task = main_app.view_functions['delete_task']
    original_login = main_app.view_functions['login']
    original_logout = main_app.view_functions['logout']

    def track_add_task(*args, **kwargs):
        response = original_add_task(*args, **kwargs)
        # Increment total tasks counter
        redis_client.incr(TOTAL_TASKS_KEY)
        # Add to task creation history
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        redis_client.lpush(TASK_CREATION_HISTORY, timestamp)
        return response

    def track_toggle_task(*args, **kwargs):
        response = original_toggle_task(*args, **kwargs)
        # Update completed tasks counter
        redis_client.incr(COMPLETED_TASKS_KEY)
        return response

    def track_delete_task(*args, **kwargs):
        response = original_delete_task(*args, **kwargs)
        # Decrement total tasks counter
        redis_client.decr(TOTAL_TASKS_KEY)
        return response

    def track_login(*args, **kwargs):
        response = original_login(*args, **kwargs)
        # Track active users
        redis_client.sadd(ACTIVE_USERS_KEY, str(kwargs.get('user_id')))
        return response

    def track_logout(*args, **kwargs):
        response = original_logout(*args, **kwargs)
        # Remove from active users
        redis_client.srem(ACTIVE_USERS_KEY, str(kwargs.get('user_id')))
        return response

    # Replace original functions with instrumented versions
    main_app.view_functions['add_task'] = track_add_task
    main_app.view_functions['toggle_task'] = track_toggle_task
    main_app.view_functions['delete_task'] = track_delete_task
    main_app.view_functions['login'] = track_login
    main_app.view_functions['logout'] = track_logout

# Dashboard routes
@dashboard.route('/')
def show_dashboard():
    metrics = {
        'total_tasks': int(redis_client.get(TOTAL_TASKS_KEY) or 0),
        'completed_tasks': int(redis_client.get(COMPLETED_TASKS_KEY) or 0),
        'active_users': len(redis_client.smembers(ACTIVE_USERS_KEY)),
        'task_creation_history': get_task_creation_history()
    }
    return render_template('dashboard/metrics.html', metrics=metrics)

def get_task_creation_history():
    history = redis_client.lrange(TASK_CREATION_HISTORY, 0, -1)
    return [timestamp.decode('utf-8') for timestamp in history]

# Background task to clean up old data
def cleanup_old_data():
    while True:
        # Clean up task creation history older than 7 days
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        redis_client.ltrim(TASK_CREATION_HISTORY, 0, 10000)  # Keep last 10000 entries
        time.sleep(3600)  # Run every hour

def start_dashboard(host='0.0.0.0', port=5001):
    # Instrument the main app
    instrument_main_app()
    
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_data, daemon=True)
    cleanup_thread.start()
    
    # Run the dashboard
    dashboard.run(host=host, port=port)

if __name__ == '__main__':
    start_dashboard()