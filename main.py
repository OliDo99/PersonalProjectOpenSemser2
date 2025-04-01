from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from datetime import datetime, timedelta
import json
import os
from auth import auth, login_manager, User
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
availability_file = os.path.join(app.root_path, "availability.json")

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
    saved_availability = load_availability().get(current_user.id, [])
    return render_template('calendar.html', today=today.strftime("%d.%m.%Y"), week_dates=week_dates, saved_availability=saved_availability)

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
                         saved_availability=saved_availability)

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
                         saved_availability=saved_availability)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    today = datetime.today()
    week_dates = get_week_dates(today)
    all_availability = load_availability()
    
    return render_template('admin_dashboard.html',
                           today=today,
                         week_dates=week_dates,
                         all_availability=all_availability)

if __name__ == '__main__':
    app.run(debug=True)
    
