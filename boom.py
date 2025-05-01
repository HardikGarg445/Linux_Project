














# import socket
# import threading
# import customtkinter as ctk
# from tkinter import messagebox, filedialog
# from tkinter import ttk
# import json
# import csv

# class PortScannerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Port Scanner Pro")
#         self.root.geometry("900x720")
#         self.root.resizable(True, True)

#         # Theme and colors
#         self.current_theme = "Dark"
#         ctk.set_appearance_mode(self.current_theme)
        
#         # Define color schemes
#         self.colors = {
#             "Dark": {
#                 "upper_bg": "#212121",
#                 "lower_bg": "#242424",
#                 "blue": "#212121",
#                 "red": "#E45151",
#                 "yellow": "#EAFF00",
#                 "dark_blue": "#15375C",
#                 "border": "#636363",
#                 "output_bg": "#1A1A1A",
#                 "text": "#FFFFFF"
#             },
#             "Light": {
#                 "upper_bg": "#FFFFFF",
#                 "lower_bg": "#D5D7E1",
#                 "blue": "#212121",
#                 "red": "#E45151",
#                 "yellow": "#EAFF00",
#                 "dark_blue": "#15375C",
#                 "border": "#EAE8E8",
#                 "output_bg": "#EAE8E8",
#                 "text": "#000000"
#             }
#         }
        
#         self.scanning = False
#         self.scan_results = []
#         self.custom_font = ("Courier New", 12, "bold")
#         self.init_ui()
#         self.update_theme_colors()

#     def init_ui(self):
#         # Main container
#         self.main_frame = ctk.CTkFrame(self.root)
#         self.main_frame.pack(pady=20, fill="both", expand=True)

#         # Input frame
#         self.input_frame = ctk.CTkFrame(self.main_frame)
#         self.input_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=20)

#         # Circular progress frame
#         self.circle_frame = ctk.CTkFrame(self.main_frame, width=200, height=200)
#         self.circle_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")
        
#         # Create circular progress indicator
#         self.circle_canvas = ctk.CTkCanvas(self.circle_frame, width=180, height=180, highlightthickness=0)
#         self.circle_canvas.place(x=10, y=10)
        
#         # Background circle
#         self.bg_circle = self.circle_canvas.create_oval(10, 10, 170, 170, width=15, outline="#636363")
        
#         # Progress arc
#         self.arc = self.circle_canvas.create_arc(10, 10, 170, 170, start=90, extent=0, style="arc", width=15, outline="#15375C")
        
#         # Percentage text
#         self.percentage_text = self.circle_canvas.create_text(90, 70, text="60%", font=("Arial", 30, "bold"), fill="#FFFFFF")
#         self.progress_label = self.circle_canvas.create_text(90, 110, text="Progress", font=("Arial", 14), fill="#FFFFFF")
        
#         # Time taken label
#         self.time_label = ctk.CTkLabel(self.circle_frame, text="Time taken: 52 s", font=("Arial", 14))
#         self.time_label.place(x=30, y=200)

#         # Host input
#         ctk.CTkLabel(self.input_frame, text="Target Host/IP :", font=self.custom_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
#         self.entry_host = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
#         self.entry_host.grid(row=0, column=1, padx=10, pady=10)

#         # Port range inputs
#         ctk.CTkLabel(self.input_frame, text="Start Port :", font=self.custom_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
#         self.entry_start_port = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
#         self.entry_start_port.insert(0, "1")
#         self.entry_start_port.grid(row=1, column=1, padx=10, pady=10)

#         ctk.CTkLabel(self.input_frame, text="End Port :", font=self.custom_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
#         self.entry_end_port = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
#         self.entry_end_port.insert(0, "1024")
#         self.entry_end_port.grid(row=2, column=1, padx=10, pady=10)

#         # Scan type
#         ctk.CTkLabel(self.input_frame, text="Scan Type :", font=self.custom_font).grid(row=3, column=0, padx=10, pady=10, sticky="w")
#         self.scan_type = ctk.CTkOptionMenu(self.input_frame, values=["TCP Connect", "UDP"], width=300, height=30, font=self.custom_font)
#         self.scan_type.grid(row=3, column=1, padx=10, pady=10)
#         self.scan_type.set("TCP Connect")

