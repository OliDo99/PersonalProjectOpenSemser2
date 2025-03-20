let selectedCells = new Set();

function toggleAvailability(cell) {
    cell.classList.toggle('selected');
    
    const key = `${cell.dataset.date}-${cell.dataset.hour}`;
    if (selectedCells.has(key)) {
        selectedCells.delete(key);
    } else {
        selectedCells.add(key);
    }
    
    document.getElementById('availability-data').value = JSON.stringify(Array.from(selectedCells));
}

// Initialize calendar when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // The week date will be set by the template
    const weekDateElement = document.getElementById('current-week');
    if (weekDateElement && weekDateElement.dataset.weekStart) {
        weekDateElement.textContent = `Week of ${weekDateElement.dataset.weekStart}`;
    }
}); 