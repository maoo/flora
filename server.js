const express = require('express')
const path = require('path');
const app = express()
const Tail = require('tail').Tail;
const tail = new Tail("data/flora.csv");
var http = require('http').createServer(app);
var io = require('socket.io').listen(http);
app.use(express.static('public'));

const port = 3000

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});

tail.on("line", function(data) {
    console.log("new line!",data);
    io.emit('new data', data);
});
tail.on("error", function(error) {
  console.log('ERROR: ', error);
});

io.on('connection', function(socket){
    socket.on('new data', function(msg){
        io.emit('new data', msg);
    });
});

http.listen(port, () => console.log(`flora running on port ${port}!`))