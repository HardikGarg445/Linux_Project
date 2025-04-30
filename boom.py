
# import socket
# import threading
# import customtkinter as ctk
# from tkinter import messagebox, filedialog, Text
# import json
# import csv

# class PortScannerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Port Scanner Pro")
#         self.root.geometry("800x600")
#         self.root.resizable(True, True)

#         ctk.set_appearance_mode("Dark")  # Default appearance
#         ctk.set_default_color_theme("dark-blue")

#         self.scanning = False
#         self.scan_results = []
#         self.current_theme = "Dark"

#         self.create_widgets()

#     def create_widgets(self):
#         self.frame = ctk.CTkFrame(self.root)
#         self.frame.pack(pady=20, fill="both", expand=True)

#         ctk.CTkLabel(self.frame, text="Target Host/IP:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
#         self.entry_host = ctk.CTkEntry(self.frame, width=250)
#         self.entry_host.grid(row=0, column=1, padx=10, pady=10)

#         ctk.CTkLabel(self.frame, text="Start Port:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
#         self.entry_start_port = ctk.CTkEntry(self.frame, width=100)
#         self.entry_start_port.insert(0, "1")
#         self.entry_start_port.grid(row=1, column=1, padx=10, pady=10)

#         ctk.CTkLabel(self.frame, text="End Port:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
#         self.entry_end_port = ctk.CTkEntry(self.frame, width=100)
#         self.entry_end_port.insert(0, "1024")
#         self.entry_end_port.grid(row=2, column=1, padx=10, pady=10)

#         ctk.CTkLabel(self.frame, text="Scan Type:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
#         self.scan_type = ctk.CTkOptionMenu(self.frame, values=["TCP Connect", "UDP"])
#         self.scan_type.grid(row=3, column=1, padx=10, pady=10)
#         self.scan_type.set("TCP Connect")

#         ctk.CTkLabel(self.frame, text="Timeout (s):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
#         self.entry_timeout = ctk.CTkEntry(self.frame, width=100)
#         self.entry_timeout.insert(0, "0.5")
#         self.entry_timeout.grid(row=4, column=1, padx=10, pady=10)

#         # Custom Canvas progress bar
#         self.progress_canvas = ctk.CTkCanvas(self.root, width=700, height=20, bg="gray20", highlightthickness=0)
#         self.progress_canvas.pack(pady=10)
#         self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 20, fill="green")

#         # Colored result box
#         self.result_box = Text(self.root, width=95, height=15, bg="#1a1a1a", fg="white", insertbackground="white")
#         self.result_box.pack(pady=10)
#         self.result_box.tag_configure("open", foreground="red")
#         self.result_box.tag_configure("closed", foreground="green")
#         self.result_box.tag_configure("error", foreground="yellow")

#         button_frame = ctk.CTkFrame(self.root)
#         button_frame.pack(pady=10)

#         ctk.CTkButton(button_frame, text="Start Scan", command=self.start_scan).pack(side="left", padx=10)
#         ctk.CTkButton(button_frame, text="Save Results", command=self.save_results).pack(side="left", padx=10)
#         ctk.CTkButton(button_frame, text="Toggle Theme", command=self.toggle_theme).pack(side="left", padx=10)

#     def start_scan(self):
#         if self.scanning:
#             return

#         host = self.entry_host.get().strip()
#         try:
#             start_port = int(self.entry_start_port.get())
#             end_port = int(self.entry_end_port.get())
#             timeout = float(self.entry_timeout.get())
#         except ValueError:
#             messagebox.showerror("Input Error", "Please enter valid numbers for ports and timeout.")
#             return

#         if not host:
#             messagebox.showerror("Input Error", "Please enter a host or IP.")
#             return

#         self.result_box.delete("1.0", "end")
#         self.scan_results.clear()
#         self.update_progress(0, 1)  # Reset progress bar

#         self.scanning = True
#         threading.Thread(target=self.scan_ports, args=(host, start_port, end_port, timeout)).start()

#     def scan_ports(self, host, start_port, end_port, timeout):
#         try:
#             ip = socket.gethostbyname(host)
#         except socket.gaierror:
#             self.print_result("Invalid hostname or IP address.\n", "error")
#             self.scanning = False
#             return

#         total_ports = end_port - start_port + 1

#         for i, port in enumerate(range(start_port, end_port + 1)):
#             if self.scan_type.get() == "UDP":
#                 self.scan_udp(ip, port, timeout)
#             else:
#                 self.scan_tcp(ip, port, timeout)
#             self.update_progress(i + 1, total_ports)

#         self.scanning = False
#         messagebox.showinfo("Scan Complete", "Port scan completed!")

#     def scan_tcp(self, ip, port, timeout):
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(timeout)
#             result = sock.connect_ex((ip, port))
#             if result == 0:
#                 service = self.get_service_name(port)
#                 banner = self.grab_banner(sock)
#                 status = f"{port} OPEN [{service}] - {banner}"
#                 self.print_result(status + "\n", "open")
#             else:
#                 status = f"{port} CLOSED"
#                 self.print_result(status + "\n", "closed")
#             sock.close()
#         except Exception as e:
#             status = f"{port} ERROR: {e}"
#             self.print_result(status + "\n", "error")
#         self.scan_results.append(status)

#     def scan_udp(self, ip, port, timeout):
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             sock.settimeout(timeout)
#             sock.sendto(b"\x00", (ip, port))
#             sock.recvfrom(1024)
#             status = f"{port} OPEN (UDP)"
#             self.print_result(status + "\n", "open")
#         except socket.timeout:
#             status = f"{port} CLOSED (UDP)"
#             self.print_result(status + "\n", "closed")
#         except:
#             status = f"{port} ERROR (UDP)"
#             self.print_result(status + "\n", "error")
#         self.scan_results.append(status)

