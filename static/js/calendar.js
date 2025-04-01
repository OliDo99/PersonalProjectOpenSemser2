document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('availability-form');
    
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
            
            if (fromTime && toTime) {
                availabilityData.push({
                    date: date,
                    from: fromTime,
                    to: toTime
                });
            }
        });
        
        
        document.getElementById('availability-data').value = JSON.stringify(availabilityData);
        console.log('Submitting data:', document.getElementById('availability-data').value); // Debug line
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