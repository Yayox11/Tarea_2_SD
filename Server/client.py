from concurrent import futures
import time

import grpc

import towercontrol_pb2
import towercontrol_pb2_grpc

nombre_aerolinea = 'LAN'
nombre_vuelo = "CAB45"
torre_inicial = "1.0.0.1"
destino = "Sao Paulo"

channel = grpc.insecure_channel('localhost:50051')
stub = towercontrol_pb2_grpc.TowerStub(channel)

request_departure = towercontrol_pb2.DepartureTrackRequest(
    airline=nombre_aerolinea,flightnumber=nombre_vuelo,initialtower=torre_inicial,destiny=destino)
response = stub.SayDepartureTrack(request_departure)

##number = towercontrol_pb2.AltitudeRequest(altitude=6969)
##response = stub.SayAltitude(number)

# et voilà
print(response.track,response.height)