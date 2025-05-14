import socket     # used for network connections 
import threading   # used for running scans in background without freezing the scan 
import customtkinter as ctk   # used for better  ui looks
from tkinter import messagebox, filedialog # used for popup box and saving files option 
from tkinter import ttk # used for adding widets, for displaying 
import json # for saving results in json format
import csv  # for saving results in csv files 
import time # for measuring scan time 

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner Pro") # window title
        self.root.geometry("900x720")    # size of appearing window 
        self.root.resizable(True, True)   # it allows user to resize 

        # Theme settings for light and dark mode 
        self.current_theme = "Light"
        ctk.set_appearance_mode(self.current_theme)

        # color schemes
        self.colors = {
            "Dark": {
                "upper_bg": "#212121",
                "lower_bg": "#242424",
                "red": "#E45151",
                "dark_blue": "#15375C",
                "border": "#636363",
                "output_bg": "#1A1A1A",
                "text": "#FFFFFF"
            },
            "Light": {
                "upper_bg": "#FFFFFF",
                "lower_bg": "#D5D7E1",
                "red": "#E45151",
                "dark_blue": "#15375C",
                "border": "#EAE8E8",
                "output_bg": "#FFFFFF",
                "text": "#000000"
            }
        }

        # Scan control variables
        self.scanning = False    # Flag to check if scanning is active
        self.stop_event = threading.Event()   # Used to stop the scan thread
        self.scan_results = []    # Stores port scan results
        self.custom_font = ("Courier New", 12, "bold")   # Font style
        self.start_time = 0      # To track scan duration

        self.init_ui()    # Initialize the UI
        self.update_theme_colors()   # Apply theme colors

    def init_ui(self):
        # Main container frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, fill="both", expand=True)

        # Left frame (input fields)
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=0, column=0, padx=50, pady=50, sticky="nw")

        # Right frame (progress circle)
        self.circle_frame = ctk.CTkFrame(self.main_frame, width=200, height=200)
        self.circle_frame.grid(row=0, column=1, padx=110, pady=50, sticky="ne")

        # Canvas for the progress circle
        self.circle_canvas = ctk.CTkCanvas(self.circle_frame, width=180, height=180, highlightthickness=0)
        self.circle_canvas.pack()
        self.bg_circle = self.circle_canvas.create_oval(10, 10, 170, 170, width=15, outline="#636363")
        self.arc = self.circle_canvas.create_arc(10, 10, 170, 170, start=90, extent=0, style="arc", width=15, outline="#15375C")  # blue circle arc making 
        self.percentage_txt = self.circle_canvas.create_text(90, 70, text="0%", font=("Arial", 30, "bold"), fill="#FFFFFF")    # Percentage text
        self.label_txt = self.circle_canvas.create_text(90, 110, text="Progress", font=("Arial", 14), fill="#FFFFFF")    # Label text

        # Time elapsed label
        self.time_label = ctk.CTkLabel(self.circle_frame, text="Time Elapsed: 0 s", font=("Arial", 14))
        self.time_label.pack(pady=(10, 0))

        # labels for taking input , field
        labels = ["Target Host/IP :", "Start Port :", "End Port :", "Scan Type :", "Timeout (s):"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(self.input_frame, text=text, font=self.custom_font).grid(row=i, column=0, padx=10, pady=5, sticky="w")

        # Entry fields 
        self.entry_host = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_start_port = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_end_port = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_timeout = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.scan_type = ctk.CTkOptionMenu(self.input_frame, values=["TCP Connect", "UDP"], width=300, height=30, font=self.custom_font)

        # Place input fields in the grid
        self.entry_host.grid(row=0, column=1, padx=10, pady=5)
        self.entry_start_port.insert(0, "1")
        self.entry_start_port.grid(row=1, column=1, padx=10, pady=5)
        self.entry_end_port.insert(0, "1024")
        self.entry_end_port.grid(row=2, column=1, padx=10, pady=5)
        self.scan_type.set("TCP Connect")
        self.scan_type.grid(row=3, column=1, padx=10, pady=5)
        self.entry_timeout.insert(0, "0.5")
        self.entry_timeout.grid(row=4, column=1, padx=10, pady=5)

        # Frame for the results table
        self.table_frame = ctk.CTkFrame(self.root)
        self.table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        # Styling the Treeview (table)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=self.colors["Light"]["output_bg"],
                        foreground=self.colors["Light"]["text"],
                        rowheight=25,
                        fieldbackground=self.colors["Light"]["output_bg"],
                        borderwidth=1)
        style.configure("Treeview.Heading",
                        background=self.colors["Light"]["upper_bg"],
                        foreground=self.colors["Light"]["text"],
                        relief="flat")
        style.configure("Vertical.TScrollbar", gripcount=0,
                        background=self.colors["Light"]["dark_blue"],
                        troughcolor=self.colors["Light"]["lower_bg"],
                        bordercolor=self.colors["Light"]["border"],
                        arrowcolor=self.colors["Light"]["text"])

        # Defining the table columns (replaced "port_again" with "service")
        cols = ("port", "type", "service", "status")
        self.tree_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", style="Vertical.TScrollbar")
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings", yscrollcommand=self.tree_scrollbar.set, height=10)
        self.tree_scrollbar.config(command=self.tree.yview)

        # Configuring the table columns
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=120, anchor="center")

        # Place table in the UI
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_scrollbar.grid(row=0, column=1, sticky="ns")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        # Color tags for open/closed ports
        self.tree.tag_configure('open', background=self.colors["Light"]["red"])  # Red for open ports
        self.tree.tag_configure('closed', background=self.colors["Light"]["output_bg"]) # Default for closed 

        # Button frame
        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(pady=20)

        # Scan button (starts/stops scanning)
        self.start_button = ctk.CTkButton(btn_frame, text="Start Scan", command=self.toggle_scan, width=150, height=40, font=self.custom_font)

        # Save button (exports results to CSV/JSON)
        self.save_button = ctk.CTkButton(btn_frame, text="Save Results", command=self.save_results, width=150, height=40, font=self.custom_font)

        # Theme toggle button (Light/Dark mode)
        self.toggle_button = ctk.CTkButton(btn_frame, text="Toggle Theme", command=self.toggle_theme, width=150, height=40, font=self.custom_font)

        # Pack buttons side by side
        for b in (self.start_button, self.save_button, self.toggle_button):
            b.pack(side="left", padx=10)

    def toggle_scan(self):
        if self.scanning:   # If already scanning, stop it
            self.stop_event.set()    # Signal the thread to stop
            self.start_button.configure(text="Start Scan")    # Reset button text
        else:      # If not scanning, start it
            self.start_scan() 

    def start_scan(self):
        host = self.entry_host.get().strip()    # Get target host/IP
        try:
            sp = int(self.entry_start_port.get())  # Start port
            ep = int(self.entry_end_port.get())    # End port
            to = float(self.entry_timeout.get())   # Timeout
        except ValueError:
            return messagebox.showerror("Input Error", "Please enter valid ports and timeout.")
        if not host:
            return messagebox.showerror("Input Error", "Enter a host or IP.")

        # Clear previous results
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.scan_results.clear()
        self.update_progress(0)   # Reset progress circle

        # Start scanning in a new thread
        self.stop_event.clear()  # Reset stop flag
        self.scanning = True   # Set scanning flag
        self.start_button.configure(text="Stop Scan")   # Update button text
        self.start_time = time.time()    # Record start time
        self.update_timer()  # Start the timer
        threading.Thread(target=self.scan_ports, args=(host, sp, ep, to), daemon=True).start()

    def update_timer(self):
        if self.scanning:
            elapsed = round(time.time() - self.start_time, 2)
            self.time_label.configure(text=f"Time taken: {elapsed} s")    #printing the time taken 
            self.root.after(500, self.update_timer)

    def scan_ports(self, host, start_port, end_port, timeout):
        try:
            ip = socket.gethostbyname(host)     # Resolve hostname to IP
        except socket.gaierror:
            self.scanning = False
            self.start_button.configure(text="Start Scan")
            return messagebox.showerror("Error", "Invalid host/IP.")
        total = end_port - start_port + 1     # Total ports to scan

        for idx, port in enumerate(range(start_port, end_port + 1), 1):
            if self.stop_event.is_set():  # If stop requested, break
                break
            if self.scan_type.get() == "UDP":    # UDP scan
                self._scan_udp(ip, port, timeout)
            else:
                self._scan_tcp(ip, port, timeout)   # TCP scan
            self.update_progress((idx / total) * 100)       # Update progress circle

        self.scanning = False
        self.start_button.configure(text="Start Scan")
        if not self.stop_event.is_set():    # If not stopped manually
            messagebox.showinfo("Done", "Scan complete!")

    def _scan_tcp(self, ip, port, timeout):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # TCP socket
            s.settimeout(timeout)
            res = s.connect_ex((ip, port))  # Try to connect
            status = "Open" if res == 0 else "Closed"    # Check if port is open
            s.close()
        except:
            status = "Error"     # If connection fails
        
        # Get service name (new addition)
        service = self.get_service_name(port, 'tcp')
        tag = 'open' if status == "Open" else 'closed'
        self.tree.insert('', 'end', values=(port, 'TCP', service, status), tags=(tag,))   # adding to the table 
        self.scan_results.append({'port': port, 'type': 'TCP', 'service': service, 'status': status})    # Store result

    def _scan_udp(self, ip, port, timeout):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # UDP socket
            s.settimeout(timeout)
            s.sendto(b"\x00", (ip, port))   # Send empty UDP packet
            s.recvfrom(1024)   # Try to receive response
            status = "Open"   # If response received, port is open
        except socket.timeout:
            status = "Closed"   # No response = likely closed
        except:
            status = "Error" # Other errors
        finally:
            s.close()

        # Get service name (new addition)
        service = self.get_service_name(port, 'udp')
        tag = 'open' if status == "Open" else 'closed'
        self.tree.insert('', 'end', values=(port, 'UDP', service, status), tags=(tag,))    # Add to table
        self.scan_results.append({'port': port, 'type': 'UDP', 'service': service, 'status': status})    # Store result

    def get_service_name(self, port, protocol):
        """Returns the service name for a given port and protocol (tcp/udp)."""
        try:
            return socket.getservbyport(port, protocol)
        except:
            return "Unknown"

    def update_progress(self, pct):
        angle = (pct / 100) * 360    # Convert percentage to degrees
        self.circle_canvas.itemconfig(self.arc, extent=-angle)      # Update arc
        self.circle_canvas.itemconfig(self.percentage_txt, text=f"{int(pct)}%")    # Update text

    def save_results(self):
        if not self.scan_results:
            return messagebox.showerror("Error", "No results to save.")
        # Ask user for file location
        fp = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV", "*.csv"), ("JSON", "*.json")])
        if not fp:
            return
        try:
            if fp.lower().endswith(".json"):  # Save as JSON
                with open(fp, "w") as f:
                    json.dump(self.scan_results, f, indent=2)
            else:      # Save as CSV
                with open(fp, "w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=['port', 'type', 'service', 'status'])
                    w.writeheader()
                    w.writerows(self.scan_results)
            messagebox.showinfo("Saved", "Results saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")

    def toggle_theme(self):
        self.current_theme = "Dark" if self.current_theme == "Light" else "Light"    # Toggle theme
        ctk.set_appearance_mode(self.current_theme)     # Apply theme
        self.update_theme_colors()   # Update all UI colors

    def update_theme_colors(self):
        # Update all UI elements
        tc = self.colors[self.current_theme]
        self.main_frame.configure(fg_color=tc["upper_bg"])
        self.input_frame.configure(fg_color=tc["upper_bg"])
        self.circle_frame.configure(fg_color=tc["upper_bg"])
        self.circle_canvas.configure(bg=tc["upper_bg"])
        self.circle_canvas.itemconfig(self.bg_circle, outline=tc["border"])
        self.circle_canvas.itemconfig(self.arc, outline=tc["dark_blue"])
        self.circle_canvas.itemconfig(self.percentage_txt, fill=tc["text"])
        self.circle_canvas.itemconfig(self.label_txt, fill=tc["text"])
        self.time_label.configure(text_color=tc["text"])
        self.table_frame.configure(fg_color=tc["lower_bg"])

        # Update Treeview (table) styling
        style = ttk.Style()
        style.configure("Treeview", background=tc["output_bg"], foreground=tc["text"], fieldbackground=tc["output_bg"])
        style.configure("Treeview.Heading", background=tc["upper_bg"], foreground=tc["text"])
        style.configure("Vertical.TScrollbar", background=tc["dark_blue"], troughcolor=tc["lower_bg"],
                        arrowcolor=tc["text"], bordercolor=tc["border"])
        self.tree.tag_configure('closed', background=tc["output_bg"])
        self.tree.tag_configure('open', background=tc["red"])
        btn_frame = self.toggle_button.master
        btn_frame.configure(fg_color=tc["lower_bg"])
        for btn in (self.start_button, self.save_button, self.toggle_button):
            btn.configure(fg_color=tc["dark_blue"], text_color="#FFFFFF")
        for entry in (self.entry_host, self.entry_start_port, self.entry_end_port, self.entry_timeout):
            entry.configure(fg_color=tc["upper_bg"], text_color=tc["text"], border_color=tc["border"])
        self.scan_type.configure(fg_color=tc["dark_blue"], text_color="#FFFFFF",
                                button_color=tc["dark_blue"], dropdown_fg_color=tc["dark_blue"],
                                dropdown_text_color="#FFFFFF")

if __name__ == "__main__":
    root = ctk.CTk()     # Create main window
    app = PortScannerApp(root)     # Initialize app
    root.mainloop()     # Start GUI event loop