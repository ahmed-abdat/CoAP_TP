import socket
import struct

# CoAP message fields
class CoAP:
    VER = 1
    CON = 0
    NON = 1
    ACK = 2
    RST = 3
    GET = 1  # GET method code

def create_option(number, value):
    """Create a CoAP option with given number and value"""
    option = bytearray()
    option.extend(struct.pack('!B', number))  # Option number
    option.extend(struct.pack('!B', len(value)))  # Option length
    option.extend(value.encode())  # Option value
    return option

def parse_response(data):
    """Parse CoAP response and extract payload"""
    if len(data) < 4:
        return None
    
    ver_type_tkl = data[0]
    code = data[1]
    msg_type = (ver_type_tkl >> 4) & 0x03
    
    # If there's payload (after options), it starts after 0xFF marker
    payload_pos = data.find(b'\xff')
    if payload_pos != -1:
        return data[payload_pos + 1:]
    return None

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create CoAP GET message for /time resource
msg = bytearray()
# Header: Version 1, Type CON, No Token
msg.extend(struct.pack('!B', (CoAP.VER << 6) | (CoAP.CON << 4)))
msg.extend(struct.pack('!B', CoAP.GET))  # Code 1 (GET)
msg.extend(struct.pack('!H', 1))  # Message ID = 1

# Add Uri-Path option (number 11) with value "time"
msg.extend(create_option(11, "time"))

print(f"Sending CoAP GET request: {msg.hex()}")

# Send to server
SERVER = ('127.0.0.1', 5683)  # Replace with your server's IP
sock.sendto(msg, SERVER)

# Set timeout for response
sock.settimeout(10)

try:
    # Wait for first response (ACK)
    data, addr = sock.recvfrom(1024)
    print(f"Received ACK: {data.hex()}")
    
    # Wait for second response (actual data)
    data, addr = sock.recvfrom(1024)
    print(f"Received response: {data.hex()}")
    
    # Parse and display payload
    payload = parse_response(data)
    if payload:
        print(f"Time from server: {payload.decode('utf-8')}")
    
except socket.timeout:
    print("No response received (timeout)")
finally:
    sock.close() 