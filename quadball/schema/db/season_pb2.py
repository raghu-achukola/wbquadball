# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: season.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cseason.proto\x12\tmodels.db\x1a\x1fgoogle/protobuf/timestamp.proto\"\x9a\x01\n\x06Season\x12\x11\n\tseason_id\x18\x01 \x01(\t\x12\x11\n\tleague_id\x18\x02 \x01(\t\x12\x35\n\x11season_start_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x33\n\x0fseason_end_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestampb\x06proto3')



_SEASON = DESCRIPTOR.message_types_by_name['Season']
Season = _reflection.GeneratedProtocolMessageType('Season', (_message.Message,), {
  'DESCRIPTOR' : _SEASON,
  '__module__' : 'season_pb2'
  # @@protoc_insertion_point(class_scope:models.db.Season)
  })
_sym_db.RegisterMessage(Season)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SEASON._serialized_start=61
  _SEASON._serialized_end=215
# @@protoc_insertion_point(module_scope)
