this_dir = File.expand_path(File.dirname(__FILE__))
$LOAD_PATH.unshift(this_dir) unless $LOAD_PATH.include?(this_dir)

require 'grpc'
require 'towercontrol_pb'
require 'towercontrol_services_pb'

nombre_aerolinea = ""
nombre_vuelo = ""
ip_conexion = ""
destino = ""
peso = 0
carga_combustible = 0
altura_establecida = 0
def main
    p "Bienvenido al vuelo"
    print "[Avion] Nombre de la aerolinea y numero de avion:"
    avion  = gets
    avion = avion.chomp.split()
    nombre_aerolinea = avion[0]
    nombre_vuelo = avion[1]
    print "[Avion - " + nombre_vuelo + "] Peso maximo carga [Kg]:"
    peso = gets.to_i
    print "[Avion - " + nombre_vuelo + "] Capacidad del tanque de combustible [L]:"
    carga_combustible = gets.to_i
    print "[Avion - "+ nombre_vuelo + "] Torre de control inicial:"
    ip = gets.chomp
    print "[Avion - "+ nombre_vuelo + "] Puerto:"
    puerto = gets.chomp
    ip_conexion = ip + ":" + puerto
    p "ip conexion: #{ip_conexion}"

    flag = TRUE 

    while flag 
        stub = Towercontrol::Tower::Stub.new(ip_conexion, :this_channel_is_insecure)
        p "[Avion - " + nombre_vuelo + "] Para despegar presione enter, cualquier otra tecla para apagar motores"
        enter = gets
        if enter == "\n"
            print "[Avion - " + nombre_vuelo + "] Ingrese destino:" 
            ciudad_destino = gets.chomp
            msg = stub.say_departure_track(Towercontrol::DepartureTrackRequest.new(flightnumber: nombre_vuelo, destiny: ciudad_destino))
            p "Estamos en la posicion de espera #{msg.pos}"
            p "La pista de despegue es #{msg.track}  y la altitud es #{msg.height}"
            altura_establecida = msg.height
            p "Volando al destino ..."
            sleep(10)
            ip = msg.ip
            port = msg.port
            ip_conexion = ip + ":" + port
            stub = Towercontrol::Tower::Stub.new(ip_conexion, :this_channel_is_insecure)
            msg2 = stub.say_landing_track(Towercontrol::LandingTrackRequest.new(track: 1 , altitude: altura_establecida))
            p "Esperando aterrizaje... nuestra posicion en la lista es #{msg2.pos}"
            p "La pista asignada es la #{msg2.message} con altura #{msg2.altitude}"
        else
            p "Apagando motores..."
            flag = FALSE
        end 

    end 
    #stub = Towercontrol::Tower::Stub.new('10.6.43.139:50051', :this_channel_is_insecure)
    #message = stub.say_altitude(Towercontrol::AltitudeRequest.new(altitude: 6969)).message
    p "Reponse: #{message}"
end 
main