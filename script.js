function navigateTo(type) {
    localStorage.setItem('calcType', type);
    window.location.href = 'form.html';
}

window.onload = function() {
    const calcType = localStorage.getItem('calcType');
    const formTitle = document.getElementById('form-title');
    const inputFields = document.getElementById('input-fields');

    const materials = {
        'FR4': 0.3,
        'Aluminum': 205,
        'Copper': 385,
        'Gold': 317,
        'Silicon': 149
    };

    if (calcType) {
        formTitle.textContent = `Calculate ${calcType === 'source' ? 'Source' : 'Ambient'} Temperature`;

        const commonFields = `
            <label for="length">Length (m):</label>
            <input type="number" id="length" name="length" required><br>
            <label for="breadth">Breadth (m):</label>
            <input type="number" id="breadth" name="breadth" required><br>
            <label for="thickness">Thickness (m):</label>
            <input type="number" id="thickness" name="thickness" required><br>
            <label for="power">Thermal Power (Watt):</label>
            <input type="number" id="power" name="power" required><br>
            <label for="material">Material:</label>
            <select id="material" name="material" required>
                ${Object.keys(materials).map(material => `<option value="${materials[material]}">${material}</option>`).join('')}
            </select><br>
        `;

        if (calcType === 'source') {
            inputFields.innerHTML = `
                ${commonFields}
                <label for="ambientTemp">Ambient Temperature (K):</label>
                <input type="number" id="ambientTemp" name="ambientTemp" required><br>
            `;
        } else {
            inputFields.innerHTML = `
                ${commonFields}
                <label for="sourceTemp">Source Temperature (K):</label>
                <input type="number" id="sourceTemp" name="sourceTemp" required><br>
            `;
        }
    }
}

function calculate() {
    const form = document.getElementById('temperature-form');
    const formData = new FormData(form);
    const calcType = localStorage.getItem('calcType');
    
    const data = {
        length: parseFloat(formData.get('length')),
        breadth: parseFloat(formData.get('breadth')),
        thickness: parseFloat(formData.get('thickness')),
        power: parseFloat(formData.get('power')),
        k: parseFloat(formData.get('material'))
    };

    if (calcType === 'source') {
        data.ambientTemp = parseFloat(formData.get('ambientTemp'));
    } else {
        data.sourceTemp = parseFloat(formData.get('sourceTemp'));
    }

    fetch(`http://localhost:5000/calculate-${calcType}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('result').textContent = `Calculated ${calcType === 'source' ? 'Source' : 'Ambient'} Temperature: ${result.temperature} K`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
