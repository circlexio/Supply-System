const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(express.static('./SupplySysLog'));

app.set('view engine', 'ejs')



const port = 5000;

app.get('/', (req, res)=>{
    res.sendFile(__dirname+'/SupplySysLog/SupplySys.html');
})




app.listen(port, function () {
    console.log('Listening on port 5000');
})