#     def get_service_name(self, port, udp=False):
#         try:
#             return socket.getservbyport(port, 'udp' if udp else 'tcp')
#         except:
#             return "Unknown"

#     def grab_banner(self, sock):
#         try:
#             sock.send(b"GET / HTTP/1.1\r\n\r\n")
#             return sock.recv(1024).decode('utf-8', errors='ignore').strip().split('\n')[0]
#         except:
#             return ""

#     def print_result(self, message, tag):
#         self.result_box.insert("end", message, tag)
#         self.result_box.see("end")

#     def update_progress(self, current, total):
#         width = 700
#         fill_width = int((current / total) * width)
#         self.progress_canvas.coords(self.progress_rect, 0, 0, fill_width, 20)

#     def save_results(self):
#         if not self.scan_results:
#             messagebox.showerror("Error", "No results to save.")
#             return
#         file_path = filedialog.asksaveasfilename(defaultextension=".txt",
#                                                  filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("JSON Files", "*.json")])
#         if not file_path:
#             return

#         if file_path.endswith(".json"):
#             with open(file_path, 'w') as f:
#                 json.dump(self.scan_results, f, indent=2)
#         elif file_path.endswith(".csv"):
#             with open(file_path, 'w', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(["Result"])
#                 for row in self.scan_results:
#                     writer.writerow([row])
#         else:
#             with open(file_path, 'w') as f:
#                 for line in self.scan_results:
#                     f.write(line + "\n")
#         messagebox.showinfo("Success", "Results saved successfully!")

#     def toggle_theme(self):
#         self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
#         ctk.set_appearance_mode(self.current_theme)

# if __name__ == "__main__":
#     root = ctk.CTk()
#     app = PortScannerApp(root)
#     root.mainloop()




import socket
import threading
import customtkinter as ctk
from tkinter import messagebox, filedialog, Text
import json
import csv

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner Pro")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        ctk.set_appearance_mode("Dark")  # Default appearance
        ctk.set_default_color_theme("dark-blue")

        self.scanning = False
        self.scan_results = []
        self.current_theme = "Dark"

        self.create_widgets()

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, fill="both", expand=True)

        # Label and Entry arranged in a 2-column grid
        ctk.CTkLabel(self.frame, text="Target Host/IP:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_host = ctk.CTkEntry(self.frame, width=250)
        self.entry_host.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Start Port:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_start_port = ctk.CTkEntry(self.frame, width=100)
        self.entry_start_port.insert(0, "1")
        self.entry_start_port.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="End Port:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_end_port = ctk.CTkEntry(self.frame, width=100)
        self.entry_end_port.insert(0, "1024")
        self.entry_end_port.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Scan Type:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.scan_type = ctk.CTkOptionMenu(self.frame, values=["TCP Connect", "UDP"])
        self.scan_type.grid(row=3, column=1, padx=10, pady=10)
        self.scan_type.set("TCP Connect")

        ctk.CTkLabel(self.frame, text="Timeout (s):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_timeout = ctk.CTkEntry(self.frame, width=100)
        self.entry_timeout.insert(0, "0.5")
        self.entry_timeout.grid(row=4, column=1, padx=10, pady=10)

        # Custom Canvas progress bar
        self.progress_canvas = ctk.CTkCanvas(self.root, width=700, height=20, bg="gray20", highlightthickness=0)
        self.progress_canvas.pack(pady=10)
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 20, fill="green")

        # Colored result box
        self.result_box = Text(self.root, width=95, height=15, bg="#1a1a1a", fg="white", insertbackground="white")
        self.result_box.pack(pady=10)
        self.result_box.tag_configure("open", foreground="red")
        self.result_box.tag_configure("closed", foreground="green")
        self.result_box.tag_configure("error", foreground="yellow")

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
        self.scan_results.clear()
        self.update_progress(0, 1)  # Reset progress bar

        self.scanning = True
        threading.Thread(target=self.scan_ports, args=(host, start_port, end_port, timeout)).start()

    def scan_ports(self, host, start_port, end_port, timeout):
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            self.print_result("Invalid hostname or IP address.\n", "error")
            self.scanning = False
            return

        total_ports = end_port - start_port + 1

        for i, port in enumerate(range(start_port, end_port + 1)):
            if self.scan_type.get() == "UDP":
                self.scan_udp(ip, port, timeout)
            else:
                self.scan_tcp(ip, port, timeout)
            self.update_progress(i + 1, total_ports)

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
                self.print_result(status + "\n", "open")
            else:
                status = f"{port} CLOSED"
                self.print_result(status + "\n", "closed")
            sock.close()
        except Exception as e:
            status = f"{port} ERROR: {e}"
            self.print_result(status + "\n", "error")
        self.scan_results.append(status)

    def scan_udp(self, ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(b"\x00", (ip, port))
            sock.recvfrom(1024)
            status = f"{port} OPEN (UDP)"
            self.print_result(status + "\n", "open")
        except socket.timeout:
            status = f"{port} CLOSED (UDP)"
            self.print_result(status + "\n", "closed")
        except:
            status = f"{port} ERROR (UDP)"
            self.print_result(status + "\n", "error")
        self.scan_results.append(status)

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

    def print_result(self, message, tag):
        self.result_box.insert("end", message, tag)
        self.result_box.see("end")

    def update_progress(self, current, total):
        width = 700
        fill_width = int((current / total) * width)
        self.progress_canvas.coords(self.progress_rect, 0, 0, fill_width, 20)

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
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        ctk.set_appearance_mode(self.current_theme)

if __name__ == "__main__":
    root = ctk.CTk()
    app = PortScannerApp(root)
    root.mainloop()


