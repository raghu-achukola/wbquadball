# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: season.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cseason.proto\x12\tmodels.db\x1a\x1fgoogle/protobuf/timestamp.proto\"\x86\x01\n\x07Ruleset\x12\x12\n\ngoal_value\x18\x01 \x01(\r\x12\x15\n\rfloor_minutes\x18\x02 \x01(\r\x12\x13\n\x0b\x63\x61tch_value\x18\x03 \x01(\r\x12#\n\x07\x65ndgame\x18\x04 \x01(\x0e\x32\x12.models.db.EndGame\x12\x16\n\x0e\x65ndgame_target\x18\x05 \x01(\r\"\xcc\x01\n\x06Season\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x11\n\tseason_id\x18\x02 \x01(\t\x12\x11\n\tleague_id\x18\x03 \x01(\t\x12\x35\n\x11season_start_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x33\n\x0fseason_end_date\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12#\n\x07ruleset\x18\x06 \x01(\x0b\x32\x12.models.db.Ruleset*Y\n\x07\x45ndGame\x12\x13\n\x0f\x45ND_GAME_UNKOWN\x10\x00\x12\x12\n\x0e\x45ND_GAME_CATCH\x10\x01\x12\x11\n\rEND_GAME_TIME\x10\x02\x12\x12\n\x0e\x45ND_GAME_SCORE\x10\x03\x62\x06proto3')

_ENDGAME = DESCRIPTOR.enum_types_by_name['EndGame']
EndGame = enum_type_wrapper.EnumTypeWrapper(_ENDGAME)
END_GAME_UNKOWN = 0
END_GAME_CATCH = 1
END_GAME_TIME = 2
END_GAME_SCORE = 3


_RULESET = DESCRIPTOR.message_types_by_name['Ruleset']
_SEASON = DESCRIPTOR.message_types_by_name['Season']
Ruleset = _reflection.GeneratedProtocolMessageType('Ruleset', (_message.Message,), {
  'DESCRIPTOR' : _RULESET,
  '__module__' : 'season_pb2'
  # @@protoc_insertion_point(class_scope:models.db.Ruleset)
  })
_sym_db.RegisterMessage(Ruleset)

Season = _reflection.GeneratedProtocolMessageType('Season', (_message.Message,), {
  'DESCRIPTOR' : _SEASON,
  '__module__' : 'season_pb2'
  # @@protoc_insertion_point(class_scope:models.db.Season)
  })
_sym_db.RegisterMessage(Season)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ENDGAME._serialized_start=404
  _ENDGAME._serialized_end=493
  _RULESET._serialized_start=61
  _RULESET._serialized_end=195
  _SEASON._serialized_start=198
  _SEASON._serialized_end=402
# @@protoc_insertion_point(module_scope)
