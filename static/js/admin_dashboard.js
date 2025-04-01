document.addEventListener('DOMContentLoaded', function() {
    // Initialize calendar navigation
    const prevWeekBtn = document.getElementById('prev-week');
    const nextWeekBtn = document.getElementById('next-week');
    
    function displayAvailability() {
        // Clear all cells first
        document.querySelectorAll('.staff-list').forEach(cell => cell.innerHTML = '');
        
        // Loop through each user's availability
        for (const [userId, availability] of Object.entries(availabilityData)) {
            availability.forEach(slot => {
                const date = slot.date;
                const fromHour = slot.from;
                const toHour = slot.to;
                
                // Find cells that match this time slot
                const cells = document.querySelectorAll(`.calendar-cell[data-date="${date}"]`);
                cells.forEach(cell => {
                    const cellHour = cell.dataset.hour;
                    if (isHourInRange(cellHour, fromHour, toHour)) {
                        const staffDiv = cell.querySelector('.staff-list');
                        if (!staffDiv.innerHTML.includes(userId)) {
                            staffDiv.innerHTML += `<div class="staff-member">${userId}</div>`;
                        }
                    }
                });
            });
        }
    }
    
    function isHourInRange(hour, from, to) {
        const hourNum = parseInt(hour.split(':')[0]);
        const fromNum = parseInt(from.split(':')[0]);
        const toNum = parseInt(to.split(':')[0]);
        return hourNum >= fromNum && hourNum < toNum;
    }
    
    // Navigation handlers
    prevWeekBtn.addEventListener('click', () => {
        // Add navigation logic
    });
    
    nextWeekBtn.addEventListener('click', () => {
        // Add navigation logic
    });
    
    // Initial display
    displayAvailability();
});