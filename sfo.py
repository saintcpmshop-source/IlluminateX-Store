#!/usr/bin/env python3
import sys
import struct

def parse_sfo_txt(input_file):
    entries = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                entries.append((key.strip(), value.strip()))
    return entries

def format_sfo(output_file, entries):
    header_fmt = '<4sIIII'
    header_size = struct.calcsize(header_fmt)
    key_table = b''
    data_table = b''
    index_table = b''
    data_offset = 0
    
    for key, value in entries:
        key_bytes = key.encode('utf-8') + b'\x00'
        val_bytes = value.encode('utf-8') + b'\x00'
        while len(val_bytes) % 4 != 0:
            val_bytes += b'\x00'
        data_fmt = 0x0204 
        index_entry = struct.pack('<HHIII', len(key_table), data_fmt, len(value)+1, len(val_bytes), data_offset)
        key_table += key_bytes
        data_table += val_bytes
        index_table += index_entry
        data_offset += len(val_bytes)

    key_table_start = header_size + len(index_table)
    data_table_start = key_table_start + len(key_table)
    
    with open(output_file, 'wb') as f:
        f.write(struct.pack(header_fmt, b'\x00PSF', 0x101, key_table_start, data_table_start, len(entries)))
        f.write(index_table)
        f.write(key_table)
        f.write(data_table)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = input_file.replace('.txt', '')
    entries = parse_sfo_txt(input_file)
    format_sfo(output_file, entries)
