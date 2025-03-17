import os
import numpy as np

def text_to_ascii(text):
    return [ord(char) for char in text]

def ascii_to_binary(ascii_list):
    return [format(num, '08b') for num in ascii_list]

def hamming_encode_block(data, block_size):
    n = block_size
    k = n - int(np.log2(n)) - 1  # Calculate number of parity bits
    encoded_blocks = []
    
    for i in range(0, len(data), k):
        block = list(data[i:i + k])
        while len(block) < k:
            block.append('0')  # Padding if needed
        
        encoded = list('0' * n)  # Placeholder for full encoded block
        
        j, parity_positions = 0, []
        for p in range(n):
            if (p + 1) & p == 0:  # Parity bit positions
                parity_positions.append(p)
            else:
                encoded[p] = block[j]
                j += 1
        
        for p in parity_positions:
            parity_value = 0
            for bit in range(n):
                if (bit + 1) & (p + 1) != 0:
                    parity_value ^= int(encoded[bit])
            encoded[p] = str(parity_value)
        
        encoded_blocks.append(''.join(encoded))
    
    return encoded_blocks

def introduce_single_bit_error(encoded_blocks):
    corrupted_blocks = []
    for block in encoded_blocks:
        block = list(block)
        error_pos = np.random.randint(0, len(block))
        block[error_pos] = '0' if block[error_pos] == '1' else '1'
        corrupted_blocks.append(''.join(block))
    return corrupted_blocks

def hamming_decode_block(encoded_blocks, block_size):
    decoded_bits = []
    for encoded in encoded_blocks:
        n = block_size
        k = n - int(np.log2(n)) - 1  # Original message length
        
        error_pos = 0
        for p in range(int(np.log2(n)) + 1):
            parity_value = 0
            for bit in range(n):
                if (bit + 1) & (2 ** p) != 0:
                    parity_value ^= int(encoded[bit])
            if parity_value != 0:
                error_pos += 2 ** p
        
        encoded = list(encoded)
        if error_pos > 0:
            encoded[error_pos - 1] = '0' if encoded[error_pos - 1] == '1' else '1'  # Correct error
        
        message = [encoded[i] for i in range(n) if (i + 1) & i != 0]
        decoded_bits.extend(message[:k])
    
    return decoded_bits

def binary_to_ascii(binary_list):
    return [chr(int(bits, 2)) for bits in binary_list]

def encode_text_file(input_file, output_file, block_size):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    ascii_codes = text_to_ascii(text)
    binary_data = ''.join(ascii_to_binary(ascii_codes))
    encoded_blocks = hamming_encode_block(binary_data, block_size)
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(encoded_blocks))

def decode_text_file(input_file, output_file, block_size, introduce_error=False):
    with open(input_file, 'r') as f:
        encoded_blocks = f.read().splitlines()
    
    if introduce_error:
        encoded_blocks = introduce_single_bit_error(encoded_blocks)
    
    decoded_bits = hamming_decode_block(encoded_blocks, block_size)
    
    binary_chunks = [''.join(decoded_bits[i:i+8]) for i in range(0, len(decoded_bits), 8)]
    decoded_text = ''.join(binary_to_ascii(binary_chunks))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decoded_text)

if __name__ == "__main__":
    block_size = int(input("Enter block size for Hamming encoding: "))
    encode_text_file("input.txt", "encoded.txt", block_size)
    decode_text_file("encoded.txt", "decoded.txt", block_size, introduce_error=True)
    print("Encoding, error introduction, and decoding complete. Check 'decoded.txt'.")
