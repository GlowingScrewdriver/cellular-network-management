import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from cellular_network_operator import CellularNetworkOperator


class CellularNetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cellular Network Management System")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.configure(".", background="#f0f4f8")
        self.style.configure("Custom.TButton",
                             background="#4a90e2",
                             foreground="black")
        self.style.configure("Home.TButton",
                             background="#2ecc71",
                             foreground="black",
                             padding=10)

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

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self.home_frame = self.create_home_tab()
        self.register_device_frame = self.create_register_device_tab()
        self.register_user_frame = self.create_register_user_tab()
        self.purchase_plan_frame = self.create_purchase_plan_tab()
        self.tower_usage_frame = self.create_tower_usage_tab()
        self.view_data_frame = self.create_view_data_tab()


    def create_home_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Home')

        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ttk.Label(content_frame,
                          text="Cellular Network Database\nManagement System",
                          font=('Helvetica', 24, 'bold'),
                          justify='center')
        title.pack(pady=20)

        subtitle = ttk.Label(content_frame,
                             text="Welcome to the management interface",
                             font=('Helvetica', 14))
        subtitle.pack(pady=10)

        buttons = [
            ("Register Device", 1),
            ("Register User", 2),
            ("Purchase Plan", 3),
            ("Record Tower Usage", 4),
            ("View Data", 5)
        ]

        for text, tab_index in buttons:
            btn = ttk.Button(content_frame,
                             text=text,
                             style="Custom.TButton",
                             command=lambda idx=tab_index: self.notebook.select(idx))
            btn.pack(pady=10, padx=20, fill='x')

        return frame

    def add_home_button(self, frame, content_frame):
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

        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Register New Device", font=('Helvetica', 14, 'bold')).grid(row=0, column=0,
                                                                                                  columnspan=2,
                                                                                                  pady=10)

        ttk.Label(content_frame, text="Device Type:").grid(row=1, column=0, padx=5, pady=5)
        # Add None as an option in the combobox
        device_type = ttk.Combobox(content_frame, values=['smartphone', 'featurephone', 'None'])
        device_type.set("None")  # Set default value to None
        device_type.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="IMEI (15 digits):").grid(row=2, column=0, padx=5, pady=5)
        imei_entry = ttk.Entry(content_frame)
        imei_entry.grid(row=2, column=1, padx=5, pady=5)

        def register_device():
            try:
                # Convert 'None' string to None type
                device_type_value = None if device_type.get() == 'None' else device_type.get()
                self.network.register_device(
                    device_type_value,
                    imei_entry.get()
                )
                messagebox.showinfo("Success", "Device registered successfully!")
                imei_entry.delete(0, tk.END)
                device_type.set('None')
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
            ('Identity Proof(Number):', 'identity_proof'), ('IMEI:', 'imei')
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

        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Purchase New Plan", font=('Helvetica', 14, 'bold')).grid(row=0, column=0,
                                                                                                columnspan=2,
                                                                                                pady=10)

        ttk.Label(content_frame, text="Plan ID:").grid(row=1, column=0, padx=5, pady=5)
        plans = {
            "Balanced (ID: 1)": "1",
            "Entertainment (ID: 2)": "2",
            "Talk-time Add On (ID: 3)": "3",
            "Data Add On (ID: 4)": "4"
        }
        plan_id_combobox = ttk.Combobox(content_frame, values=list(plans.keys()), state="readonly")
        plan_id_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="IMEI:").grid(row=2, column=0, padx=5, pady=5)
        imei_entry = ttk.Entry(content_frame)
        imei_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="Phone Number:").grid(row=3, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(content_frame)
        phone_entry.grid(row=3, column=1, padx=5, pady=5)

        def purchase_plan():
            try:
                # Get the selected Plan ID from the combobox
                selected_plan = plan_id_combobox.get()
                plan_id = plans.get(selected_plan)  # Extract the numeric ID

                # Call network purchase plan method
                self.network.purchase_plan(
                    int(plan_id),
                    imei_entry.get(),
                    phone_entry.get()
                )
                messagebox.showinfo("Success", "Plan purchased successfully!")
                plan_id_combobox.set('')  # Reset combobox selection
                imei_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        purchase_btn = ttk.Button(content_frame, text="Purchase Plan", style="Custom.TButton", command=purchase_plan)
        purchase_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # Adding a 'Home' button function (assuming it exists in the class)
        self.add_home_button(frame, content_frame)
        return frame

    def create_tower_usage_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Record Tower Usage')

        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Record Tower Usage", font=('Helvetica', 14, 'bold')).grid(row=0, column=0,
                                                                                                 columnspan=2,
                                                                                                 pady=10)

        # Input fields for IMEI, Tower ID, and Usage Quantum
        ttk.Label(content_frame, text="IMEI:").grid(row=1, column=0, padx=5, pady=5)
        imei_entry = ttk.Entry(content_frame)
        imei_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="Tower ID:").grid(row=2, column=0, padx=5, pady=5)
        tower_id_entry = ttk.Entry(content_frame)
        tower_id_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(content_frame, text="Usage Quantum:").grid(row=3, column=0, padx=5, pady=5)
        usage_quantum_entry = ttk.Entry(content_frame)
        usage_quantum_entry.grid(row=3, column=1, padx=5, pady=5)

        def record_tower_usage():
            try:
                imei = imei_entry.get()
                tower_id = int(tower_id_entry.get())
                usage_quantum = int(usage_quantum_entry.get())

                # Call the network method to record tower usage
                self.network.record_tower_usage(imei, tower_id, usage_quantum)

                # Show success message
                messagebox.showinfo("Success", "Tower usage recorded successfully!")

                # Clear inputs
                imei_entry.delete(0, tk.END)
                tower_id_entry.delete(0, tk.END)
                usage_quantum_entry.delete(0, tk.END)

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for Tower ID and Usage Quantum.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Button to record tower usage
        record_btn = ttk.Button(content_frame, text="Record Tower Usage", style="Custom.TButton",
                                command=record_tower_usage)
        record_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # Add a 'Home' button to return to the main tab
        self.add_home_button(frame, content_frame)
        return frame

    def create_view_data_tab(self) -> ttk.Frame:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='View Data')

        content_frame = ttk.Frame(frame)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Select Table:").grid(row=0, column=0, padx=5, pady=5)
        tables = ['all users','Available Plans', 'Plan Popularity', 'User Details','User Usage', 'Inactive Users',"Tower Load","Multiple plans","User distribution based on city","Device type distribution","Average tower capacity by business users","Currently running plans"]
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
                # q1
                elif selected == 'Plan Popularity':
                    data = list(self.network.get_table("plan_popularity_"))
                elif selected == 'User Details':
                    phone = simpledialog.askstring("Input", "Enter phone number:")
                    if phone:
                        data = [self.network.get_user_details(phone)]
                    else:
                        return
                elif selected == 'Inactive Users':
                    data = list(self.network.get_idle_users())
                elif selected == 'User Usage':
                    phone = simpledialog.askstring("Input", "Enter phone number:")
                    if phone:
                        data= self.network.get_user_usage(phone)
                    else:
                        return
                elif selected == 'Tower Load':

                    tower_id = simpledialog.askstring("Input", "Enter Tower ID:")

                    if not tower_id or not tower_id.isdigit():
                        messagebox.showerror("Error", "Invalid Tower ID. Please enter a valid integer.")
                        return

                    # Display the tower load
                    data=[{f"Tower Load for Tower ID {tower_id}":self.network.get_tower_load(int(tower_id))},{}]

                elif selected == "Multiple plans":
                    data=list(self.network.get_table("multi_plan_"))

                elif selected == "User distribution based on city":
                    data=list(self.network.get_table("user_distribution_"))

                elif selected == "Device type distribution":
                    data=list(self.network.get_table("device_distribution_"))

                elif selected == "Average tower capacity by business users":
                    data=list(self.network.get_table("avg_tower_capac_bu_"))

                elif selected == "Currently running plans":
                    data=list(self.network.get_table("running_plans_"))

                elif selected == 'all users':
                    data = list(self.network.list_users())


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
