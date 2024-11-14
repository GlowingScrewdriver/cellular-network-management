import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from cellular_network_operator import CellularNetworkOperator


class CellularNetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cellular Network Management System")
        self.root.geometry("800x600")

        # Set theme colors
        self.style = ttk.Style()
        self.style.configure(".", background="#f0f4f8")  # Light blue-gray background
        self.style.configure("Custom.TButton",
                             background="#4a90e2",  # Blue buttons
                             foreground="black")  # Changed text color to black
        self.style.configure("Home.TButton",
                             background="#2ecc71",  # Green for home button
                             foreground="black",  # Changed text color to black
                             padding=10)

        # Apply background color to root window
        self.root.configure(bg="#f0f4f8")

        try:
            self.network = CellularNetworkOperator(
                host='127.0.0.1',
                user='root',
                password='pass',
                database='cellular_network'
            )
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            root.destroy()
            return

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Create tabs
        self.home_frame = self.create_home_tab()
        self.register_device_frame = self.create_register_device_tab()
        self.register_user_frame = self.create_register_user_tab()
        self.purchase_plan_frame = self.create_purchase_plan_tab()
        self.view_data_frame = self.create_view_data_tab()

    def create_home_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Home')

        # Create centered content
        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = ttk.Label(content_frame,
                          text="Cellular Network Database\nManagement System",
                          font=('Helvetica', 24, 'bold'),
                          justify='center')
        title.pack(pady=20)

        # Subtitle
        subtitle = ttk.Label(content_frame,
                             text="Welcome to the management interface",
                             font=('Helvetica', 14))
        subtitle.pack(pady=10)

        # Navigation buttons
        buttons = [
            ("Register Device", 1),
            ("Register User", 2),
            ("Purchase Plan", 3),
            ("View Data", 4)
        ]

        for text, tab_index in buttons:
            btn = ttk.Button(content_frame,
                             text=text,
                             style="Custom.TButton",
                             command=lambda idx=tab_index: self.notebook.select(idx))
            btn.pack(pady=10, padx=20, fill='x')

        return frame

    def add_home_button(self, frame, content_frame):
        # Create a container frame for the home button
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=100, column=0, columnspan=3, sticky='se', padx=10, pady=10)

        home_btn = ttk.Button(button_frame,
                              text="Back to Home",
                              style="Home.TButton",
                              command=lambda: self.notebook.select(0))
        home_btn.pack(side='right')

    def create_register_device_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Register Device')

        # Create centered content frame
        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Register New Device", font=('Helvetica', 14, 'bold')).grid(row=0, column=0,
                                                                                                  columnspan=2,
                                                                                                  pady=10)

        ttk.Label(content_frame, text="Device Type:").grid(row=1, column=0, padx=5, pady=5)
        device_type = ttk.Combobox(content_frame, values=['smartphone', 'featurephone'])
        device_type.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="IMEI (15 digits):").grid(row=2, column=0, padx=5, pady=5)
        imei_entry = ttk.Entry(content_frame)
        imei_entry.grid(row=2, column=1, padx=5, pady=5)

        def register_device():
            try:
                self.network.register_device(
                    device_type.get(),
                    imei_entry.get()
                )
                messagebox.showinfo("Success", "Device registered successfully!")
                imei_entry.delete(0, tk.END)
                device_type.set('')
            except Exception as e:
                messagebox.showerror("Error", str(e))

        register_btn = ttk.Button(content_frame, text="Register Device", style="Custom.TButton",
                                  command=register_device)
        register_btn.grid(row=3, column=0, columnspan=2, pady=20)

        self.add_home_button(frame, content_frame)
        return frame

    def create_register_user_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Register User')

        # Create centered content frame
        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Register New User", font=('Helvetica', 14, 'bold')).grid(row=0, column=0,
                                                                                                columnspan=2,
                                                                                                pady=10)

        fields = [
            ('Name:', 'name'), ('Phone:', 'phone'),
            ('Apartment:', 'apt_name'), ('Street:', 'street_name'),
            ('City:', 'city'), ('Pincode:', 'pincode'),
            ('State:', 'state'), ('Email:', 'email'),
            ('Identity Proof:', 'identity_proof'), ('IMEI:', 'imei')
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(content_frame, text=label).grid(row=i + 1, column=0, padx=5, pady=5)
            entry = ttk.Entry(content_frame)
            entry.grid(row=i + 1, column=1, padx=5, pady=5)
            entries[key] = entry

        def register_user():
            try:
                self.network.register_user(**{
                    key: entry.get() for key, entry in entries.items()
                })
                messagebox.showinfo("Success", "User registered successfully!")
                for entry in entries.values():
                    entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        register_btn = ttk.Button(content_frame, text="Register User", style="Custom.TButton", command=register_user)
        register_btn.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

        self.add_home_button(frame, content_frame)
        return frame

    def create_purchase_plan_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Purchase Plan')

        # Create centered content frame
        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Purchase New Plan", font=('Helvetica', 14, 'bold')).grid(row=0, column=0,
                                                                                                columnspan=2,
                                                                                                pady=10)

        ttk.Label(content_frame, text="Plan ID:").grid(row=1, column=0, padx=5, pady=5)
        plan_id_entry = ttk.Entry(content_frame)
        plan_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="IMEI:").grid(row=2, column=0, padx=5, pady=5)
        imei_entry = ttk.Entry(content_frame)
        imei_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="Phone Number:").grid(row=3, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(content_frame)
        phone_entry.grid(row=3, column=1, padx=5, pady=5)

        def purchase_plan():
            try:
                self.network.purchase_plan(
                    int(plan_id_entry.get()),
                    imei_entry.get(),
                    phone_entry.get()
                )
                messagebox.showinfo("Success", "Plan purchased successfully!")
                plan_id_entry.delete(0, tk.END)
                imei_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        purchase_btn = ttk.Button(content_frame, text="Purchase Plan", style="Custom.TButton", command=purchase_plan)
        purchase_btn.grid(row=4, column=0, columnspan=2, pady=20)

        self.add_home_button(frame, content_frame)
        return frame

    def create_view_data_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='View Data')

        # Create centered content frame
        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Select Table:").grid(row=0, column=0, padx=5, pady=5)
        tables = ['Available Plans', 'Plan Popularity', 'User Details', 'Inactive Users']
        table_select = ttk.Combobox(content_frame, values=tables)
        table_select.grid(row=0, column=1, padx=5, pady=5)

        tree = ttk.Treeview(content_frame)
        tree.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)

        def load_table_data(event):
            for item in tree.get_children():
                tree.delete(item)

            selected = table_select.get()
            try:
                if selected == 'Available Plans':
                    data = list(self.network.get_plans())
                elif selected == 'Plan Popularity':
                    data = list(self.network.get_plan_popularity())
                elif selected == 'User Details':
                    phone = simpledialog.askstring("Input", "Enter phone number:")
                    if phone:
                        data = [self.network.get_user_details(phone)]
                    else:
                        return
                elif selected == 'Inactive Users':
                    data = list(self.network.get_idle_users())

                if data and len(data) > 0:
                    columns = list(data[0].keys())
                    tree['columns'] = columns
                    tree['show'] = 'headings'

                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=100)

                    for item in data:
                        tree.insert('', 'end', values=list(item.values()))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        table_select.bind('<<ComboboxSelected>>', load_table_data)

        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        self.add_home_button(frame, content_frame)
        return frame


if __name__ == "__main__":
    root = tk.Tk()
    app = CellularNetworkGUI(root)
    root.mainloop()