import socket
from pymongo import MongoClient
import time

#connects to mongodb using pymongo.
def connect_to_database():
    connection_string = ""
    client = MongoClient(connection_string)
    db = client["test"]
    return db

#this code simplifies and calls the functions depending on what query was selected.
def handle_query(query, db):
    try:
        if query == "1":
            return query_one(db)
        elif query == "2":
            return query_two(db)
        elif query == "3":
            return query_three(db)
        elif query.lower() == "exit":
            return 0  # Signal to close the client connection
        else:
            return "Invalid query. Please send a valid query."
    except Exception as e:
        print(f"Error in query handling: {e}")
        return f"Error: {e}"

#handles the query one using pipeline and lookup by joinging birtual and metadata.
def query_one(db):
    pipeline = [
        {
            "$lookup": {
                "from": "LAB7_metadata",
                "localField": "payload.parent_asset_uid",
                "foreignField": "assetUid",
                "as": "meta",
            }
        },
        {
            "$match": {
                "meta.customAttributes.additionalMetadata.location": "kitchen",
                "payload.timestamp": {
                    "$lte": str(time.time()),
                    "$gt": str(time.time() - 10800),  # Last 3 hours
                }
            },
        },
        {
            "$group": {
                "_id": "$payload.parent_asset_uid",
                "avgMoisture": {
                    "$avg": {"$toDouble": "$payload.Moisture Meter - 1"}
                },
                "deviceName": {"$first": "$meta.customAttributes.name"}  # Get the device name
            },
        }
    ]
    results = db["LAB7_virtual"].aggregate(pipeline)
    response = [
        f"Device: {result['deviceName']}, Average Moisture: {result['avgMoisture']:.2f}% RH"
        for result in results
    ]
    print("Debug: Aggregation Results:", response)   
    return "\n".join(response) if response else "No matching data found for the last three hours."

#handles the average of the water consumption used by the dishwasher from all the data.
def query_two(db):
    pipeline = [
        {
            "$lookup": {
                "from": "LAB7_metadata",
                "localField": "payload.parent_asset_uid",
                "foreignField": "assetUid",
                "as": "meta",
            }
        },
        {
            "$match": {
                "meta.customAttributes.additionalMetadata.location": "kitchen1",
                "meta.customAttributes.name": "Dishwasher"
            }
        },
        {
            "$group": {
                "_id": "$payload.parent_asset_uid",
                "avgWaterConsumption": {
                    "$avg": {"$toDouble": "$payload.Water consumption"}
                },
                "deviceName": {"$first": "$meta.customAttributes.name"}  # Get the device name

            }
        }
    ]
    results = db["LAB7_virtual"].aggregate(pipeline)
    response = [
        f"Device: {result['deviceName']}, Average Water Consumption: {result['avgWaterConsumption']:.2f} gallons per cycle"
        for result in results
    ]
    print("Debug: Aggregation Results:", response)
    return "\n".join(response) if response else "No matching data found."

#
def query_three(db):
    #defines the aggregation pippeline
    pipeline = [
        {
            "$lookup": {
                "from": "LAB7_metadata",
                "localField": "payload.parent_asset_uid",
                "foreignField": "assetUid",
                "as": "meta",
            }
        },
        {
             # Add or modify fields in the current documents
            "$set": {
                #Calculate a new field called electricityConsumption
                "electricityConsumption": {
                    # Use a switch case to determine the value depending on the branches conditions and values
                    "$switch": {
                        "branches": [
                            {
                                "case": {"$gt": ["$payload.Ammeter 1", None]},
                                "then": {"$toDouble": "$payload.Ammeter 1"},
                            },
                            {
                                "case": {"$gt": ["$payload.Ammeter 2", None]},
                                "then": {"$toDouble": "$payload.Ammeter 2"},
                            },
                            {
                                "case": {"$gt": ["$payload.sensor 3 68ef587e-9fb0-4b6f-afc5-503b0e802e6f", None]},
                                "then": {"$toDouble": "$payload.sensor 3 68ef587e-9fb0-4b6f-afc5-503b0e802e6f"},
                            }
                        ],
                        "default": 0
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$payload.parent_asset_uid",# Groups by parent_asset_uid
                "totalElectricityConsumption": {"$sum": "$electricityConsumption"},# Sum the electricity consumption
                "deviceName": {"$first": "$meta.customAttributes.name"}  # Get the device name
            }
        },
        {
            "$sort": {"totalElectricityConsumption": -1}  # Descending order
        },
        {
            "$limit": 1  # Get the top device which has the most
        }
    ]

    results = db["LAB7_virtual"].aggregate(pipeline)
    response = [
        f"Device: {result['deviceName']}, Total Electricity Consumption: {result['totalElectricityConsumption']:.2f} kWh"
        for result in results
    ]
    print("Debug: Aggregation Results:", response)
    return "\n".join(response) if response else "No matching data found."


def server():
    db = connect_to_database()
    my_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = str(input("Enter the server IP address: "))
    server_port = int(input("Enter the port number to run the server on: ")) 

    my_tcp_socket.bind((server_ip, server_port))
    my_tcp_socket.listen(5)
    print("Server is running and waiting for a connection...")

    while True:
        try:
            # Accept a connection from a client
            incoming_socket, incoming_address = my_tcp_socket.accept()
            print(f"Connection established with {incoming_address}")

            while True:
                try:
                    # Receive data from the client
                    query = incoming_socket.recv(1024)
                    if not query:
                        print("Client disconnected.")
                        break

                    # Decode the data received from the client
                    query = query.decode('utf-8').strip()
                    print(f"Received query from client: {query}")
                    
                    # Handle the query
                    response = handle_query(query, db)

                    if response == 0:
                        print("Client requested to close the connection.")
                        incoming_socket.sendall("Connection closed.".encode())
                        break

                    # Send the response back to the client
                    incoming_socket.sendall(response.encode())
                except Exception as e:
                    print(f"Error while handling query: {e}")
                    incoming_socket.sendall(f"Error: {e}".encode())
                    break

        except Exception as e:
            print(f"Connection error: {e}")

        finally:
            incoming_socket.close()
            print("Connection closed.")

if __name__ == "__main__":
    server()
