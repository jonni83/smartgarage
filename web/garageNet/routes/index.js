var express = require('express');
var router = express.Router();
// var PythonShell = require('python-shell');

/* GET home page. */
router.get('/', function(req, res) {
  var options = {
    mode: 'text',
    pythonPath: 'python',
    pythonOptions: '',
    scriptPath: '',
    args: ''
  };
  var leftdoor = false;
  var rightdoor = true;
  var leftbay = false;
  var rightbay = true;

  // console.log("========== is the left door open =======")
  // client.invoke("isDoorOpen", "left", function(error, res, more) {
  //   console.log("left door open status is: " + res);
  //   res.locals.leftdoor = res;
  // });
  // 
  // console.log("========== is the right door open =======")
  // client.invoke("isDoorOpen", "right", function(error, res, more) {
  //   console.log("right door open status is: " + res);
  //   res.locals.rightdoor = res;
  // });
  // 
  // console.log("========== is the left bay occupied =======")
  // client.invoke("isBayOccupied", "left", function(error, res, more) {
  //   console.log("left bay status is: " + res);
  //   res.locals.leftbay = res;
  // });
  
  // console.log("========== is the right bay occupied =======")
  // client.invoke("isBayOccupied", "right", function(error, res, more) {
  //   console.log("right bay status is: " + res);
  //   res.locals.rightbay = res;
  // });
  //
  
  /* PythonShell.run('script.py', options, function(err, results) {
    if (err) throw err;
    console.log('results: %j', results);
  }); */

  // res.locals.leftdoor = leftdoor;
  // res.locals.rightdoor = rightdoor;
  // res.locals.leftbay = leftbay;
  // res.locals.rightbay = rightbay;
    
  // res.render('index', { title: 'Express' });
  res.render('index', { title: 'Express', leftdoor: leftdoor, rightdoor: rightdoor, leftbay: leftbay, rightbay: rightbay });
});

module.exports = router;
