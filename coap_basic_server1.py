# coap_basic_server1.py
import socket
import struct
import datetime
import time

# Configuration
SERVER_ADDRESS = ('0.0.0.0', 5683)
SIMULATE_DELAY = True  # Set to False to test without delay

class CoAP:
    """CoAP Protocol Constants"""
    # Message Types
    CON = 0  # Confirmable
    NON = 1  # Non-confirmable
    ACK = 2  # Acknowledgement
    RST = 3  # Reset
    
    # Response Codes
    EMPTY = 0
    GET = 1
    CONTENT = 69  # 2.05 Content
    
    # Protocol
    VER = 1

def parse_message(data):
    """Parse incoming CoAP message"""
    if len(data) < 4:
        return None
    
    # Parse header
    ver_type_tkl = data[0]
    version = (ver_type_tkl >> 6) & 0x03
    msg_type = (ver_type_tkl >> 4) & 0x03
    token_length = ver_type_tkl & 0x0F
    
    # Parse code and message ID
    code = data[1]
    msg_id = struct.unpack('!H', data[2:4])[0]
    
    # Extract token if present
    token = data[4:4+token_length] if token_length > 0 else None
    
    return version, msg_type, code, msg_id, token

def create_response(msg_type, code, msg_id, token=None, payload=None):
    """Create a CoAP response message"""
    token_length = len(token) if token else 0
    response = bytearray()
    
    # Add header
    response.extend(struct.pack('!B', (CoAP.VER << 6) | (msg_type << 4) | token_length))
    response.extend(struct.pack('!B', code))
    response.extend(struct.pack('!H', msg_id))
    
    # Add token if present
    if token:
        response.extend(token)
    
    # Add payload if present
    if payload:
        response.extend(b'\xff')  # Payload marker
        response.extend(payload)
    
    return response

def handle_empty_message(msg_id, token, client_address, sock):
    """Handle empty CoAP message"""
    print(f"Received empty message from {client_address}")
    response = create_response(CoAP.RST, CoAP.EMPTY, msg_id, token)
    print(f"Sending RST response: {response.hex()}")
    sock.sendto(response, client_address)

def handle_get_request(msg_type, msg_id, token, client_address, sock):
    """Handle GET request for time resource"""
    print(f"Received GET request from {client_address}")
    
    # Send ACK for confirmable requests
    if msg_type == CoAP.CON:
        ack = create_response(CoAP.ACK, CoAP.EMPTY, msg_id, token)
        print(f"Sending ACK: {ack.hex()}")
        sock.sendto(ack, client_address)
    
    # Simulate processing delay if enabled
    if SIMULATE_DELAY:
        print("Processing request (5 seconds delay)...")
        time.sleep(5)
    
    # Prepare and send response
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')
    response_type = CoAP.CON if (msg_type == CoAP.CON and SIMULATE_DELAY) else msg_type
    response = create_response(response_type, CoAP.CONTENT, 
                             msg_id + 1 if SIMULATE_DELAY else msg_id, 
                             token, time_str)
    print(f"Sending response: {response.hex()}")
    sock.sendto(response, client_address)

def main():
    """Main server loop"""
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Bind socket
        print(f"Starting server on {SERVER_ADDRESS}")
        print(f"Simulated delay is {'enabled' if SIMULATE_DELAY else 'disabled'}")
        sock.bind(SERVER_ADDRESS)
        
        # Main loop
        while True:
            print("\nWaiting for incoming messages...")
            data, client_address = sock.recvfrom(1024)
            print(f"Received message: {data.hex()}")
            
            # Parse message
            version, msg_type, code, msg_id, token = parse_message(data)
            
            # Handle message based on code
            if code == CoAP.EMPTY:
                handle_empty_message(msg_id, token, client_address, sock)
            elif code == CoAP.GET:
                handle_get_request(msg_type, msg_id, token, client_address, sock)
    
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Closing server socket")
        sock.close()

if __name__ == "__main__":
    main()
