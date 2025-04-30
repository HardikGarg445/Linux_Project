import socket
import threading
import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import csv

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner Pro")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        ctk.set_appearance_mode("dark")  # Options: "light", "dark"
        ctk.set_default_color_theme("dark-blue")

        self.scanning = False
        self.scan_results = []

        self.create_widgets()

    def create_widgets(self):
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Target Host/IP:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_host = ctk.CTkEntry(frame, width=250)
        self.entry_host.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Start Port:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_start_port = ctk.CTkEntry(frame, width=100)
        self.entry_start_port.insert(0, "1")
        self.entry_start_port.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="End Port:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_end_port = ctk.CTkEntry(frame, width=100)
        self.entry_end_port.insert(0, "1024")
        self.entry_end_port.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Scan Type:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.scan_type = ctk.CTkOptionMenu(frame, values=["TCP Connect", "UDP"])
        self.scan_type.grid(row=3, column=1, padx=10, pady=10)
        self.scan_type.set("TCP Connect")

        ctk.CTkLabel(frame, text="Timeout (s):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_timeout = ctk.CTkEntry(frame, width=100)
        self.entry_timeout.insert(0, "0.5")
        self.entry_timeout.grid(row=4, column=1, padx=10, pady=10)

        self.progress = ctk.CTkProgressBar(self.root, width=700)
        self.progress.set(0)
        self.progress.pack(pady=10)

        self.result_box = ctk.CTkTextbox(self.root, width=750, height=200)
        self.result_box.pack(pady=10)

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Start Scan", command=self.start_scan).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Save Results", command=self.save_results).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Toggle Theme", command=self.toggle_theme).pack(side="left", padx=10)

    def start_scan(self):
        if self.scanning:
            return

        host = self.entry_host.get().strip()
        try:
            start_port = int(self.entry_start_port.get())
            end_port = int(self.entry_end_port.get())
            timeout = float(self.entry_timeout.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for ports and timeout.")
            return

        if not host:
            messagebox.showerror("Input Error", "Please enter a host or IP.")
            return

        self.result_box.delete("1.0", "end")
        self.progress.set(0)
        self.scan_results.clear()

        self.scanning = True
        threading.Thread(target=self.scan_ports, args=(host, start_port, end_port, timeout)).start()

    def scan_ports(self, host, start_port, end_port, timeout):
        ip = socket.gethostbyname(host)
        total_ports = end_port - start_port + 1

        for i, port in enumerate(range(start_port, end_port + 1)):
            if self.scan_type.get() == "UDP":
                self.scan_udp(ip, port, timeout)
            else:
                self.scan_tcp(ip, port, timeout)
            self.progress.set((i + 1) / total_ports)

        self.scanning = False
        messagebox.showinfo("Scan Complete", "Port scan completed!")

    def scan_tcp(self, ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = self.get_service_name(port)
                banner = self.grab_banner(sock)
                status = f"{port} OPEN [{service}] - {banner}"
            else:
                status = f"{port} CLOSED"
            sock.close()
        except Exception as e:
            status = f"{port} ERROR: {e}"
        self.scan_results.append(status)
        self.result_box.insert("end", status + "\n")

    def scan_udp(self, ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(b"\x00", (ip, port))
            sock.recvfrom(1024)
            status = f"{port} OPEN (UDP)"
        except socket.timeout:
            status = f"{port} CLOSED (UDP)"
        except:
            status = f"{port} ERROR (UDP)"
        self.scan_results.append(status)
        self.result_box.insert("end", status + "\n")

    def get_service_name(self, port, udp=False):
        try:
            return socket.getservbyport(port, 'udp' if udp else 'tcp')
        except:
            return "Unknown"

    def grab_banner(self, sock):
        try:
            sock.send(b"GET / HTTP/1.1\r\n\r\n")
            return sock.recv(1024).decode('utf-8', errors='ignore').strip().split('\n')[0]
        except:
            return ""

    def save_results(self):
        if not self.scan_results:
            messagebox.showerror("Error", "No results to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json")])
        if not file_path:
            return

        if file_path.endswith(".json"):
            with open(file_path, 'w') as f:
                json.dump(self.scan_results, f, indent=2)
        elif file_path.endswith(".csv"):
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Result"])
                for row in self.scan_results:
                    writer.writerow([row])
        else:
            with open(file_path, 'w') as f:
                for line in self.scan_results:
                    f.write(line + "\n")
        messagebox.showinfo("Success", "Results saved successfully!")

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current == "dark" else "dark")


if __name__ == "__main__":
    root = ctk.CTk()
    app = PortScannerApp(root)
    root.mainloop()
