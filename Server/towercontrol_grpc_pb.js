// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var towercontrol_pb = require('./towercontrol_pb.js');

function serialize_towercontrol_DepartureTrackReply(arg) {
  if (!(arg instanceof towercontrol_pb.DepartureTrackReply)) {
    throw new Error('Expected argument of type towercontrol.DepartureTrackReply');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_towercontrol_DepartureTrackReply(buffer_arg) {
  return towercontrol_pb.DepartureTrackReply.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_towercontrol_DepartureTrackRequest(arg) {
  if (!(arg instanceof towercontrol_pb.DepartureTrackRequest)) {
    throw new Error('Expected argument of type towercontrol.DepartureTrackRequest');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_towercontrol_DepartureTrackRequest(buffer_arg) {
  return towercontrol_pb.DepartureTrackRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_towercontrol_FlightsRequest(arg) {
  if (!(arg instanceof towercontrol_pb.FlightsRequest)) {
    throw new Error('Expected argument of type towercontrol.FlightsRequest');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_towercontrol_FlightsRequest(buffer_arg) {
  return towercontrol_pb.FlightsRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_towercontrol_FlightsResponse(arg) {
  if (!(arg instanceof towercontrol_pb.FlightsResponse)) {
    throw new Error('Expected argument of type towercontrol.FlightsResponse');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_towercontrol_FlightsResponse(buffer_arg) {
  return towercontrol_pb.FlightsResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_towercontrol_LandingTrackReply(arg) {
  if (!(arg instanceof towercontrol_pb.LandingTrackReply)) {
    throw new Error('Expected argument of type towercontrol.LandingTrackReply');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_towercontrol_LandingTrackReply(buffer_arg) {
  return towercontrol_pb.LandingTrackReply.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_towercontrol_LandingTrackRequest(arg) {
  if (!(arg instanceof towercontrol_pb.LandingTrackRequest)) {
    throw new Error('Expected argument of type towercontrol.LandingTrackRequest');
  }
  return new Buffer(arg.serializeBinary());
}

function deserialize_towercontrol_LandingTrackRequest(buffer_arg) {
  return towercontrol_pb.LandingTrackRequest.deserializeBinary(new Uint8Array(buffer_arg));
}


// The greeting service definition.
var TowerService = exports.TowerService = {
  sayLandingTrack: {
    path: '/towercontrol.Tower/SayLandingTrack',
    requestStream: false,
    responseStream: false,
    requestType: towercontrol_pb.LandingTrackRequest,
    responseType: towercontrol_pb.LandingTrackReply,
    requestSerialize: serialize_towercontrol_LandingTrackRequest,
    requestDeserialize: deserialize_towercontrol_LandingTrackRequest,
    responseSerialize: serialize_towercontrol_LandingTrackReply,
    responseDeserialize: deserialize_towercontrol_LandingTrackReply,
  },
  sayDepartureTrack: {
    path: '/towercontrol.Tower/SayDepartureTrack',
    requestStream: false,
    responseStream: false,
    requestType: towercontrol_pb.DepartureTrackRequest,
    responseType: towercontrol_pb.DepartureTrackReply,
    requestSerialize: serialize_towercontrol_DepartureTrackRequest,
    requestDeserialize: deserialize_towercontrol_DepartureTrackRequest,
    responseSerialize: serialize_towercontrol_DepartureTrackReply,
    responseDeserialize: deserialize_towercontrol_DepartureTrackReply,
  },
  sayFlights: {
    path: '/towercontrol.Tower/SayFlights',
    requestStream: false,
    responseStream: true,
    requestType: towercontrol_pb.FlightsRequest,
    responseType: towercontrol_pb.FlightsResponse,
    requestSerialize: serialize_towercontrol_FlightsRequest,
    requestDeserialize: deserialize_towercontrol_FlightsRequest,
    responseSerialize: serialize_towercontrol_FlightsResponse,
    responseDeserialize: deserialize_towercontrol_FlightsResponse,
  },
};

exports.TowerClient = grpc.makeGenericClientConstructor(TowerService);
