const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs')



// ####
const { exec } = require("child_process");

let ips;

exec("echo $(/sbin/ip -o -4 addr list | awk '{print $4}' | cut -d/ -f1)", (error, stdout, stderr) => {
    if (error) {
        console.log(`error: ${error.message}`);
        return;
    }
    if (stderr) {
        console.log(`stderr: ${stderr}`);
        return;
    }
    var out = stdout.trim()
    out = out.split(" ")
    // console.log(out)
    var obj = {
        "ip" : out
    }
    ips = obj;
    fs.writeFile('./ip.json', JSON.stringify(obj), err=>{
        if(!err){
            console.log('Created  IP.json');
        }
    })
    // console.log(`stdout: ${stdout}`);
});
// ####
const app = express();
app.use(express.static('./SupplySysLog'));

app.set('view engine', 'ejs')



const port = 5000;

app.get('/', (req, res)=>{
    res.sendFile(__dirname+'/SupplySysLog/SupplySys.html');
})


app.get('/ips', (req, res)=>{
    console.log(ips);
    res.send(JSON.stringify(ips))
})



app.listen(port, function () {
    console.log('Listening on port 5000');
})