#         # Timeout
#         ctk.CTkLabel(self.input_frame, text="Time out (s) :", font=self.custom_font).grid(row=4, column=0, padx=10, pady=10, sticky="w")
#         self.entry_timeout = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
#         self.entry_timeout.insert(0, "0.5")
#         self.entry_timeout.grid(row=4, column=1, padx=10, pady=10)

#         # Results table frame
#         self.table_frame = ctk.CTkFrame(self.root)
#         self.table_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
#         # Create custom style for treeview
#         style = ttk.Style()
#         style.configure("Treeview", 
#                         background="#1A1A1A", 
#                         foreground="white", 
#                         fieldbackground="#1A1A1A",
#                         borderwidth=1)
#         style.configure("Treeview.Heading", 
#                         background="#212121", 
#                         foreground="white",
#                         relief="flat")
#         style.map("Treeview", background=[("selected", "#15375C")])
        
#         # Create treeview for results
#         columns = ('port', 'type', 'port_again', 'status')
#         self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings', height=10)
        
#         # Configure columns
#         self.tree.heading('port', text='Port')
#         self.tree.heading('type', text='Type')
#         self.tree.heading('port_again', text='Port')
#         self.tree.heading('status', text='Status')
        
#         for col in columns:
#             self.tree.column(col, anchor='center', width=150)
        
#         # Add sample data
#         self.tree.insert('', 'end', values=('80', 'TCP /IP', 'TCP /IP', 'Closed'))
#         self.tree.insert('', 'end', values=('43', 'TCP /IP', 'TCP /IP', 'Open'))
        
#         # Configure tag for open ports
#         self.tree.tag_configure('open', background='#E45151')
#         self.tree.tag_configure('closed', background='#1A1A1A')
        
#         # Apply tags to rows
#         for item in self.tree.get_children():
#             if self.tree.item(item)['values'][3] == 'Open':
#                 self.tree.item(item, tags=('open',))
#             else:
#                 self.tree.item(item, tags=('closed',))
                
#         self.tree.pack(fill='both', expand=True)

#         # Buttons
#         button_frame = ctk.CTkFrame(self.root)
#         button_frame.pack(pady=20)
        
#         self.start_button = ctk.CTkButton(button_frame, text="Start Scan", command=self.start_scan, 
#                                           width=150, height=40, font=self.custom_font)
#         self.start_button.pack(side="left", padx=10)
        
#         self.save_button = ctk.CTkButton(button_frame, text="Save Results", command=self.save_results, 
#                                          width=150, height=40, font=self.custom_font)
#         self.save_button.pack(side="left", padx=10)
        
#         self.toggle_button = ctk.CTkButton(button_frame, text="Toggle Theme", command=self.toggle_theme, 
#                                            width=150, height=40, font=self.custom_font)
#         self.toggle_button.pack(side="left", padx=10)

#     def update_theme_colors(self):
#         # Get current theme colors
#         theme_colors = self.colors[self.current_theme]
        
#         # Update main frame
#         self.main_frame.configure(fg_color=theme_colors["upper_bg"])
        
#         # Update input frame
#         self.input_frame.configure(fg_color=theme_colors["upper_bg"])
        
#         # Update circle frame
#         self.circle_frame.configure(fg_color=theme_colors["upper_bg"])
        
#         # Update circle canvas
#         self.circle_canvas.configure(bg=theme_colors["upper_bg"])
        
#         # Update circle elements
#         self.circle_canvas.itemconfig(self.bg_circle, outline=theme_colors["border"])
#         self.circle_canvas.itemconfig(self.arc, outline=theme_colors["dark_blue"])
#         self.circle_canvas.itemconfig(self.percentage_text, fill=theme_colors["text"])
#         self.circle_canvas.itemconfig(self.progress_label, fill=theme_colors["text"])
        
#         # Update time label
#         self.time_label.configure(text_color=theme_colors["text"])
        
#         # Update table frame
#         self.table_frame.configure(fg_color=theme_colors["lower_bg"])
        
