from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from datetime import datetime, timedelta
import json
import os
from auth import auth, login_manager, User

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

@app.route('/')
@login_required
def home():
    today = datetime.today() - timedelta(days=2)
    week_dates = get_week_dates(today)
    saved_availability = load_availability().get(current_user.id, [])
    return render_template('calendar.html', today=today.strftime("%d %B, %Y"), week_dates=week_dates, saved_availability=saved_availability)

@app.route('/calendar', methods=["GET", "POST"])
@login_required
def user_calendar():
    if request.method == "POST":

        direction = request.form.get("direction")
        current_date = request.form.get("today")

        today_date = datetime.strptime(current_date, "%d %B, %Y").date()

        temp = today_date + timedelta(days=int(direction))
        week_dates = get_week_dates(temp)

        today = temp.strftime("%d %B, %Y")
    else:
        date = datetime.today()
        week_dates = get_week_dates(date)
        today = datetime.today().strftime("%d %B, %Y")

    saved_availability = load_availability().get(current_user.id, [])
    return render_template('calendar.html', today=today, week_dates=week_dates, saved_availability=saved_availability)

@app.route('/availability', methods=['POST'])
@login_required
def update_availability():
    return redirect(url_for('user_calendar'))

@app.route('/save_availability', methods=['POST'])
@login_required
def save_availability():

    current_date = request.form.get("today")
    today = datetime.strptime(current_date, "%d %B, %Y").date()
    week_dates = get_week_dates(today)
    today = today.strftime("%d %B, %Y")

    availability_json = request.form.get("availability_data")
    try:
        new_availability = json.loads(availability_json) if availability_json else []
    except json.JSONDecodeError:
        new_availability = []
    
    
    # Load the current availability from the file
    all_availability = load_availability()
    current_availability = all_availability.get(current_user.id, [])
    
    # Merge both lists using set union to avoid duplicate keys
    merged_availability = list(set(current_availability) | set(new_availability))
    
    # Save the merged availability data back to the file
    all_availability[current_user.id] = merged_availability
    with open(availability_file, "w") as f:
        json.dump(all_availability, f)

    saved_availability = load_availability().get(current_user.id, [])
    return render_template('calendar.html', today=today, week_dates=week_dates, saved_availability=saved_availability)

# Routes for admin side
@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
