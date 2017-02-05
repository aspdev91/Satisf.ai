//start.js
var spawn = require('child_process').spawn,
    py    = spawn('python', ['seamlessOrder.py']),
    data = {'restaurant':'Homemade Taqueria'},
    dataString = '';

py.stdout.on('data', function(data){
  dataString += data.toString();
});

py.stdout.on('end', function(){
  console.log('Sum of numbers=',dataString);
});

py.stdin.write(JSON.stringify(data));
py.stdin.end();