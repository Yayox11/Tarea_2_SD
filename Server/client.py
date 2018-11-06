from concurrent import futures
import time

import grpc

import towercontrol_pb2
import towercontrol_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = towercontrol_pb2_grpc.TowerStub(channel)

# create a valid request message
number = towercontrol_pb2.AltitudeRequest(altitude=6969)

# make the call
response = stub.SayAltitude(number)

# et voilà
print(response.message)