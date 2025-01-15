import socket
import struct

# CoAP Protocol Constants
class CoAP:
    # Message Types
    CON = 0  # Confirmable
    NON = 1  # Non-confirmable
    ACK = 2  # Acknowledgement
    RST = 3  # Reset
    
    # Protocol Version
    VER = 1

def create_empty_message(msg_id=1):
    """Create an empty CoAP message"""
    msg = bytearray()
    # Header: Version 1, Type CON, No Token
    msg.extend(struct.pack('!B', (CoAP.VER << 6) | (CoAP.CON << 4)))
    msg.extend(struct.pack('!B', 0))  # Code 0 (Empty)
    msg.extend(struct.pack('!H', msg_id))  # Message ID
    return msg

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 5683)  # Replace with your server's IP
    
    try:
        # Create and send empty message
        msg = create_empty_message()
        print(f"Sending empty CoAP message: {msg.hex()}")
        sock.sendto(msg, server_address)
        
        # Wait for response
        sock.settimeout(10)
        data, addr = sock.recvfrom(1024)
        print(f"Received response: {data.hex()}")
        
    except socket.timeout:
        print("No response received (timeout)")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main() 