#         # Update treeview style
#         style = ttk.Style()
#         style.configure("Treeview", 
#                         background=theme_colors["output_bg"], 
#                         foreground=theme_colors["text"], 
#                         fieldbackground=theme_colors["output_bg"])
#         style.configure("Treeview.Heading", 
#                         background=theme_colors["upper_bg"], 
#                         foreground=theme_colors["text"])
        
#         # Update button frame
#         button_frame = self.toggle_button.master
#         button_frame.configure(fg_color=theme_colors["lower_bg"])
        
#         # Update buttons
#         self.start_button.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"])
#         self.save_button.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"])
#         self.toggle_button.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"])
        
#         # Update entry fields
#         self.entry_host.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
#                                  border_color=theme_colors["border"])
#         self.entry_start_port.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
#                                        border_color=theme_colors["border"])
#         self.entry_end_port.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
#                                      border_color=theme_colors["border"])
#         self.entry_timeout.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
#                                     border_color=theme_colors["border"])
        
#         # Update dropdown
#         self.scan_type.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"], 
#                                 button_color=theme_colors["dark_blue"], dropdown_fg_color=theme_colors["dark_blue"])

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

#         # Clear previous results
#         for item in self.tree.get_children():
#             self.tree.delete(item)
#         self.scan_results.clear()
        
#         # Reset progress
#         self.update_progress(0)
        
#         self.scanning = True
#         threading.Thread(target=self.scan_ports, args=(host, start_port, end_port, timeout), daemon=True).start()

#     def scan_ports(self, host, start_port, end_port, timeout):
#         try:
#             ip = socket.gethostbyname(host)
#         except socket.gaierror:
#             messagebox.showerror("Error", "Invalid hostname or IP address.")
#             self.scanning = False
#             return

#         total_ports = end_port - start_port + 1
#         scanned = 0
        
#         for port in range(start_port, end_port + 1):
#             if self.scan_type.get() == "UDP":
#                 self.scan_udp(ip, port, timeout)
#             else:
#                 self.scan_tcp(ip, port, timeout)
            
#             scanned += 1
#             progress = (scanned / total_ports) * 100
#             self.update_progress(progress)

#         self.scanning = False
#         messagebox.showinfo("Scan Complete", "Port scan completed!")

#     def scan_tcp(self, ip, port, timeout):
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(timeout)
#             result = sock.connect_ex((ip, port))
#             if result == 0:
#                 status = "Open"
#                 tag = "open"
#             else:
#                 status = "Closed"
#                 tag = "closed"
#             sock.close()
            
#             # Insert result in treeview
#             item = self.tree.insert('', 'end', values=(port, 'TCP /IP', 'TCP /IP', status))
#             self.tree.item(item, tags=(tag,))
            
#             # Add to results list
#             self.scan_results.append({
#                 'port': port,
#                 'type': 'TCP',
#                 'status': status
#             })
            
#         except Exception as e:
#             print(f"Error scanning port {port}: {e}")

#     def scan_udp(self, ip, port, timeout):
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             sock.settimeout(timeout)
#             sock.sendto(b"\x00", (ip, port))
#             sock.recvfrom(1024)
#             status = "Open"
#             tag = "open"
#         except socket.timeout:
#             status = "Closed"
#             tag = "closed"
#         except Exception as e:
#             status = "Error"
#             tag = "closed"
#             print(f"Error scanning UDP port {port}: {e}")
#         finally:
#             sock.close()
            
#         # Insert result in treeview
#         item = self.tree.insert('', 'end', values=(port, 'UDP', 'UDP', status))
#         self.tree.item(item, tags=(tag,))
        
#         # Add to results list
#         self.scan_results.append({
#             'port': port,
#             'type': 'UDP',
#             'status': status
#         })

#     def update_progress(self, percentage):
#         # Update circular progress
#         angle = (percentage / 100) * 360
#         self.circle_canvas.itemconfig(self.arc, extent=-angle)
#         self.circle_canvas.itemconfig(self.percentage_text, text=f"{int(percentage)}%")
        
#         # Update time taken (in a real app, this would be calculated)
#         elapsed_time = int(percentage / 100 * 60)  # Just for demonstration
#         self.time_label.configure(text=f"Time taken: {elapsed_time} s")

