# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: statsheet.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fstatsheet.proto\x12\x10models.statsheet\"|\n\x13StatSheetPossession\x12\x10\n\x08\x65nd_time\x18\x01 \x01(\t\x12\x0f\n\x07offense\x18\x02 \x01(\t\x12\x0e\n\x06\x65xtras\x18\x03 \x01(\t\x12\x0e\n\x06result\x18\x04 \x01(\t\x12\x0f\n\x07primary\x18\x05 \x01(\t\x12\x11\n\tsecondary\x18\x06 \x01(\tb\x06proto3')



_STATSHEETPOSSESSION = DESCRIPTOR.message_types_by_name['StatSheetPossession']
StatSheetPossession = _reflection.GeneratedProtocolMessageType('StatSheetPossession', (_message.Message,), {
  'DESCRIPTOR' : _STATSHEETPOSSESSION,
  '__module__' : 'statsheet_pb2'
  # @@protoc_insertion_point(class_scope:models.statsheet.StatSheetPossession)
  })
_sym_db.RegisterMessage(StatSheetPossession)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STATSHEETPOSSESSION._serialized_start=37
  _STATSHEETPOSSESSION._serialized_end=161
# @@protoc_insertion_point(module_scope)