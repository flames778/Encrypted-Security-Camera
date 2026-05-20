import sys
import os
from pathlib import Path
from config import FOOTAGE_DIR
from key_manager import get_or_create_key
from encrypt_chunk import decrypt_chunk

def main():
    if len(sys.argv) != 2:
        print("Usage: python batch_decrypt.py <output_merged.h264>")
        sys.exit(1)
        
    output_file = sys.argv[1]
    
    key = get_or_create_key()
    
    enc_files = sorted(FOOTAGE_DIR.glob("*.enc"))
    if not enc_files:
        print("No .enc files found in footage directory.")
        sys.exit(0)
        
    print(f"Found {len(enc_files)} chunks. Decrypting and merging...")
    
    with open(output_file, "wb") as out_f:
        for enc_file in enc_files:
            print(f"Processing {enc_file.name}...")
            with open(enc_file, "rb") as in_f:
                encrypted_data = in_f.read()
                
            try:
                plaintext = decrypt_chunk(encrypted_data, key)
                out_f.write(plaintext)
            except Exception as e:
                print(f"Failed to decrypt {enc_file.name}: {e}")
                
    print(f"Merge complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
