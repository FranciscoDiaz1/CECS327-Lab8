# CECS327-Lab8
This project integrates IoT sensors, a TCP client-server system, and a MongoDB database to process and analyze IoT data. It includes metadata for IoT devices and handles user queries with data conversions and efficient processing.

## Table of Contents
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Running Client and Server on Google Cloud VMs](#running-client-and-server-on-google-cloud-vms)
- [Possible Queries](#possible-queries)


---

## Requirements
- **Python 3.8+**
- **MongoDB**: URL to access the database
- **IoT Sensor Data**: Generated via [dataniz.com](https://dataniz.com) (devices must be configured and turned on)
- **Libraries**
- **Google Cloud VMs**: Separate VMs for running the server and client
- Previous Labs: Prior assignments must be completed and functioning to ensure success in this lab.

---

## Setup Instructions
1. **Create the GitHub Repository**
   - Add the TA as a collaborator to provide access to your code and README file.

2. **Install Necessary Libraries**
   - Install `pymongo` by running:
     ```
     pip install pymongo
     ```
     in the terminal for each Google VM.
   - Import the `time` and `socket` modules in your code to manage port connections.

3. **Configure Firewall Rules**
   - Open the Google Cloud Console.
   - Add firewall rules to allow traffic on the specified port numbers for both server and client.
   - Ensure the rules are configured for both incoming and outgoing traffic.

4. **Set Up MongoDB**
   - Use a hosted MongoDB instance or set up your own on another Google VM.
   - Configure the database connection string (`MONGO_URI`) in your code.

---

## Running Client and Server on Google Cloud VMs

1. **Start the Server**
   - Open the terminal on the **server VM**.
   - Navigate to the directory containing your server code/file:
     ```
     cd path/to/server
     ```
   - Start the server with:
     ```
     python server.py
     ```

2. **Start the Client**
   - Open the terminal on the **client VM**.
   - Navigate to the directory containing the client code/file:
     ```
     cd path/to/client
     ```
   - Start the client with:
     ```
     python client.py
     ```

3. **Connecting the Server and Client**
   - Ensure the **server's public IP address** is correctly specified in the client's configuration.
   - Both VMs must have firewall rules configured to allow the required communication.
   - 
---

## Possible Queries

### How to Select a Query
To select a query, enter the corresponding number (1, 2, or 3) when prompted by the client application.

### Queries List
1. **Average Moisture in Kitchen Fridge (last 3 hours)**
   - Command:
     ```
     1
     ```
   - Description:
     Calculates the average relative humidity (RH%) inside your kitchen fridge for the past three hours.

2. **Average Water Consumption Per  Cycle**
   - Command:
     ```
     2
     ```
   - Description:
     Calculates the average water usage per cycle for your smart dishwasher.

3. **Electricity Consumption Comparison**
   - Command:
     ```
     3
     ```
   - Description:
     Determines which of the IoT devices (e.g., two refrigerators and one dishwasher) consumed the most electricity.
     
4. **Terminate Program**
   - Command:
     ```
     exit
     ```
   - Description:
     This input will terminate and close the client program and closes the socket being used.

---

## Invalid Queries
If you enter an invalid number or unsupported query, the system will display the following message:
  - Sorry, this query cannot be processed. Please try one of the following:
 1. What is the average moisture inside my kitchen fridge in the past three hours?
 2. What is the average water consumption per cycle in my smart dishwasher?
 3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?

