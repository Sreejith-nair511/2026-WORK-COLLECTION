# A simple simulation using standard Python lists and integers.
# In a real C program, these variables would be stored contiguously in memory.

def buffer_overflow_concept():
    # 1. Define the "memory layout"
    BUFFER_SIZE = 5
    
    # The 'buffer' list is a fixed size (simulating a C array)
    buffer = [0] * BUFFER_SIZE  # e.g., [0, 0, 0, 0, 0]

    # The 'important_value' is logically adjacent to the buffer
    important_value = 0xDEADBEEF  # A critical value (like a return address)

    print(f"Initial State:")
    print(f"  Buffer: {buffer}")
    print(f"  Important Value: 0x{important_value:X}")
    print("-" * 30)

    # 2. Attempt a "safe" write (input fits)
    safe_input = [1, 2, 3]
    print(f"Attempting Safe Write (Length {len(safe_input)}):")
    
    # Simulate writing only up to the buffer size
    for i in range(min(len(safe_input), BUFFER_SIZE)):
        buffer[i] = safe_input[i]

    print(f"  Buffer: {buffer}")
    print(f"  Important Value: 0x{important_value:X} (Unchanged)")
    print("-" * 30)

    # 3. Attempt an "unsafe" write (input overflows)
    # The input has 8 elements, which is 3 more than BUFFER_SIZE (5)
    overflow_input = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x01, 0x02] 
    
    print(f"Attempting UNSAFE Write (Overflowing Length {len(overflow_input)}):")

    # In Python, we must explicitly combine the "buffer" and the "adjacent variable" 
    # to simulate the contiguous memory write.
    
    # Create a simulated memory block (Buffer + Important Value space)
    simulated_memory = buffer + [important_value]

    # The 'unsafe' part: write past the end of the original buffer (index 5)
    for i in range(len(overflow_input)):
        if i < len(simulated_memory):
            simulated_memory[i] = overflow_input[i]
        else:
            # Stop the loop if we run out of simulated memory
            break

    # Extract the simulated corrupted data
    simulated_buffer = simulated_memory[:BUFFER_SIZE]
    # In a real overflow, the last few bytes of the input overwrite the int
    simulated_corrupted_int = simulated_memory[BUFFER_SIZE] 

    print(f"  Simulated Corrupted Buffer: {simulated_buffer}")
    print(f"  Simulated Corrupted Value: {hex(simulated_corrupted_int)} (Corrupted!)")
    print("-" * 30)
    print("Observation: The overflowing data (0xFF, 0x01, 0x02) overwrote the\nadjacent 'important' value in the simulation.")

if __name__ == "__main__":
    buffer_overflow_concept()