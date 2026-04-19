import sys

def rc4_encrypt_decrypt(key: bytes, data: bytes) -> bytes:
    """
    RC4 Stream Cipher implementation.
    The same function is used for both encryption and decryption.
    """
    
    # 1. Initialization: Create S array (0 to 255)
    S = list(range(256))
    key_length = len(key)
    
    # 2. Key-Scheduling Algorithm (KSA)
    j = 0
    for i in range(256):
        # j = (j + S[i] + key[i mod key_length]) mod 256
        j = (j + S[i] + key[i % key_length]) % 256
        # Swap S[i] and S[j]
        S[i], S[j] = S[j], S[i]

    # 3. Pseudo-Random Generation Algorithm (PRGA) and Encryption
    i = 0
    j = 0
    keystream_byte = 0
    output = bytearray()

    for data_byte in data:
        # Increment i and j
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        
        # Swap S[i] and S[j]
        S[i], S[j] = S[j], S[i]
        
        # Get keystream byte (t = (S[i] + S[j]) mod 256)
        t = (S[i] + S[j]) % 256
        keystream_byte = S[t]
        
        # XOR data byte with keystream byte
        encrypted_byte = data_byte ^ keystream_byte
        output.append(encrypted_byte)

    return bytes(output)

# --- Demonstration ---
# The key and data must be in 'bytes' format
SECRET_KEY = b"MySecretRC4Key"
PLAINTEXT  = b"Attack at dawn on Monday, October 24."

print(f"Original Text: {PLAINTEXT.decode()}")

# Encryption
CIPHERTEXT = rc4_encrypt_decrypt(SECRET_KEY, PLAINTEXT)
print(f"Encrypted (Hex): {CIPHERTEXT.hex()}")

# Decryption (Using the same function and key)
DECRYPTED_TEXT = rc4_encrypt_decrypt(SECRET_KEY, CIPHERTEXT)
print(f"Decrypted Text: {DECRYPTED_TEXT.decode()}")