#     def save_results(self):
#         if not self.scan_results:
#             messagebox.showerror("Error", "No results to save.")
#             return
            
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             filetypes=[("CSV Files", "*.csv"), ("JSON Files", "*.json")]
#         )
        
#         if not file_path:
#             return
            
#         try:
#             if file_path.endswith(".json"):
#                 with open(file_path, 'w') as f:
#                     json.dump(self.scan_results, f, indent=2)
#             else:
#                 with open(file_path, 'w', newline='') as f:
#                     writer = csv.DictWriter(f, fieldnames=['port', 'type', 'status'])
#                     writer.writeheader()
#                     writer.writerows(self.scan_results)
                    
#             messagebox.showinfo("Success", "Results saved successfully!")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to save results: {e}")

#     def toggle_theme(self):
#         # Toggle between Dark and Light themes
#         self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        
#         # Update customtkinter appearance mode
#         ctk.set_appearance_mode(self.current_theme)
        
#         # Update custom colors
#         self.update_theme_colors()

# if __name__ == "__main__":
#     root = ctk.CTk()
#     app = PortScannerApp(root)
#     root.mainloop()




















import socket
import threading
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import ttk
import json
import csv

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner Pro")
        self.root.geometry("900x720")
        self.root.resizable(True, True)

        # Theme and colors
        self.current_theme = "Dark"
        ctk.set_appearance_mode(self.current_theme)
        
        # Define color schemes
        self.colors = {
            "Dark": {
                "upper_bg": "#212121",
                "lower_bg": "#242424",
                "blue": "#212121",
                "red": "#E45151",
                "yellow": "#EAFF00",
                "dark_blue": "#15375C",
                "border": "#636363",
                "output_bg": "#FFFFFF",  # Changed from #1A1A1A to #FFFFFF
                "text": "#000000"  # Changed from #FFFFFF to #000000 for better contrast on white
            },
            "Light": {
                "upper_bg": "#FFFFFF",
                "lower_bg": "#D5D7E1",
                "blue": "#212121",
                "red": "#E45151",
                "yellow": "#EAFF00",
                "dark_blue": "#15375C",
                "border": "#EAE8E8",
                "output_bg": "#EAE8E8",
                "text": "#000000"
            }
        }
        
        self.scanning = False
        self.scan_results = []
        self.custom_font = ("Courier New", 12, "bold")
        self.init_ui()
        self.update_theme_colors()

    def init_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, fill="both", expand=True)

        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=20)

        # Circular progress frame
        self.circle_frame = ctk.CTkFrame(self.main_frame, width=200, height=200)
        self.circle_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")
        
        # Create circular progress indicator
        self.circle_canvas = ctk.CTkCanvas(self.circle_frame, width=180, height=180, highlightthickness=0)
        self.circle_canvas.place(x=10, y=10)
        
        # Background circle
        self.bg_circle = self.circle_canvas.create_oval(10, 10, 170, 170, width=15, outline="#636363")
        
        # Progress arc
        self.arc = self.circle_canvas.create_arc(10, 10, 170, 170, start=90, extent=0, style="arc", width=15, outline="#15375C")
        
        # Percentage text
        self.percentage_text = self.circle_canvas.create_text(90, 70, text="60%", font=("Arial", 30, "bold"), fill="#FFFFFF")
        self.progress_label = self.circle_canvas.create_text(90, 110, text="Progress", font=("Arial", 14), fill="#FFFFFF")
        
        # Time taken label
        self.time_label = ctk.CTkLabel(self.circle_frame, text="Time taken: 52 s", font=("Arial", 14))
        self.time_label.place(x=30, y=200)

        # Host input
        ctk.CTkLabel(self.input_frame, text="Target Host/IP :", font=self.custom_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_host = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_host.grid(row=0, column=1, padx=10, pady=10)

        # Port range inputs
        ctk.CTkLabel(self.input_frame, text="Start Port :", font=self.custom_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_start_port = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_start_port.insert(0, "1")
        self.entry_start_port.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.input_frame, text="End Port :", font=self.custom_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_end_port = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_end_port.insert(0, "1024")
        self.entry_end_port.grid(row=2, column=1, padx=10, pady=10)

        # Scan type
        ctk.CTkLabel(self.input_frame, text="Scan Type :", font=self.custom_font).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.scan_type = ctk.CTkOptionMenu(self.input_frame, values=["TCP Connect", "UDP"], width=300, height=30, font=self.custom_font)
        self.scan_type.grid(row=3, column=1, padx=10, pady=10)
        self.scan_type.set("TCP Connect")

        # Timeout
        ctk.CTkLabel(self.input_frame, text="Time out (s) :", font=self.custom_font).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_timeout = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_timeout.insert(0, "0.5")
        self.entry_timeout.grid(row=4, column=1, padx=10, pady=10)

        # Results table frame
        self.table_frame = ctk.CTkFrame(self.root)
        self.table_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        # Create custom style for treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#1A1A1A", 
                        foreground="white", 
                        fieldbackground="#1A1A1A",
                        borderwidth=1)
        style.configure("Treeview.Heading", 
                        background="#212121", 
                        foreground="white",
                        relief="flat")
        style.map("Treeview", background=[("selected", "#15375C")])
        
        # Create treeview for results
        columns = ('port', 'type', 'port_again', 'status')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        self.tree.heading('port', text='Port')
        self.tree.heading('type', text='Type')
        self.tree.heading('port_again', text='Port')
        self.tree.heading('status', text='Status')
        
        for col in columns:
            self.tree.column(col, anchor='center', width=150)
        
        # Add sample data
        self.tree.insert('', 'end', values=('80', 'TCP /IP', 'TCP /IP', 'Closed'))
        self.tree.insert('', 'end', values=('43', 'TCP /IP', 'TCP /IP', 'Open'))
        
        # Configure tag for open ports
        self.tree.tag_configure('open', background='#E45151')
        self.tree.tag_configure('closed', background='#FFFFFF')  # Changed from #1A1A1A to #FFFFFF
        
        # Apply tags to rows
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][3] == 'Open':
                self.tree.item(item, tags=('open',))
            else:
                self.tree.item(item, tags=('closed',))
                
        self.tree.pack(fill='both', expand=True)

        # Buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = ctk.CTkButton(button_frame, text="Start Scan", command=self.start_scan, 
                                          width=150, height=40, font=self.custom_font)
        self.start_button.pack(side="left", padx=10)
        
        self.save_button = ctk.CTkButton(button_frame, text="Save Results", command=self.save_results, 
                                         width=150, height=40, font=self.custom_font)
        self.save_button.pack(side="left", padx=10)
        
        self.toggle_button = ctk.CTkButton(button_frame, text="Toggle Theme", command=self.toggle_theme, 
                                           width=150, height=40, font=self.custom_font)
        self.toggle_button.pack(side="left", padx=10)

    def update_theme_colors(self):
        # Get current theme colors
        theme_colors = self.colors[self.current_theme]
        
        # Update main frame
        self.main_frame.configure(fg_color=theme_colors["upper_bg"])
        
        # Update input frame
        self.input_frame.configure(fg_color=theme_colors["upper_bg"])
        
        # Update circle frame
        self.circle_frame.configure(fg_color=theme_colors["upper_bg"])
        
        # Update circle canvas
        self.circle_canvas.configure(bg=theme_colors["upper_bg"])
        
        # Update circle elements
        self.circle_canvas.itemconfig(self.bg_circle, outline=theme_colors["border"])
        self.circle_canvas.itemconfig(self.arc, outline=theme_colors["dark_blue"])
        self.circle_canvas.itemconfig(self.percentage_text, fill=theme_colors["text"])
        self.circle_canvas.itemconfig(self.progress_label, fill=theme_colors["text"])
        
        # Update time label
        self.time_label.configure(text_color=theme_colors["text"])
        
        # Update table frame
        self.table_frame.configure(fg_color=theme_colors["lower_bg"])
        
        # Update treeview style
        style = ttk.Style()
        style.configure("Treeview", 
                        background=theme_colors["output_bg"], 
                        foreground=theme_colors["text"], 
                        fieldbackground=theme_colors["output_bg"])
        style.configure("Treeview.Heading", 
                        background=theme_colors["upper_bg"], 
                        foreground=theme_colors["text"])
        
        # Update button frame
        button_frame = self.toggle_button.master
        button_frame.configure(fg_color=theme_colors["lower_bg"])
        
        # Update buttons
        self.start_button.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"])
        self.save_button.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"])
        self.toggle_button.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"])
        
        # Update entry fields
        self.entry_host.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
                                 border_color=theme_colors["border"])
        self.entry_start_port.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
                                       border_color=theme_colors["border"])
        self.entry_end_port.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
                                     border_color=theme_colors["border"])
        self.entry_timeout.configure(fg_color=theme_colors["upper_bg"], text_color=theme_colors["text"], 
                                    border_color=theme_colors["border"])
        
        # Update dropdown
        self.scan_type.configure(fg_color=theme_colors["dark_blue"], text_color=theme_colors["text"], 
                                button_color=theme_colors["dark_blue"], dropdown_fg_color=theme_colors["dark_blue"])

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

        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.scan_results.clear()
        
        # Reset progress
        self.update_progress(0)
        
        self.scanning = True
        threading.Thread(target=self.scan_ports, args=(host, start_port, end_port, timeout), daemon=True).start()

    def scan_ports(self, host, start_port, end_port, timeout):
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            messagebox.showerror("Error", "Invalid hostname or IP address.")
            self.scanning = False
            return

        total_ports = end_port - start_port + 1
        scanned = 0
        
        for port in range(start_port, end_port + 1):
            if self.scan_type.get() == "UDP":
                self.scan_udp(ip, port, timeout)
            else:
                self.scan_tcp(ip, port, timeout)
            
            scanned += 1
            progress = (scanned / total_ports) * 100
            self.update_progress(progress)

        self.scanning = False
        messagebox.showinfo("Scan Complete", "Port scan completed!")

    def scan_tcp(self, ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                status = "Open"
                tag = "open"
            else:
                status = "Closed"
                tag = "closed"
            sock.close()
            
            # Insert result in treeview
            item = self.tree.insert('', 'end', values=(port, 'TCP /IP', 'TCP /IP', status))
            self.tree.item(item, tags=(tag,))
            
            # Add to results list
            self.scan_results.append({
                'port': port,
                'type': 'TCP',
                'status': status
            })
            
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

    def scan_udp(self, ip, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(b"\x00", (ip, port))
            sock.recvfrom(1024)
            status = "Open"
            tag = "open"
        except socket.timeout:
            status = "Closed"
            tag = "closed"
        except Exception as e:
            status = "Error"
            tag = "closed"
            print(f"Error scanning UDP port {port}: {e}")
        finally:
            sock.close()
            
        # Insert result in treeview
        item = self.tree.insert('', 'end', values=(port, 'UDP', 'UDP', status))
        self.tree.item(item, tags=(tag,))
        
        # Add to results list
        self.scan_results.append({
            'port': port,
            'type': 'UDP',
            'status': status
        })

    def update_progress(self, percentage):
        # Update circular progress
        angle = (percentage / 100) * 360
        self.circle_canvas.itemconfig(self.arc, extent=-angle)
        self.circle_canvas.itemconfig(self.percentage_text, text=f"{int(percentage)}%")
        
        # Update time taken (in a real app, this would be calculated)
        elapsed_time = int(percentage / 100 * 60)  # Just for demonstration
        self.time_label.configure(text=f"Time taken: {elapsed_time} s")

    def save_results(self):
        if not self.scan_results:
            messagebox.showerror("Error", "No results to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("JSON Files", "*.json")]
        )
        
        if not file_path:
            return
            
        try:
            if file_path.endswith(".json"):
                with open(file_path, 'w') as f:
                    json.dump(self.scan_results, f, indent=2)
            else:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['port', 'type', 'status'])
                    writer.writeheader()
                    writer.writerows(self.scan_results)
                    
            messagebox.showinfo("Success", "Results saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {e}")

    def toggle_theme(self):
        # Toggle between Dark and Light themes
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        
        # Update customtkinter appearance mode
        ctk.set_appearance_mode(self.current_theme)
        
        # Update custom colors
        self.update_theme_colors()

if __name__ == "__main__":
    root = ctk.CTk()
    app = PortScannerApp(root)
    root.mainloop()




