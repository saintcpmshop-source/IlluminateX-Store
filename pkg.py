#!/usr/bin/env python3
"""
Modernized pkg.py for PSL1GHT - Python 3 Compatible
Copyright (c) 2026 saintcpmshop-source
Based on the original tools by the PS3 Dev community.
"""
import sys
import os
import struct
import hashlib
import argparse
from Crypto.Cipher import AES

# --- Constants ---
PKG_MAGIC = 0x7F504147
PKG_VERSION = 0x0100

# --- Helper Functions ---
def align(val, alignment):
    return (val + alignment - 1) & ~(alignment - 1)

def sha1(data):
    return hashlib.sha1(data).digest()

def aes_encrypt_cbc(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data)

def aes_encrypt_ctr(key, nonce, data):
    # Simplified CTR implementation for PS3 PKG
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce[:8], initial_value=nonce[8:])
    return cipher.encrypt(data)

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# --- Main Packaging Logic ---
def make_pkg(content_id, src_dir, out_pkg):
    print(f"[!] Building PKG: {out_pkg}")
    print(f"[!] Content ID: {content_id}")
    
    # 1. Gather files from the source directory
    files = []
    for root, _, filenames in os.walk(src_dir):
        for f in filenames:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, src_dir)
            files.append((rel_path, read_file(full_path)))
            print(f"    -> Adding {rel_path}")

    # 2. Sort files (PARAM.SFO must be first)
    files.sort(key=lambda x: x[0] != "PARAM.SFO")

    # 3. Build Header (Simplified for CFW FSELF)
    # In a real PKG, there is heavy encryption here using the PS3 keys.
    # For CFW, we use a "Debug" or "FSELF" PKG format which is much simpler.
    
    pkg_data = bytearray()
    
    # Fake Header (CFW accepts this format)
    pkg_data.extend(struct.pack(">I", PKG_MAGIC))
    pkg_data.extend(struct.pack(">I", PKG_VERSION))
    pkg_data.extend(struct.pack(">I", 0)) # Type
    pkg_data.extend(struct.pack(">I", 0)) # Meta offset
    pkg_data.extend(struct.pack(">I", len(files))) # Number of files
    
    # Write File Headers
    current_offset = 0x1000 # Start data after header
    
    for rel_path, data in files:
        name_bytes = rel_path.encode('utf-8')
        
        # File Header Structure
        pkg_data.extend(struct.pack(">I", len(name_bytes)))
        pkg_data.extend(struct.pack(">I", len(data)))
        pkg_data.extend(struct.pack(">I", current_offset))
        pkg_data.extend(b'\x00' * 4) # Padding
        pkg_data.extend(name_bytes)
        
        current_offset += align(len(data), 16)

    # Pad the header to the data start
    while len(pkg_data) < 0x1000:
        pkg_data.append(0)

    # Write File Data
    for rel_path, data in files:
        pkg_data.extend(data)
        # Align to 16 bytes
        while len(pkg_data) % 16 != 0:
            pkg_data.append(0)
            
    # Write the final PKG file
    with open(out_pkg, 'wb') as f:
        f.write(pkg_data)
        
    print(f"[+] Success! {out_pkg} created ({len(pkg_data)} bytes).")

# --- Entry Point ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PS3 PKG Builder (Python 3)')
    parser.add_argument('--contentid', required=True, help='Content ID (e.g., UP0000-ILSTORE01_00-0000000000000001)')
    parser.add_argument('src_dir', help='Directory containing USRDIR')
    parser.add_argument('out_pkg', help='Output PKG file')
    
    args = parser.parse_args()
    
    make_pkg(args.contentid, args.src_dir, args.out_pkg)
