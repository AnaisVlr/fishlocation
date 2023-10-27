import math
import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
from AutoCompleteSearchBar import AutoCompleteSearchBar
from main import zones, nouveau_df, listPoisson


# Code from https://github.com/TomSchimansky/TkinterMapView/blob/main/examples/map_view_demo.py
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
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        """

        #Search bar pour trouver un poisson
        self.search_fish_bar = tkinter.Entry(self, width=50)
        self.search_fish_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_fish_bar.focus()
        """
        self.search_fish_bar = AutoCompleteSearchBar(self, listPoisson)

        self.search_fish_bar_button = tkinter.Button(master=self, width=8, text="Find fish", command=self.search_fish)
        self.search_fish_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_fish_bar_clear = tkinter.Button(master=self, width=8, text="Clear", command=self.clear_fish)
        self.search_fish_bar_clear.grid(row=0, column=2, pady=10, padx=10)

        # Recherche avancee
        self.filtre_frame = tkinter.Frame(master=self)
        self.filtre_frame.grid(row=1, column=1)

        self.filtre_isActive = tkinter.BooleanVar()
        self.filtre_checkbox_active = tkinter.Checkbutton(master=self.filtre_frame, text='Recherche Avancée',
                                                          variable=self.filtre_isActive, onvalue=True, offvalue=False)
        self.filtre_checkbox_active.grid()

        self.filtre_ville_label = tkinter.Label(master=self.filtre_frame, text="Ville :")
        self.filtre_ville_label.grid()

        self.filtre_ville_entry = tkinter.Entry(master=self.filtre_frame)
        self.filtre_ville_entry.grid()

        self.filtre_radius_label = tkinter.Label(master=self.filtre_frame, text="Radius (km) :")
        self.filtre_radius_label.grid()

        self.filtre_radius_entry = tkinter.Scale(master=self.filtre_frame, from_=0, to=200, orient=tkinter.HORIZONTAL)
        self.filtre_radius_entry.grid()

        # Info sur le cote
        self.info_frame = tkinter.Frame(master=self)
        self.info_frame.grid(row=2, column=2)

        self.info_label = tkinter.Label(master=self.info_frame, text="Nombre de résultats :")
        self.info_label.grid()

        self.info_number = tkinter.Label(master=self.info_frame, text="")
        self.info_number.grid()

        # Map
        self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # self.map_widget.set_address("NYC")
        self.map_widget.set_position(43.66106, 3.80563)

        self.marker_list = []
        self.marker_path = None

        self.search_marker = None
        self.search_in_progress = False

        # Création des lieux de prélèvement
        for coord_key, zone in zones.items():
            latitude, longitude = coord_key
            # Récupérer les poissons trouvés à cette position
            poissons = zone["poissons"]
            poissons_str = [str(poisson) for poisson in poissons]
            texte_poissons = "\n".join(poissons_str)
            # Ajouter un marqueur sur la carte
            self.marker_list.append(self.map_widget.set_marker(latitude, longitude, text=texte_poissons))

    def updateFilterFrame(self, poissons_filtres):
        nb_res = len(poissons_filtres)
        print(nb_res)
        self.info_number.config(text=str(nb_res))

    def search_fish(self, event=None):
        self.clear_marker_list()
        # Obtenir le nom du poisson recherché
        poisson = self.search_fish_bar.getInput()
        if poisson is not None:
            # Filtrer le dataframe pour ne garder que les lignes qui correspondent au poisson recherché
            poissons_filtres = nouveau_df[nouveau_df['vernacularName'] == poisson]
            # Obtenir les emplacements où le poisson a été trouvé

            if self.filtre_isActive.get():
                poissons_filtres = self.filtre(poissons_filtres)

            self.updateFilterFrame(poissons_filtres)

            emplacements = poissons_filtres[['decimalLatitude', 'decimalLongitude']]

            # Afficher les emplacements sur la carte
            for _, row in emplacements.iterrows():
                latitude = row['decimalLatitude']
                longitude = row['decimalLongitude']

                self.marker_list.append(self.map_widget.set_marker(latitude, longitude, text=poisson))
            self.map_widget.set_position(emplacements.iat[0, 0], emplacements.iat[0, 1])

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

        self.map_widget.delete_all_marker()
        lat, lon = self.map_widget.get_position()
        print(lat, lon)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()

    def radius_cal(self, lat, km):
        # Rayon de la Terre en kilomètres
        earth_radius_km = 6371.0

        # Conversion de kilomètres en radians
        lat_in_radians = math.radians(lat)

        # Calcul du rayon en degrés de latitude et de longitude
        lat_degrees = (km / earth_radius_km) * (180.0 / math.pi)
        lon_degrees = (km / (earth_radius_km * math.cos(lat_in_radians))) * (180.0 / math.pi)

        return lat_degrees, lon_degrees

    def filtre(self, poissons):
        print("on filtre mass")
        ville = self.filtre_ville_entry.get()
        self.map_widget.set_address(ville+",France")
        radius = self.filtre_radius_entry.get()
        lat, lon = self.map_widget.get_position()
        print(lat,lon)
        latDiff, lonDiff = self.radius_cal(lat, radius)
        poissons = poissons[poissons['decimalLatitude'] > (lat - latDiff)]
        poissons = poissons[poissons['decimalLatitude'] < (lat + latDiff)]

        poissons = poissons[poissons['decimalLongitude'] > (lon - lonDiff)]
        poissons = poissons[poissons['decimalLongitude'] < (lon + lonDiff)]
        return poissons


if __name__ == "__main__":
    app = App()
    app.start()
