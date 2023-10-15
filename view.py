import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView

from main import zones, nouveau_df

#Code from https://github.com/TomSchimansky/TkinterMapView/blob/main/examples/map_view_demo.py
class App(tkinter.Tk):

    APP_NAME = "fishMap.py"
    WIDTH = 800
    HEIGHT = 750

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #Search bar for position
        self.search_position_bar = tkinter.Entry(self, width=50)
        self.search_position_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_position_bar.focus()

        self.search_position_bar_button = tkinter.Button(master=self, width=8, text="Find position", command=self.search_position)
        self.search_position_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_position_bar_clear = tkinter.Button(master=self, width=8, text="Clear", command=self.clear_position)
        self.search_position_bar_clear.grid(row=0, column=2, pady=10, padx=10)

        #Search bar for fish
        self.search_fish_bar = tkinter.Entry(self, width=50)
        self.search_fish_bar.grid(row=1, column=0, pady=10, padx=10, sticky="we")
        self.search_fish_bar.focus()

        self.search_fish_bar_button = tkinter.Button(master=self, width=8, text="Find fish", command=self.search_fish)
        self.search_fish_bar_button.grid(row=1, column=1, pady=10, padx=10)

        self.search_fish_bar_clear = tkinter.Button(master=self, width=8, text="Clear", command=self.clear_fish)
        self.search_fish_bar_clear.grid(row=1, column=2, pady=10, padx=10)

        #Map
        self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=2, column=0, columnspan=3, sticky="nsew")

        #self.map_widget.set_address("NYC")
        self.map_widget.set_position(43.66106,3.80563)
        self.marker_list = []
        self.marker_path = None

        self.search_marker = None
        self.search_in_progress = False

        # Création des lieux de prélèvement
        for zone in zones:
            self.marker_list.append(self.map_widget.set_marker(zone["latitude"], zone["longitude"], text=""))


    def search_position(self, event=None):
        self.clear_marker_list()
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_position_bar.get()
            self.search_marker = self.map_widget.set_address(address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False
    
    
    def search_fish(self, event=None):
        self.clear_marker_list()
        # Obtenir le nom du poisson recherché
        poisson = self.search_fish_bar.get()
        # Filtrer le dataframe pour ne garder que les lignes qui correspondent au poisson recherché
        poissons_filtres = nouveau_df[nouveau_df['scientificName'] == poisson]
        print(poissons_filtres)
        # Obtenir les emplacements où le poisson a été trouvé
        emplacements = poissons_filtres[['decimalLatitude', 'decimalLongitude']]

        # Afficher les emplacements sur la carte
        for _, row in emplacements.iterrows():
            latitude = row['decimalLatitude']
            longitude = row['decimalLongitude']
            
            self.marker_list.append(self.map_widget.set_marker(latitude, longitude, text=""))
            self.map_widget.set_position(latitude, longitude)
        

    def save_marker(self):
        if self.search_marker is not None:
            self.marker_list.append(self.search_marker)

    def clear_marker_list(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)

        self.marker_list.clear()
        self.connect_marker()

    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def clear_position(self):
        self.search_position_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def clear_fish(self):
        self.search_fish_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
