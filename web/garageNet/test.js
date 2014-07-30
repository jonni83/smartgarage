var PythonShell = require('python-shell');
var pyshell = new PythonShell('script.py');

pyshell.on('message', function(message) {
    console.log(message);
}
