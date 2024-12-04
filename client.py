import socket

# Predefined valid queries
valid_queries = [
    "What is the average moisture inside my kitchen fridge in the past three hours?",
    "What is the average water consumption per cycle in my smart dishwasher?",
    "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?",
]

def client():
    # Prompt user for server's IP and port
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port number: "))
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        tcp_socket.connect((server_ip, server_port))
        tcp_socket.settimeout(20)  # Set a timeout of 20 seconds
        print("Connected to the server.")
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    while True:
        # Asking user to enter query of choice
        print("\nEnter a query:")
        for i, query in enumerate(valid_queries, start=1):
            print(f"{i}: {query}")
        print("Type '1', '2', or '3' to send a query, or 'exit' to quit.")

        query_input = input("Your choice: ").strip()

        #Terminating the program when user enters "exit" in the query
        if query_input.lower() == "exit":
            tcp_socket.send(query_input.encode("utf-8"))
            print("Exiting client. Closing connection.")
            break

        # Validate input
        if query_input in ["1", "2", "3"]:
            try:
                # Send the message to the server
                tcp_socket.send(query_input.encode("utf-8"))

                # Receive and display the response
                response = tcp_socket.recv(4096)  # Increased buffer size
                print("\nServer replied:\n" + "=" * 20)
                print(response.decode("utf-8"))
                print("=" * 20)
            except socket.timeout:
                print("Server response timed out. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Sorry, this query cannot be processed. Please try one of the following:")
    # Close the socket
    tcp_socket.close()

if __name__ == "__main__":
    client()
