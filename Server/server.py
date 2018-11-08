from concurrent import futures
import time
import sys
from queue import Queue

import grpc

import towercontrol_pb2
import towercontrol_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class TowerServicer(towercontrol_pb2_grpc.TowerServicer):

    def __init__(self,datos_aeropuertos,datos_torre,alturas,lista_aterrijaze,lista_despegue,lista_aterrizando,lista_despegando,queue_aterrizando,queue_despegando):
        datos_aeropuertos = datos_aeropuertos
        datos_torre = datos_torre
        self.alturas = alturas
        self.queue_aterrizando = queue_aterrizando
        self.queue_despegando = queue_despegando
        self.lista_aterrijaze = lista_aterrijaze
        self.lista_despegue = lista_despegue
        self.lista_despegando = lista_despegando
        self.lista_aterrizando = lista_aterrizando

    def SayLandingTrack(self, request, context):
        response = towercontrol_pb2.LandingTrackReply()
        self.alturas +=1
        response.altitude = self.alturas
        self.lista_aterrizando.append(("aterrizando",datos_torre['Ciudad'],request.flightnumber,request.destiny,track))
        print("Nuevo avion en el aeropuerto")
        print("Asignando pista de aterrizaje")
        if len(self.lista_aterrijaze) == 0:
            self.queue_aterrizando.put(request,True)
            response.pos = self.queue_aterrizando.qsize()
            print("entro")
            while(True):
                if len(self.lista_aterrijaze) != 0:
                    request = queue_aterrizando.get(True)
                    break
        else:
            response.pos = 0
        track = self.lista_aterrijaze.pop(0)
        time.sleep(5)
        print("La pista asignada es " + str(track))
        response.message = track
        self.lista_aterrijaze.append(track)
        self.lista_aterrizando.remove(("aterrizando",datos_torre['Ciudad'],request.flightnumber,request.destiny,track))           
        self.alturas-=1
        return response
    
    def SayDepartureTrack(self, request, context):
        response = towercontrol_pb2.DepartureTrackReply()
        self.alturas+=1
        response.height = self.alturas
        self.lista_despegando.append(("despegando",datos_torre['Ciudad'],request.flightnumber,request.destiny,track))
        print("Torre de control - " + datos_torre["Ciudad"] +"] Avion" + request.flightnumber + "quiere despegar")
        print("Consultando destino...")
        print("Enviando dirección de "+ request.destiny)
        print("Consultando restricciones de pasajeros y combustible")
        if len(lista_despegue) == 0:
            self.queue_despegando.put(request,True)
            response.pos = self.queue_despegando.qsize()
            print("entro")
            while(True):
                if len(lista_despegue) != 0:
                    request = queue_despegando.get(True)
                    break
        else:
            response.pos = 0
        track = self.lista_despegue.pop(0)
        time.sleep(5)
        response.track = track
        response.ip = datos_aeropuertos[request.destiny][0]
        response.port = datos_aeropuertos[request.destiny][1]
        print("La pista asignada a "+request.flightnumber+" es " + str(track) + " y la altura " + str(alturas))
        lista_despegue.append(track)
        self.lista_despegando.remove(("despegando",datos_torre['Ciudad'],request.flightnumber,request.destiny,track))
        self.alturas-=1
        return response

    def SayFlights(self, request, context):
        total_lists = self.lista_aterrizando + self.lista_despegando
        for element in total_lists:
            response = towercontrol_pb2.FlightsResponse()
            response.type = element[0]
            response.airport = element[1]
            response.flight = element[2]
            response.destiny = element[3]
            response.track = element[4]
            yield response 

datos_torre={}
datos_aeropuertos={}
host_base = 50051

try:
    print("Bienvenido a la torre de control")
    ciudad = str(input("[Torre de Control] Nombre del aeropuerto:"))
    datos_torre["Ciudad"]=ciudad
    cantidad_pistas_aterrijaze = int(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Cantidad de pistas de aterrizaje:"))
    datos_torre["Pistas_aterrizaje"] = cantidad_pistas_aterrijaze
    cantidad_pistas_despegue = int(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Cantidad de pistas de despegue:"))
    datos_torre["Pistas_despuegue"]=cantidad_pistas_despegue
    ip_torre = str(input("[Torre de Control] Ingrese IP del aeropuerto:"))
    port_torre = str(input("[Torre de Control] Ingrese el puerto:"))
    lista_aterrijaze = list(range(1,cantidad_pistas_aterrijaze + 1))
    lista_despegue = list(range(1,cantidad_pistas_despegue + 1))
    datos_aeropuertos[datos_torre["Ciudad"]] = (ip_torre,port_torre)
    queue_despegando = Queue()
    queue_aterrizando = Queue()
    lista_aterrizando = []
    lista_despegando = []
    alturas = 1
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    towercontrol_pb2_grpc.add_TowerServicer_to_server(
        TowerServicer(datos_aeropuertos,datos_torre,alturas,lista_aterrijaze,lista_despegue,lista_aterrizando,lista_despegando,queue_aterrizando,queue_despegando), server)
    server.add_insecure_port(ip_torre+':'+port_torre)
    server.start()
    flag = True
    while(flag):
        print("[Torre de Control - " + datos_torre["Ciudad"] + "] Para agregar destino presione enter, cualquier otra tecla para continuar")
        enter = sys.stdin.readline()
        if enter == '\n':
            ciudad = str(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Ingrese nombre y dirección IP:"))
            list_ciudad = ciudad.strip().split()
            port = str(input("[Torre de Control - " + datos_torre["Ciudad"] + "] Ingrese el puerto de la ciudad:"))
            datos_aeropuertos[" ".join(list_ciudad[:-1])]=(list_ciudad[-1],port)
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