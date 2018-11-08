var messages = require('./towercontrol_pb');
var services = require('./towercontrol_grpc_pb');

var grpc = require('grpc');

function main() {
  var client = new services.TowerClient('192.168.1.87:50051', grpc.credentials.createInsecure());
  var request = new messages.FlightsRequest();
  request.setMessage("");
  console.log('Greeting:');
  var call = client.sayFlights(request);
  call.on('data', function(feature){
    console.log(feature.airport)
    console.log(feature.type)
    console.log(feature.flight)
    console.log(feature.destiny)
  });

  call.on('end', function(){
  });
  call.on('error', function(e) {
    // An error has occurred and the stream has been closed.
  });
}
main();