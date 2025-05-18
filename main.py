from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user
from datetime import datetime, timedelta
import json
import os
import json
import os
from auth import auth, login_manager, User
from functools import wraps
from schedule import ScheduleGenerator


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
availability_file = os.path.join(app.root_path, "availability.json")
required_hours_file = os.path.join(app.root_path, "required_hours.json")
schedule_file = os.path.join(app.root_path, "schedule.json")
hourly_requirements_file = os.path.join(app.root_path, "hourly_requirements.json")

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth, url_prefix='/auth')

def get_week_dates(date):
    monday = date - timedelta(days=date.weekday())
    week_dates = [monday + timedelta(days=i) for i in range(7)]
    return week_dates

def load_availability():
    try:
        with open(availability_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_required_hours():
    try:
        with open(required_hours_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_required_hours(required_hours):
    with open(required_hours_file, "w") as f:
        json.dump(required_hours, f)

def save_schedule(schedule_data):
    with open(schedule_file, "w") as f:
        json.dump(schedule_data, f)

def load_schedule():
    try:
        with open(schedule_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_hourly_requirements():
    try:
        with open(hourly_requirements_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_hourly_requirements(requirements):
    with open(hourly_requirements_file, "w") as f:
        json.dump(requirements, f)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    today = datetime.today() - timedelta(days=2)
    week_dates = get_week_dates(today)
    saved_availability = load_availability().get(str(current_user.id), [])
    return render_template('calendar.html', 
                         today=today.strftime("%d.%m.%Y"),
                         week_dates=week_dates,
                         saved_availability=saved_availability,
                         current_user=current_user)

@app.route('/calendar', methods=["GET", "POST"])
@login_required
def user_calendar():
    if request.method == "POST":
        direction = request.form.get("direction")
        current_date = request.form.get("today")

        today_date = datetime.strptime(current_date, "%d.%m.%Y").date()

        temp = today_date + timedelta(days=int(direction))
        week_dates = get_week_dates(temp)

        today = temp.strftime("%d.%m.%Y")
        pass
    else:
        date = datetime.today()
        week_dates = get_week_dates(date)
        today = datetime.today().strftime("%d.%m.%Y")

    saved_availability = load_availability().get(str(current_user.id), [])
    return render_template('calendar.html', 
                         today=today, 
                         week_dates=week_dates, 
                         saved_availability=saved_availability,
                         current_user=current_user)

@app.route('/availability', methods=['POST'])
@login_required
def update_availability():
    return redirect(url_for('user_calendar'))

@app.route('/save_availability', methods=['POST'])
@login_required
def save_availability():
    current_date = request.form.get("today")
    availability_data = request.form.get("availability_data")
    
    if not availability_data:
        flash('No availability data provided')
        return redirect(url_for('user_calendar'))
    
    try:
        today = datetime.strptime(current_date, "%d.%m.%Y").date()
        week_dates = get_week_dates(today)
        today = today.strftime("%d.%m.%Y")

        # Load the current availability from the file
        all_availability = load_availability()
        
        # Get current user's existing availability or create empty list
        user_availability = all_availability.get(str(current_user.id), [])
        
        # Parse the new JSON data from the form
        new_availability = json.loads(availability_data)
        
        # Validate the data structure
        if not isinstance(new_availability, list):
            raise ValueError("Invalid data format")
        
        # Convert dates to desired format
        for item in new_availability:
            date_obj = datetime.strptime(item['date'], '%d.%m.%Y')
            item['date'] = date_obj.strftime('%d.%m.%Y')
        
        # Remove any existing entries for the dates in new_availability
        current_dates = [item['date'] for item in new_availability]
        user_availability = [item for item in user_availability if item['date'] not in current_dates]
        
        # Add the new availability entries
        user_availability.extend(new_availability)
        
        # Update the user's availability
        all_availability[str(current_user.id)] = user_availability
        
        # Save the merged availability data back to the file
        with open(availability_file, "w") as f:
            json.dump(all_availability, f)

        flash('Availability saved successfully')
        
    except (json.JSONDecodeError, ValueError) as e:
        flash(f'Error saving availability: {str(e)}')
        return redirect(url_for('user_calendar'))
    
    saved_availability = load_availability().get(str(current_user.id), [])    
    return render_template('calendar.html', 
                         today=today, 
                         week_dates=week_dates, 
                         saved_availability=saved_availability,
                         current_user=current_user)

@app.route('/admin/dashboard', methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    if request.method == "POST":
        direction = request.form.get("direction")
        current_date = request.form.get("today")

        today_date = datetime.strptime(current_date, "%d.%m.%Y").date()
        temp = today_date + timedelta(days=int(direction))
        week_dates = get_week_dates(temp)
        today = temp.strftime("%d.%m.%Y")
    else:
        date = datetime.today()
        week_dates = get_week_dates(date)
        today = datetime.today().strftime("%d.%m.%Y")

    all_availability = load_availability()
    all_requirements = load_hourly_requirements()
    
    # Get requirements for current week
    hourly_requirements = all_requirements.get(today, {})
    # Initialize with zeros if no requirements exist for this week
    if not hourly_requirements:
        hourly_requirements = {str(i): 0 for i in range(24)}
    
    return render_template('admin_dashboard.html',
                         today=today,
                         week_dates=week_dates,
                         all_availability=all_availability,
                         hourly_requirements=hourly_requirements,
                         current_user=current_user)

@app.route('/admin/set-hours', methods=['POST'])
@admin_required
def set_required_hours():
    data = request.get_json()
    if not data or 'hours' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    required_hours = data['hours']
    save_required_hours(required_hours)
    return jsonify({'message': 'Required hours updated successfully'})

@app.route('/admin/set-hourly-requirements', methods=['POST'])
@admin_required
def set_hourly_requirements():
    data = request.get_json()
    
    if not data or 'requirements' not in data or 'week_date' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    week_date = data['week_date']
    requirements = data['requirements']
    
    try:
        # Load existing requirements
        all_requirements = load_hourly_requirements()
        if not isinstance(all_requirements, dict):
            all_requirements = {}
        
        # Convert all keys to strings to ensure consistent format
        requirements = {str(k): int(v) for k, v in requirements.items()}
        
        # Update requirements for this week
        all_requirements[week_date] = requirements
        
        # Save the updated requirements
        save_hourly_requirements(all_requirements)
        
        return jsonify({'message': 'Hourly requirements updated successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Error saving requirements: {str(e)}'}), 500

@app.route('/admin/schedule', methods=['GET', 'POST'])
@admin_required
def view_schedule():
    if request.method == "POST":
        direction = request.form.get("direction")
        current_date = request.form.get("today")

        today_date = datetime.strptime(current_date, "%d.%m.%Y").date()
        today = (today_date + timedelta(days=int(direction))).strftime("%d.%m.%Y")
    else:
        today = datetime.today().strftime("%d.%m.%Y")

    # Load all availability data
    all_availability = load_availability()
    
    # Convert the availability data into a timeline format
    formatted_availability = {}
    for user_id, availabilities in all_availability.items():
        user_data = {
            'name': user_id,
            'availabilities': {}
        }
        
        # Group availability slots by date
        for availability in availabilities:
            date = availability['date']
            start_time = datetime.strptime(availability['from'], '%H:%M')
            end_time = datetime.strptime(availability['to'], '%H:%M')
            
            if date not in user_data['availabilities']:
                user_data['availabilities'][date] = []
                
            user_data['availabilities'][date].append({
                'start_hour': start_time.hour,
                'end_hour': end_time.hour
            })
        
        formatted_availability[user_id] = user_data

    return render_template('schedule.html', 
                         today=today,
                         availability=formatted_availability,
                         current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)


