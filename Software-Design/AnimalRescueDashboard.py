import os
import customtkinter as ctk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkintermapview

# Import the data layer (Model) from my CRUD module: "AnimalRescueCRUD_Enhanced.py"
from AnimalRescueCRUD_Enhanced import AnimalShelter

class DashboardApp(ctk.CTk):
    """
    Visualization and Controller Layer for the Animal Rescue Dashboard.
    Interacts with the AnimalShelter data layer to fetch and render data.
    """
    def __init__(self, db_handler):
        super().__init__()
        self.db = db_handler
        
        self.title("CS-340 Animal Rescue Dashboard - Refactored")
        self.geometry("1200x800")
        
        # Configure the grid layout
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_data = pd.DataFrame()
        
        self.initialize_interface()
        self.apply_filters("reset")  # Load initial data on startup

    def initialize_interface(self):
        # 1. Header Section
        self.header_label = ctk.CTkLabel(self, text="Grazioso Salvare Animal Rescue Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=20)

        # 2. Filter Controls Frame
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.filter_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.filter_var = ctk.StringVar(value="reset")
        
        filters = [
            ("Reset", "reset"),
            ("Water Rescue", "water"),
            ("Mountain/Wilderness Rescue", "mountain"),
            ("Disaster/Individual Tracking", "tracking")
        ]
        
        # Generate radio buttons for user input dynamically
        for i, (text, val) in enumerate(filters):
            rb = ctk.CTkRadioButton(self.filter_frame, text=text, variable=self.filter_var, value=val, command=self.on_filter_change)
            rb.grid(row=0, column=i, padx=20, pady=15)

        # 3. Data Table Frame
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Utilizing ttk.Treeview to render the structured data table
        self.tree = ttk.Treeview(self.table_frame)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # 4. Charts Frame: Pie Chart + Map
        self.charts_frame = ctk.CTkFrame(self)
        self.charts_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.charts_frame.grid_columnconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(1, weight=1)

        # Initialize the interactive map widget
        self.map_widget = tkintermapview.TkinterMapView(self.charts_frame, corner_radius=0, height=300)
        self.map_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.map_widget.set_position(30.75, -97.48)
        self.map_widget.set_zoom(5)

        # Initialize the matplotlib pie chart canvas
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.charts_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def on_filter_change(self):
        """Triggered when a user selects a new radio button filter."""
        selected_filter = self.filter_var.get()
        self.apply_filters(selected_filter)

    def apply_filters(self, filter_type):
        """Fetches data using the secure aggregation pipeline in the CRUD module."""
        if filter_type == 'reset':
            raw_data = self.db.read({})
        else:
            raw_data = self.db.get_rescue_candidates(filter_type)
            
        self.current_data = pd.DataFrame.from_records(raw_data)
        
        # Clean the dataframe for UI rendering
        if '_id' in self.current_data.columns:
            self.current_data.drop(columns=['_id'], inplace=True)

        self.update_visualizations()

    def update_visualizations(self):
        """Updates the table, pie chart, and map based on the current dataset."""
        if self.current_data.empty:
            self.tree.delete(*self.tree.get_children())
            self.ax.clear()
            self.canvas.draw()
            self.map_widget.delete_all_marker()
            return

        # 1. Update Data Table
        self.tree.delete(*self.tree.get_children())
        self.tree["column"] = list(self.current_data.columns)
        self.tree["show"] = "headings"

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for index, row in self.current_data.iterrows():
            self.tree.insert("", "end", values=list(row))

        # 2. Update Pie Chart
        self.ax.clear()
        breed_counts = self.current_data['breed'].value_counts()
        self.ax.pie(breed_counts, labels=breed_counts.index.tolist(), autopct='%1.1f%%', startangle=90)
        self.ax.set_title('Preferred Animals by Breed')
        self.canvas.draw()

        # Reset map markers until a row is selected
        self.map_widget.delete_all_marker()

    def on_row_select(self, event):
        """Updates the geolocation map when a specific row is clicked in the data table."""
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0])['values']
            columns = list(self.current_data.columns)
            
            try:
                lat_idx = columns.index('location_lat')
                long_idx = columns.index('location_long')
                name_idx = columns.index('name')
                
                lat = float(item_values[lat_idx])
                long = float(item_values[long_idx])
                animal_name = item_values[name_idx]
                
                # Update map pin
                self.map_widget.delete_all_marker()
                self.map_widget.set_position(lat, long)
                self.map_widget.set_zoom(12)
                self.map_widget.set_marker(lat, long, text=f"Animal: {animal_name}")
            except ValueError:
                pass # Fail silently if location data is missing for the selected record

if __name__ == "__main__":
    # Pull credentials from system environment variables, instead of hardcoding them, to enhance security and flexibility.
    USER = os.getenv('MONGO_USER', 'aacuser')
    PASS = os.getenv('MONGO_PASS', 'CS340')
    HOST = os.getenv('MONGO_HOST', 'localhost')
    PORT = int(os.getenv('MONGO_PORT', 27017))
    DB = 'aac'
    COL = 'animals'

    # Initialize the Model
    db_handler = AnimalShelter(USER, PASS, HOST, PORT, DB, COL)
    
    # Initialize the View/Controller
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = DashboardApp(db_handler)
    app.mainloop()
  
