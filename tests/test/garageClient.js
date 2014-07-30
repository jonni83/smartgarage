var zerorpc = require("zerorpc");

var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

console.log("========== let's say hello World! =======")
client.invoke("hello", "World!", function(error, res, more) {
	console.log(res);
});

console.log("========== is the left door open =======")
client.invoke("isDoorOpen", "left", function(error, res, more) {
	console.log("left door open status is: " + res);
});

console.log("========== is the right door open =======")
client.invoke("isDoorOpen", "right", function(error, res, more) {
	console.log("right door open status is: " + res);
});

console.log("========== is the left bay occupied =======")
client.invoke("isBayOccupied", "left", function(error, res, more) {
	console.log("left bay status is: " + res);
});

// console.log("========== is the right bay occupied =======")
// client.invoke("isBayOccupied", "right", function(error, res, more) {
// 	console.log("right bay status is: " + res);
// });
// 
