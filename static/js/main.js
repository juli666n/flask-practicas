const form = document.querySelector('#save_plant');
const opt = document.querySelector('#plant');
const sensor = document.querySelector('#sensor');

async function drawOption(){
    let plants = await getPlants();
    let template_option = '';

    template_option += `<option selected value='default'>Seleccione planta</option>`;

    plants.forEach(plant => {
        template_option += `
            <option value="${plant.id}">${plant.name}</option>
        `;
    });

    opt.innerHTML = template_option;
}

let name = '';

opt.addEventListener('change', (event) => {
    let item = event.target;
    name = item.options[item.selectedIndex].text;
});

async function drawTable() {
    let sensors = await getSensor();
    let template_sensor = '';


    sensors.forEach(sensor => {
        template_sensor += `
            <tr>
                <td>${name}</td>
                <td>${sensor.temperature}</td>
                <td>${sensor.moisture}</td>
                <td>${sensor.lux}</td>
            </tr>
        `;
    });

    sensor.innerHTML = template_sensor;
}

async function getPlants() {
    const response = await fetch('/api/plants');
    return await response.json();
}

async function getSensor() {
    const response = await fetch('/api/sensors');
    return await response.json();
}


form.addEventListener('submit', (evt) => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    const id= formData.get('plant');

    if (id !== 'default') {
        fetch(`/api/plants/${id}`, {
            method: 'POST',
            body: JSON.stringify({
                is_selected: 1
            }),
            headers:{
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                alert(`${data}`);
                drawTable();
            });
    } else {
       alert("Seleccione una planta");
    }

});

window.setInterval(async () => {
    await drawTable();
}, 1500);

document.addEventListener("DOMContentLoaded", ()=>{
    drawOption();
    drawTable();
});
