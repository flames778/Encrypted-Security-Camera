import sys
import os
from config import KEY_FILE
from key_manager import get_or_create_key
from encrypt_chunk import decrypt_chunk

def main():
    if len(sys.argv) != 3:
        print("Usage: python decrypt.py <input.enc> <output.h264>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        sys.exit(1)
        
    key = get_or_create_key()
    
    with open(input_file, "rb") as f:
        encrypted_data = f.read()
        
    try:
        plaintext = decrypt_chunk(encrypted_data, key)
    except Exception as e:
        print(f"Decryption failed: {e}")
        sys.exit(1)
        
    with open(output_file, "wb") as f:
        f.write(plaintext)
        
    print(f"Successfully decrypted to {output_file}")

if __name__ == "__main__":
    main()
