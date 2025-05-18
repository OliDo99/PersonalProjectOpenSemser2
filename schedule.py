from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class ScheduleGenerator:
    def __init__(self, availability_data: Dict, hourly_requirements: Dict):
        self.availability = availability_data
        self.hourly_requirements = hourly_requirements
        self.schedule = {}

    def _get_available_slots(self, date: str) -> Dict[str, List[Dict]]:
        """Get all available slots for a given date"""
        available_slots = {}
        for employee, slots in self.availability.items():
            employee_slots = [slot for slot in slots if slot['date'] == date]
            if employee_slots:
                available_slots[employee] = employee_slots
        return available_slots

    def _is_employee_available(self, employee: str, date: str, hour: int) -> bool:
        """Check if an employee is available at a specific hour"""
        if employee not in self.availability:
            return False
        
        for slot in self.availability[employee]:
            if slot['date'] == date:
                from_hour = int(slot['from'].split(':')[0])
                to_hour = int(slot['to'].split(':')[0])
                if from_hour <= hour < to_hour:
                    return True
        return False

    def _get_assigned_employees(self, date: str, hour: int) -> List[str]:
        """Get list of employees already assigned to this hour"""
        if date not in self.schedule:
            return []
        return [shift['employee'] for shift in self.schedule[date] 
                if int(shift['from'].split(':')[0]) <= hour < int(shift['to'].split(':')[0])]

    def generate_schedule(self, start_date: str, end_date: str) -> Dict:
        """Generate schedule for the given date range"""
        current_date = datetime.strptime(start_date, "%d.%m.%Y")
        end = datetime.strptime(end_date, "%d.%m.%Y")
        assigned_hours = {employee: 0 for employee in self.availability.keys()}

        while current_date <= end:
            date_str = current_date.strftime("%d.%m.%Y")
            self.schedule[date_str] = []
            
            # For each hour of the day
            for hour in range(24):
                # Get required staff count for this hour
                required_staff = self.hourly_requirements.get(str(hour), 0)
                if required_staff == 0:
                    continue

                # Get currently assigned staff for this hour
                assigned = self._get_assigned_employees(date_str, hour)
                needed = required_staff - len(assigned)

                if needed <= 0:
                    continue

                # Find available employees for this hour
                available_employees = [
                    emp for emp in self.availability.keys()
                    if emp not in assigned and self._is_employee_available(emp, date_str, hour)
                ]

                # Sort by assigned hours (prioritize those with fewer hours)
                available_employees.sort(key=lambda x: assigned_hours[x])

                # Assign shifts to meet the requirement
                for employee in available_employees[:needed]:
                    # Find the longest continuous block we can assign
                    start_hour = hour
                    end_hour = hour + 1

                    # Extend forward if possible
                    while (end_hour < 24 and 
                           self._is_employee_available(employee, date_str, end_hour) and
                           len(self._get_assigned_employees(date_str, end_hour)) < self.hourly_requirements.get(str(end_hour), 0)):
                        end_hour += 1

                    # Add the shift
                    self.schedule[date_str].append({
                        'employee': employee,
                        'from': f"{start_hour:02d}:00",
                        'to': f"{end_hour:02d}:00"
                    })
                    assigned_hours[employee] += (end_hour - start_hour)

            current_date += timedelta(days=1)

        return {
            'schedule': self.schedule,
            'assigned_hours': assigned_hours,
            'hourly_requirements': self.hourly_requirements
        }