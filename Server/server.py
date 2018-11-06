from concurrent import futures
import time
import sys

import grpc

import towercontrol_pb2
import towercontrol_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class TowerServicer(towercontrol_pb2_grpc.TowerServicer):

    def __init__(self,cola,datos_aeropuertos,datos_torre):
        cola = cola
        datos_aeropuertos = datos_aeropuertos
        datos_torre = datos_torre

    def SayAltitude(self, request, context):
        response = towercontrol_pb2.AltitudeReply()
        response.message = request.altitude
        return response

    def SayLandingTrack(self, request, context):
        response = towercontrol_pb2.LandingTrackReply()
        if len(self.cola) == datos_torre["Pistas_aterrizaje"]:
            response.message = 0
        elif len(self.cola) < datos_torre["Pistas_aterrizaje"]:
            response.message = 1            
        return response
    
    def SayDepartureTrack(self, request, context):
        response = towercontrol_pb2.DepartureTrackReply()
        print("Torre de control - " + datos_torre["Ciudad"] +"] Avion" + request.flightnumber + "quiere despegar")
        print("Consultando destino...")
        print("Enviando dirección de "+ request.destiny)
        print("Consultando restricciones de pasajeros y combustible")
        print("La pista asignada a "+request.flightnumber+" es la 2 y altura 5")
        response.track = 2
        response.height = 5
        return response

    def SayIpRequest(self, request, context):
        return towercontrol_pb2.IpReply(altitude=1000,ip="10.0.0.1")

cola = []
datos_torre={}
datos_aeropuertos={}
alturas = set()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
towercontrol_pb2_grpc.add_TowerServicer_to_server(TowerServicer(cola,datos_aeropuertos,datos_torre), server)
server.add_insecure_port('[::]:50051')
server.start()
try:
    print("Bienvenido a la torre de control")
    ciudad = str(input("[Torre de Control] Nombre del aeropuerto:"))
    datos_torre["Ciudad"]=ciudad
    cantidad_pistas_aterrijaze = int(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Cantidad de pistas de aterrizaje:"))
    datos_torre["Pistas_aterrizaje"] = cantidad_pistas_aterrijaze
    cantidad_pistas_despuegue = int(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Cantidad de pistas de despegue:"))
    datos_torre["Pistas_despuegue"]=cantidad_pistas_despuegue
    datos_aeropuertos[datos_torre["Ciudad"]] = ("10.0.0.1",50051)
    print("El aeropuerto de "+datos_torre["Ciudad"]+"tiene por IP 10.0.0.1")
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