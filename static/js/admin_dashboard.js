document.addEventListener('DOMContentLoaded', function() {
    const requirementsForm = document.getElementById('requirements-form');
    
    if (!requirementsForm) return;
    
    requirementsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const requirements = {};
        const inputs = document.querySelectorAll('.staff-requirement');
        
        inputs.forEach(input => {
            requirements[input.dataset.hour] = parseInt(input.value) || 0;
        });

        const weekDateInput = document.querySelector('input[name="today"]');
        if (!weekDateInput) return;

        const weekDate = weekDateInput.value;

        fetch('/admin/set-hourly-requirements', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                requirements: requirements,
                week_date: weekDate
            })
        })
        .then(response => response.json().then(data => ({
            ok: response.ok,
            data: data
        })))
        .then(({ok, data}) => {
            if (ok && data.message) {
                alert('Requirements saved successfully!');
                window.location.reload();
            } else {
                alert('Error saving requirements: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            alert('Error saving requirements. Please try again.');
        });
    });
});