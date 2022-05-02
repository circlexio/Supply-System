// alert('hello');




const assignIP = (event) =>{
    axios.get('/ips').then(function (response) {
        ipa = response.data.ip[1]
        //Global elements
        var on = document.getElementById('systemon');
        var speed_I = document.getElementById('inputPumpSpeed');
        var speed_R = document.getElementById('recirculationPumpSpeed');
        var pressure_I = document.getElementById('inputPumpPressure');
        var pressure_R = document.getElementById('recirculationPumpPressure');
        var inkPump = document.getElementById('inkPump');


        //Socket Connection
        const socket = new WebSocket('ws://'+ ipa +':8015/');

        socket.addEventListener('open', (event)=>{
            socket.send('HTML client connected');
        })


        socket.addEventListener('message', (event)=>{
            console.log(event.data);
            data = JSON.parse(event.data)
            // console.log(typeof data);
            on.innerText = "SYSTEM : "+ data.machineState
            speed_I.innerText = "SPEED : " + data.inputPump
            speed_R.innerText = "SPEED : " + data.recirculationPump
            pressure_I.innerText = "PRESSURE :  " + data.inputPressure +" bar"
            pressure_R.innerText = "PRESSURE :  " + data.recirculationPressure +" bar"
            inkPump.innerText = "INK TANK : " + data.tankFull;

        })

    })

    
}
 

window.addEventListener('load', assignIP)
console.log(window.myParam);



