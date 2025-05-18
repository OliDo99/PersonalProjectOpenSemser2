document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('availability-form');
    
    // Function to validate time slots
    function validateTimeSlots(from, to) {
        if (!from || !to) return false;
        const fromTime = parseInt(from.split(':')[0]);
        const toTime = parseInt(to.split(':')[0]);
        return fromTime < toTime;
    }

    // Function to update the To dropdown based on From selection
    function updateToDropdown(fromSelect, toSelect) {
        const fromValue = fromSelect.value;
        toSelect.innerHTML = '<option value="">Select To</option>';
        
        if (fromValue) {
            const selectedHour = parseInt(fromValue);
            for (let hour = selectedHour + 1; hour <= 24; hour++) {
                const hourStr = hour.toString().padStart(2, '0') + ':00';
                toSelect.innerHTML += `<option value="${hourStr}">${hourStr}</option>`;
            }
            toSelect.disabled = false;
        } else {
            toSelect.disabled = true;
        }
    }

    // Set up initial state and event listeners
    document.querySelectorAll('.time-slot-from').forEach(fromSelect => {
        const row = fromSelect.closest('tr');
        const toSelect = row.querySelector('.time-slot-to');
        
        // Initial setup
        if (fromSelect.value) {
            updateToDropdown(fromSelect, toSelect);
            toSelect.value = toSelect.querySelector('option[selected]')?.value || '';
        }

        fromSelect.addEventListener('change', function() {
            updateToDropdown(this, toSelect);
        });
    });
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const availabilityData = [];
        const rows = document.querySelectorAll('tbody tr');
          rows.forEach(row => {
            const fromSelect = row.querySelector('.time-slot-from');
            const toSelect = row.querySelector('.time-slot-to');
            
            const date = fromSelect.dataset.date;
            const fromTime = fromSelect.value;
            const toTime = toSelect.value;
            
            if (fromTime && toTime && validateTimeSlots(fromTime, toTime)) {
                availabilityData.push({
                    date: date,
                    from: fromTime,
                    to: toTime
                });
            }
        });
        
        if (availabilityData.length === 0) {
            alert('Please select at least one valid time slot (From time must be before To time)');
            return;
        }

        document.getElementById('availability-data').value = JSON.stringify(availabilityData);
        form.submit();
        
    });

    // Add change event listeners to all "From" dropdowns
    document.querySelectorAll('.time-slot-from').forEach(fromSelect => {
        fromSelect.addEventListener('change', function() {
            const row = this.closest('tr');
            const toSelect = row.querySelector('.time-slot-to');
            
            // Clear existing options
            toSelect.innerHTML = '<option value="">Select To</option>';
            
            if (this.value) {
                // Enable the "To" dropdown
                toSelect.disabled = false;
                
                // Get the selected hour
                const selectedHour = parseInt(this.value);
                
                // Add new options starting from the selected hour + 1
                for (let hour = selectedHour + 1; hour <= 24; hour++) {
                    const option = document.createElement('option');
                    option.value = `${hour.toString().padStart(2, '0')}:00`;
                    option.textContent = `${hour.toString().padStart(2, '0')}:00`;
                    toSelect.appendChild(option);
                }
            } else {
                // Disable the "To" dropdown if no "From" time is selected
                toSelect.disabled = true;
            }
        });
    });
});