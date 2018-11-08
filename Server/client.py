from concurrent import futures
import time
import sys

import grpc

import towercontrol_pb2
import towercontrol_pb2_grpc

nombre_aerolinea = ""
nombre_vuelo = ""
ip_conexion = ""
destino = ""
peso = 0
carga_combustible = 0
altura_establecida = 0

print("Bienvenido al vuelo")
avion = str(input("[Avion] Nombre de la aerolinea y numero de avion:"))
avion = avion.strip().split()
nombre_aerolinea = avion[0]
nombre_vuelo = avion[1]
peso = int(input("[Avion - " + nombre_vuelo + "] Peso maximo carga [Kg]:"))
carga_combustible = int(input("[Avion - " + nombre_vuelo + "] Capacidad del tanque de combustible [L]:"))
ip = str(input("[Avion - "+ nombre_vuelo + "] Torre de control inicial:"))
port = str(input("[Avion - "+ nombre_vuelo + "] Ingrese el puerto:"))
ip_conexion = ip+':'+port
flag = True
while(flag):
    channel = grpc.insecure_channel(ip_conexion)
    stub = towercontrol_pb2_grpc.TowerStub(channel)
    print("[Avion - " + nombre_vuelo + "] Para despegar presione enter, cualquier otra tecla para apagar motores")
    enter = sys.stdin.readline()
    if enter == '\n':
        ciudad_destino = str(input("[Avion - " + nombre_vuelo + "] Ingrese destino:"))
        request_departure = towercontrol_pb2.DepartureTrackRequest(
        flightnumber=nombre_vuelo,destiny=ciudad_destino)
        response = stub.SayDepartureTrack(request_departure)
        print("Estamos en la posición de espera "+str(response.pos))
        print("La pista de despegue es "+str(response.track)+" y la altitud es: "+str(response.height))
        altura_establecida = response.height
        print("Volando al destino....")
        time.sleep(10)
        ip = response.ip
        port = response.port
        ip_conexion = str(ip) + ':' + str(port)
        channel = grpc.insecure_channel(ip_conexion)
        stub = towercontrol_pb2_grpc.TowerStub(channel)
        request_landing = towercontrol_pb2.LandingTrackRequest(
            track=1,
            altitude=altura_establecida
        )
        response = stub.SayLandingTrack(request_landing)
        print("Esperando pista de aterrizaje... nuestra posición en la lista es "+str(response.pos))
        print("La pista asignada es la "+str(response.message)+ " con altura "+str(response.altitude))
    else:
        print("Apagando motores...")
        flag = False


# et voilà
    print(response.message)