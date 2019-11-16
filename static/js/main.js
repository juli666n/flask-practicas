window.onload = () => {
    draw();
}

const form = document.querySelector('#save_plant');
const opt = document.querySelector('#configSave');
const sensor = document.querySelector('#sensor');



async function draw() {

    let {plants} = await getPlants();
    let {sensors} = await getPlants();
    console.log(plants);


    let template_sensor = '';
    let template_option = '';

    template_option += `<option selected value='default'>Seleccione planta</option>`;

    plants.forEach(plant => {
        template_option += `
            <option value="${plant.id}">${plant.name}</option>
        `;
    });

    opt.innerHTML = template_option;

    sensors.forEach(sensor => {
        template_sensor += `
            <tr>
                <td>${sensor.temperarure}</td>
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

form.addEventListener('submit', (evt) => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    const val = {
        plantId: formData.get('plantId')
    };

    if (val.plantId !== 'default') {
        fetch('/api/plants', {
            method: 'POST',
            body: JSON.stringify(val),
            headers:{
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                alert(data.msg);
                draw();
            });
    } else {
        alert("Seleccione una planta");
    }

});

