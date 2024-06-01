import os
from scapy.all import sniff, wrpcap
from datetime import datetime


def packet_callback(packet):
    print(packet.summary())

def capture_packets(interface, count, output_file):
    # 创建一个新的文件
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 捕获特定接口的数据
    packets = sniff(iface=interface, count=count, prn=packet_callback)
    
    # 保存为一个pcap
    wrpcap(output_file, packets)
    print(f"Captured {count} packets and saved to {output_file}")

if __name__ == "__main__":
    interface = "WLAN"  
    count = 11
    time_str = datetime.now().strftime("%Y.%m.%d-%H'%M'%S")
    output_file = f"./MFR_test/pcap_files/test/captured_{time_str}.pcap"
    
    # 抓包
    capture_packets(interface, count, output_file)
