this_dir = File.expand_path(File.dirname(__FILE__))
$LOAD_PATH.unshift(this_dir) unless $LOAD_PATH.include?(this_dir)

require 'grpc'
require 'towercontrol_pb'
require 'towercontrol_services_pb'
def main
    stub = Towercontrol::Tower::Stub.new('10.6.43.139:50051', :this_channel_is_insecure)
    message = stub.say_altitude(Towercontrol::AltitudeRequest.new(altitude: 6969)).message
    p "Reponse: #{message}"
end 
main