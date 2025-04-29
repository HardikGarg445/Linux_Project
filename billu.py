import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import csv
import json

class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner Pro")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.style = ttk.Style(self.root)
        self.current_theme = "light"
        self.set_theme("light")

        self.create_widgets()

        self.scanning = False
        self.scan_results = []

    def set_theme(self, theme):
        if theme == "dark":
            self.root.configure(bg="#2e2e2e")
            self.style.configure("TLabel", background="#2e2e2e", foreground="white")
            self.style.configure("TEntry", fieldbackground="#3e3e3e", foreground="white")
            self.style.configure("TButton", background="#3e3e3e", foreground="white")
            self.style.configure("TCombobox", fieldbackground="#3e3e3e", background="#3e3e3e", foreground="white")
        else:
            self.root.configure(bg="white")
            self.style.configure("TLabel", background="white", foreground="black")
            self.style.configure("TEntry", fieldbackground="white", foreground="black")
            self.style.configure("TButton", background="white", foreground="black")
            self.style.configure("TCombobox", fieldbackground="white", background="white", foreground="black")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.set_theme(self.current_theme)

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Target Host/IP:").grid(row=0, column=0, sticky="w")
        self.entry_host = ttk.Entry(frame, width=40)
        self.entry_host.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Start Port:").grid(row=1, column=0, sticky="w")
        self.entry_start_port = ttk.Entry(frame, width=20)
        self.entry_start_port.grid(row=1, column=1, sticky="w", pady=5)
        self.entry_start_port.insert(0, "1")

        ttk.Label(frame, text="End Port:").grid(row=2, column=0, sticky="w")
        self.entry_end_port = ttk.Entry(frame, width=20)
        self.entry_end_port.grid(row=2, column=1, sticky="w", pady=5)
        self.entry_end_port.insert(0, "1024")

        ttk.Label(frame, text="Scan Type:").grid(row=3, column=0, sticky="w")
        self.scan_type = ttk.Combobox(frame, values=["TCP Connect", "UDP"], state="readonly")
        self.scan_type.current(0)
        self.scan_type.grid(row=3, column=1, sticky="w", pady=5)

        ttk.Label(frame, text="Timeout (s):").grid(row=4, column=0, sticky="w")
        self.entry_timeout = ttk.Entry(frame, width=20)
        self.entry_timeout.grid(row=4, column=1, sticky="w", pady=5)
        self.entry_timeout.insert(0, "0.5")

        self.button_start = ttk.Button(frame, text="Start Scan", command=self.start_scan)
        self.button_start.grid(row=5, column=0, columnspan=2, pady=10)

        self.button_theme = ttk.Button(frame, text="Toggle Theme", command=self.toggle_theme)
        self.button_theme.grid(row=6, column=0, columnspan=2)

        self.progress = ttk.Progressbar(self.root, length=700, mode='determinate')
        self.progress.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Port", "Service", "Banner", "Status"), show="headings", height=15)
        self.tree.heading("Port", text="Port")
        self.tree.heading("Service", text="Service")
        self.tree.heading("Banner", text="Banner")
        self.tree.heading("Status", text="Status")
        self.tree.pack(pady=10)

        self.button_save = ttk.Button(self.root, text="Save Results", command=self.save_results)
        self.button_save.pack(pady=5)

    def start_scan(self):
        if self.scanning:
            return

        host = self.entry_host.get().strip()
        start_port = int(self.entry_start_port.get().strip())
        end_port = int(self.entry_end_port.get().strip())
        timeout = float(self.entry_timeout.get().strip())
        scan_type = self.scan_type.get()

        if not host:
            messagebox.showerror("Error", "Please enter a valid host/IP")
            return

        self.scan_results.clear()
        self.tree.delete(*self.tree.get_children())

        self.progress['value'] = 0
        self.progress['maximum'] = (end_port - start_port + 1)

        self.scanning = True
        threading.Thread(target=self.scan_ports, args=(host, start_port, end_port, timeout, scan_type)).start()

    def scan_ports(self, host, start_port, end_port, timeout, scan_type):
        ip = socket.gethostbyname(host)
        for port in range(start_port, end_port + 1):
            if scan_type == "UDP":
                self.scan_udp(ip, port, timeout)
            else:
                self.scan_tcp(ip, port, timeout)
            self.progress['value'] += 1

        self.scanning = False
        messagebox.showinfo("Done", "Scan Completed!")

    def scan_tcp(self, ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = self.get_service_name(port)
                banner = self.grab_banner(sock)
                status = "Open"
            else:
                service = self.get_service_name(port)
                banner = "N/A"
                status = "Closed"

            self.scan_results.append((port, service, banner, status))
            self.tree.insert("", "end", values=(port, service, banner, status))
            sock.close()
        except:
            pass

    def scan_udp(self, ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(b"\x00", (ip, port))
            sock.recvfrom(1024)
            service = self.get_service_name(port, udp=True)
            self.scan_results.append((port, service, "UDP Response", "Open"))
            self.tree.insert("", "end", values=(port, service, "UDP Response", "Open"))
        except socket.timeout:
            self.scan_results.append((port, "Unknown", "N/A", "Closed"))
            self.tree.insert("", "end", values=(port, "Unknown", "N/A", "Closed"))
        except:
            self.scan_results.append((port, "Unknown", "N/A", "Closed"))
            self.tree.insert("", "end", values=(port, "Unknown", "N/A", "Closed"))

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
            messagebox.showerror("Error", "No scan results to save!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON Files", "*.json"),
                                                            ("CSV Files", "*.csv"),
                                                            ("Text Files", "*.txt")])
        if not file_path:
            return

        if file_path.endswith(".json"):
            with open(file_path, 'w') as f:
                json.dump(self.scan_results, f, indent=2)
        elif file_path.endswith(".csv"):
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Port", "Service", "Banner", "Status"])
                for row in self.scan_results:
                    writer.writerow(row)
        elif file_path.endswith(".txt"):
            with open(file_path, 'w') as f:
                for row in self.scan_results:
                    f.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\n")
        messagebox.showinfo("Success", "Results saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()
