# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: player.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cplayer.proto\x12\tmodels.db\x1a\x1egoogle/protobuf/wrappers.proto\"\xf7\x01\n\x06Player\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x19\n\x11player_first_name\x18\x02 \x01(\t\x12\x18\n\x10player_last_name\x18\x03 \x01(\t\x12*\n\x06\x63hases\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12)\n\x05\x62\x65\x61ts\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12)\n\x05keeps\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12)\n\x05seeks\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.BoolValueb\x06proto3')



_PLAYER = DESCRIPTOR.message_types_by_name['Player']
Player = _reflection.GeneratedProtocolMessageType('Player', (_message.Message,), {
  'DESCRIPTOR' : _PLAYER,
  '__module__' : 'player_pb2'
  # @@protoc_insertion_point(class_scope:models.db.Player)
  })
_sym_db.RegisterMessage(Player)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PLAYER._serialized_start=60
  _PLAYER._serialized_end=307
# @@protoc_insertion_point(module_scope)
