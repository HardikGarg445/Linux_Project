import socket
import threading
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import ttk
import json
import csv
import time

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner Pro")
        self.root.geometry("900x720")
        self.root.resizable(True, True)

        # start in Light theme
        self.current_theme = "Light"
        ctk.set_appearance_mode(self.current_theme)

        # define our color palettes
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
                "output_bg": "#FFFFFF",  # white background for results
                "text": "#000000"
            }
        }

        self.scanning = False
        self.scan_results = []
        self.custom_font = ("Courier New", 12, "bold")

        self.init_ui()
        self.update_theme_colors()

    def init_ui(self):
        # main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, fill="both", expand=True)

        # inputs
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # circular progress
        self.circle_frame = ctk.CTkFrame(self.main_frame, width=200, height=200)
        self.circle_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")
        self.circle_canvas = ctk.CTkCanvas(self.circle_frame, width=180, height=180, highlightthickness=0)
        self.circle_canvas.place(x=10, y=10)
        self.bg_circle      = self.circle_canvas.create_oval(10,10,170,170, width=15, outline="#636363")
        self.arc            = self.circle_canvas.create_arc(10,10,170,170, start=90, extent=0,
                                                          style="arc", width=15, outline="#15375C")
        self.percentage_txt = self.circle_canvas.create_text(90,70,  text="0%", 
                                                             font=("Arial",30,"bold"), fill="#FFFFFF")
        self.label_txt      = self.circle_canvas.create_text(90,110, text="Progress",
                                                             font=("Arial",14),      fill="#FFFFFF")
        self.time_label     = ctk.CTkLabel(self.circle_frame, text="Time taken: 0 s", font=("Arial",14))
        self.time_label.place(x=30, y=200)

        # input fields
        labels = ["Target Host/IP :", "Start Port :", "End Port :", "Scan Type :", "Timeout (s):"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(self.input_frame, text=text, font=self.custom_font)\
               .grid(row=i, column=0, padx=10, pady=5, sticky="w")

        self.entry_host       = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_start_port = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_end_port   = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.entry_timeout    = ctk.CTkEntry(self.input_frame, width=300, height=30, font=self.custom_font)
        self.scan_type        = ctk.CTkOptionMenu(self.input_frame,
                                                  values=["TCP Connect","UDP"],
                                                  width=300, height=30, font=self.custom_font)

        self.entry_host.grid(row=0, column=1, padx=10, pady=5)
        self.entry_start_port.insert(0, "1")
        self.entry_start_port.grid(row=1, column=1, padx=10, pady=5)
        self.entry_end_port.insert(0, "1024")
        self.entry_end_port.grid(row=2, column=1, padx=10, pady=5)

        self.scan_type.set("TCP Connect")
        self.scan_type.grid(row=3, column=1, padx=10, pady=5)

        self.entry_timeout.insert(0, "0.5")
        self.entry_timeout.grid(row=4, column=1, padx=10, pady=5)

        # results table
        self.table_frame = ctk.CTkFrame(self.root)
        self.table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        # base Treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=self.colors["Light"]["output_bg"],
                        foreground=self.colors["Light"]["text"],
                        fieldbackground=self.colors["Light"]["output_bg"],
                        borderwidth=1)
        style.configure("Treeview.Heading",
                        background=self.colors["Light"]["upper_bg"],
                        foreground=self.colors["Light"]["text"],
                        relief="flat")
        style.map("Treeview", background=[("selected", self.colors["Light"]["dark_blue"])])

        cols = ("port","type","port_again","status")
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # initial tag colors (will be overridden)
        self.tree.tag_configure('open',   background=self.colors["Light"]["red"])
        self.tree.tag_configure('closed', background=self.colors["Light"]["output_bg"])

        # buttons
        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(pady=20)
        self.start_button  = ctk.CTkButton(btn_frame, text="Start Scan",
                                           command=self.start_scan, width=150, height=40,
                                           font=self.custom_font)
        self.save_button   = ctk.CTkButton(btn_frame, text="Save Results",
                                           command=self.save_results, width=150, height=40,
                                           font=self.custom_font)
        self.toggle_button = ctk.CTkButton(btn_frame, text="Toggle Theme",
                                           command=self.toggle_theme, width=150, height=40,
                                           font=self.custom_font)

        for b in (self.start_button, self.save_button, self.toggle_button):
            b.pack(side="left", padx=10)

    def update_theme_colors(self):
        """Reconfigure all colors for current theme, including tag backgrounds."""
        tc = self.colors[self.current_theme]

        # frames and canvas
        self.main_frame.configure(fg_color=tc["upper_bg"])
        self.input_frame.configure(fg_color=tc["upper_bg"])
        self.circle_frame.configure(fg_color=tc["upper_bg"])
        self.circle_canvas.configure(bg=tc["upper_bg"])
        self.circle_canvas.itemconfig(self.bg_circle, outline=tc["border"])
        self.circle_canvas.itemconfig(self.arc, outline=tc["dark_blue"])
        self.circle_canvas.itemconfig(self.percentage_txt, fill=tc["text"])
        self.circle_canvas.itemconfig(self.label_txt, fill=tc["text"])
        self.time_label.configure(text_color=tc["text"])

        # table background
        self.table_frame.configure(fg_color=tc["lower_bg"])
        style = ttk.Style()
        style.configure("Treeview",
                        background=tc["output_bg"],
                        foreground=tc["text"],
                        fieldbackground=tc["output_bg"])
        style.configure("Treeview.Heading",
                        background=tc["upper_bg"],
                        foreground=tc["text"])

        # tag colors: closed = output_bg, open = red
        self.tree.tag_configure('closed', background=tc["output_bg"])
        self.tree.tag_configure('open',   background=tc["red"])

        # buttons
        btn_frame = self.toggle_button.master
        btn_frame.configure(fg_color=tc["lower_bg"])
        for btn in (self.start_button, self.save_button, self.toggle_button):
            btn.configure(fg_color=tc["dark_blue"], text_color="#FFFFFF")

        # entries
        for entry in (self.entry_host, self.entry_start_port,
                      self.entry_end_port, self.entry_timeout):
            entry.configure(fg_color=tc["upper_bg"], text_color=tc["text"], border_color=tc["border"])

        # dropdown
        self.scan_type.configure(
            fg_color=tc["dark_blue"],
            text_color="#FFFFFF",
            button_color=tc["dark_blue"],
            dropdown_fg_color=tc["dark_blue"],
            dropdown_text_color="#FFFFFF"
        )

    def start_scan(self):
        if self.scanning:
            return
        host = self.entry_host.get().strip()
        try:
            sp = int(self.entry_start_port.get())
            ep = int(self.entry_end_port.get())
            to = float(self.entry_timeout.get())
        except ValueError:
            return messagebox.showerror("Input Error", "Please enter valid ports and timeout.")
        if not host:
            return messagebox.showerror("Input Error", "Enter a host or IP.")

        # clear old
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.scan_results.clear()
        self.update_progress(0)

        self.scanning = True
        self.start_time = time.time()
        threading.Thread(target=self.scan_ports, args=(host, sp, ep, to), daemon=True).start()

    def scan_ports(self, host, start_port, end_port, timeout):
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror:
            self.scanning = False
            return messagebox.showerror("Error", "Invalid host/IP.")
        total = end_port - start_port + 1
        for idx, port in enumerate(range(start_port, end_port+1), 1):
            if self.scan_type.get() == "UDP":
                self._scan_udp(ip, port, timeout)
            else:
                self._scan_tcp(ip, port, timeout)
            self.update_progress((idx/total)*100)

        elapsed = round(time.time()-self.start_time,2)
        self.scanning = False
        self.time_label.configure(text=f"Time taken: {elapsed} s")
        messagebox.showinfo("Done", "Scan complete!")

    def _scan_tcp(self, ip, port, timeout):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            res = s.connect_ex((ip, port))
            status = "Open" if res==0 else "Closed"
            s.close()
        except:
            status = "Error"
        tag = 'open' if status=="Open" else 'closed'
        self.tree.insert('', 'end', values=(port,'TCP','TCP',status), tags=(tag,))
        self.scan_results.append({'port':port,'type':'TCP','status':status})

    def _scan_udp(self, ip, port, timeout):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(timeout)
            s.sendto(b"\x00",(ip,port))
            s.recvfrom(1024)
            status = "Open"
        except socket.timeout:
            status = "Closed"
        except:
            status = "Error"
        finally:
            s.close()
        tag = 'open' if status=="Open" else 'closed'
        self.tree.insert('', 'end', values=(port,'UDP','UDP',status), tags=(tag,))
        self.scan_results.append({'port':port,'type':'UDP','status':status})

    def update_progress(self, pct):
        angle = (pct/100)*360
        self.circle_canvas.itemconfig(self.arc, extent=-angle)
        self.circle_canvas.itemconfig(self.percentage_txt, text=f"{int(pct)}%")

    def save_results(self):
        if not self.scan_results:
            return messagebox.showerror("Error", "No results to save.")
        fp = filedialog.asksaveasfilename(defaultextension=".csv",
                                          filetypes=[("CSV","*.csv"),("JSON","*.json")])
        if not fp:
            return
        try:
            if fp.lower().endswith(".json"):
                with open(fp,"w") as f:
                    json.dump(self.scan_results, f, indent=2)
            else:
                with open(fp,"w",newline="") as f:
                    w = csv.DictWriter(f, fieldnames=['port','type','status'])
                    w.writeheader()
                    w.writerows(self.scan_results)
            messagebox.showinfo("Saved", "Results saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")

    def toggle_theme(self):
        self.current_theme = "Dark" if self.current_theme=="Light" else "Light"
        ctk.set_appearance_mode(self.current_theme)
        self.update_theme_colors()

if __name__ == "__main__":
    root = ctk.CTk()
    app  = PortScannerApp(root)
    root.mainloop()
