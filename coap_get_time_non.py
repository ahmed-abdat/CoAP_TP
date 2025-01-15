import socket
import struct

# CoAP Protocol Constants
class CoAP:
    # Message Types
    CON = 0  # Confirmable
    NON = 1  # Non-confirmable
    ACK = 2  # Acknowledgement
    RST = 3  # Reset
    
    # Request Codes
    GET = 1
    
    # Protocol Version
    VER = 1

def create_option(number, value):
    """Create a CoAP option"""
    option = bytearray()
    option.extend(struct.pack('!B', number))  # Option number
    option.extend(struct.pack('!B', len(value)))  # Option length
    option.extend(value.encode())  # Option value
    return option

def create_non_get_request(resource_path, msg_id=1):
    """Create a NON-confirmable CoAP GET request"""
    msg = bytearray()
    # Header: Version 1, Type NON, No Token
    msg.extend(struct.pack('!B', (CoAP.VER << 6) | (CoAP.NON << 4)))
    msg.extend(struct.pack('!B', CoAP.GET))  # Code 1 (GET)
    msg.extend(struct.pack('!H', msg_id))  # Message ID
    
    # Add Uri-Path option (number 11)
    msg.extend(create_option(11, resource_path))
    return msg

def main():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 5683)  # Replace with your server's IP
    
    try:
        # Create and send NON GET request
        msg = create_non_get_request("time")
        print(f"Sending NON-confirmable CoAP GET request: {msg.hex()}")
        sock.sendto(msg, server_address)
        
        # Wait for response
        sock.settimeout(10)
        data, addr = sock.recvfrom(1024)
        print(f"Received response: {data.hex()}")
        
        # Extract time from response if present
        payload_pos = data.find(b'\xff')
        if payload_pos != -1:
            time_str = data[payload_pos + 1:].decode('utf-8')
            print(f"Server time: {time_str}")
        
    except socket.timeout:
        print("No response received (timeout)")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main() 