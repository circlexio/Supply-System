alert('hello');

var on = document.getElementById('systemon');
var speed_I = document.getElementById('inputPumpSpeed');
var speed_R = document.getElementById('recirculationPumpSpeed');

var pressure_I = document.getElementById('inputPumpPressure');
var pressure_R = document.getElementById('recirculationPumpPressure');

const socket = new WebSocket('ws://localhost:8001');

socket.addEventListener('open', (event)=>{
    socket.send('HTML client connected');
})


socket.addEventListener('message', (event)=>{
    console.log(event.data);
    on.innerText = data.pumpOn
    speed_I.innerText = data.speedI
    speed_R.innerText = data.speedR
    pressure_I.innerText = data.pressureI
    pressure_R.innerText = data.pressureR

})


