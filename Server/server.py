from concurrent import futures
import time
import sys

import grpc

import towercontrol_pb2
import towercontrol_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class TowerServicer(towercontrol_pb2_grpc.TowerServicer):

    def __init__(self,cola,datos_aeropuertos,datos_torre,alturas,host_base):
        cola = cola
        datos_aeropuertos = datos_aeropuertos
        datos_torre = datos_torre
        alturas = alturas
        host_base = host_base

    def SayAltitude(self, request, context):
        response = towercontrol_pb2.AltitudeReply()
        response.message = request.altitude
        return response

    def SayLandingTrack(self, request, context):
        print("Nuevo avion en el aeropuerto")
        print("Asignando pista de aterrizaje")
        print("La pista asignada es la 1")
        response = towercontrol_pb2.LandingTrackReply()
        response.message = 1
        alturas.add(request.altitude)
        print(alturas)           
        return response
    
    def SayDepartureTrack(self, request, context):
        response = towercontrol_pb2.DepartureTrackReply()
        print("Torre de control - " + datos_torre["Ciudad"] +"] Avion" + request.flightnumber + "quiere despegar")
        print("Consultando destino...")
        print("Enviando dirección de "+ request.destiny)
        print("Consultando restricciones de pasajeros y combustible")
        print("La pista asignada a "+request.flightnumber+" es la 2 y altura 5")
        response.track = 2
        len_alturas = len(list(alturas))
        if len_alturas == 0:
            response.height = 1
            alturas.add(1)
        else:
            lista = list(alturas)
            iters = 0
            for i in range(len(lista) -1):
                iters+=1
                if lista[i+1] - lista[i] > 1:
                    response.height = lista[i]+1
                    alturas.add(lista[i]+1)
            if iters + 1 == len(lista):
                response.height = lista[-1]+1
                alturas.add(lista[-1]+1)
        response.ip = datos_aeropuertos[request.destiny]
        print(alturas)
        return response

    def SayIpRequest(self, request, context):
        return towercontrol_pb2.IpReply(altitude=1000,ip="10.0.0.1")

cola = []
datos_torre={}
datos_aeropuertos={}
alturas = set()
host_base = 50051

try:
    print("Bienvenido a la torre de control")
    ciudad = str(input("[Torre de Control] Nombre del aeropuerto:"))
    datos_torre["Ciudad"]=ciudad
    cantidad_pistas_aterrijaze = int(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Cantidad de pistas de aterrizaje:"))
    datos_torre["Pistas_aterrizaje"] = cantidad_pistas_aterrijaze
    cantidad_pistas_despuegue = int(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Cantidad de pistas de despegue:"))
    datos_torre["Pistas_despuegue"]=cantidad_pistas_despuegue
    ip = str(input("[Torre de Control] Ingrese IP del aeropuerto:"))
    datos_aeropuertos[datos_torre["Ciudad"]] = ip
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    towercontrol_pb2_grpc.add_TowerServicer_to_server(TowerServicer(cola,datos_aeropuertos,datos_torre,alturas,host_base), server)
    values = sum(map(int,ip.strip().split('.')))
    print(ip+':'+str(host_base+values))
    server.add_insecure_port("10.6.43.139"+':'+str(host_base+values))
    server.start()
    flag = True
    while(flag):
        print("[Torre de Control - " + datos_torre["Ciudad"] + "] Para agregar destino presione enter, cualquier otra tecla para continuar")
        enter = sys.stdin.readline()
        if enter == '\n':
            ciudad = str(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Ingrese nombre y dirección IP:"))
            list_ciudad = ciudad.strip().split()
            datos_aeropuertos[" ".join(list_ciudad[:-1])]=list_ciudad[-1]
            print(datos_aeropuertos.items())
        else:
            print("Aeropuertos añadidos")
            flag=False
            print(datos_aeropuertos.items())
    while True:
        time.sleep(_ONE_DAY_IN_SECONDS)
        print("pico")
except KeyboardInterrupt:
    server.stop(0)