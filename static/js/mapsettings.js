document.addEventListener('DOMContentLoaded', function () {
    const administrativeDivisionSelect = document.getElementById('administrativeDivision');
    const walkTimeInput = document.getElementById('walkTime');
    const amenityTypeSelect = document.getElementById('amenityType');

    // Function to fetch data and populate the administrative division dropdown
    async function populateAdministrativeDivisions() {
        const apiUrl = '/api/administrative-divisions';

        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const divisions = await response.json();

            // Clear existing options
            administrativeDivisionSelect.innerHTML = '<option selected disabled>Изберете...</option>';

            // Add new options from API data
            divisions.forEach(division => {
                const option = document.createElement('option');
                option.value = division[0];
                option.textContent = division[1];
                administrativeDivisionSelect.appendChild(option);
            });

        } catch (error) {
            console.error('Error fetching administrative divisions:', error);
            const errorOption = document.createElement('option');
            errorOption.textContent = 'Error loading divisions';
            errorOption.disabled = true;
            administrativeDivisionSelect.appendChild(errorOption);
        }
    }

    function handleFormChange() {
        const settings = {
            administrativeDivision: administrativeDivisionSelect.value,
            walkTime: parseInt(walkTimeInput.value, 10),
            amenityType: amenityTypeSelect.value
        };
        console.log('Form settings changed:', settings);
    }

    // Call the function to populate the dropdown when the page loads
    populateAdministrativeDivisions();

    // Add event listeners for changes
    administrativeDivisionSelect.addEventListener('change', handleFormChange);
    walkTimeInput.addEventListener('change', handleFormChange);
    amenityTypeSelect.addEventListener('change', handleFormChange);

    // Initial log of settings when the page loads (after divisions are potentially loaded)
    handleFormChange();
});
