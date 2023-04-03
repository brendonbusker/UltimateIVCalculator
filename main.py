import tkinter as t
import tkinter.messagebox
import requests


class IVCalc:
    def __init__(self):
        #Main window
        self.main_window = t.Tk()
        self.main_window.geometry("700x400")
        self.main_window.title("Ultimate IV Calculator")

        #Frames
        self.enter_pokemon_frame = t.Frame(self.main_window)
        self.enter_level_frame = t.Frame(self.main_window)
        self.stats_label_frame = t.Frame(self.main_window)
        self.enter_stats_frame = t.Frame(self.main_window)
        self.enter_ev_frame = t.Frame(self.main_window)
        self.enter_nature_frame = t.Frame(self.main_window)
        self.iv_frame = t.Frame(self.main_window)
        self.calc_frame = t.Frame(self.main_window)


        #Enter Pokemon
        self.pokemon_label = t.Label(self.enter_pokemon_frame, text = "Enter Pokemon: ")
        self.pokemon_entry = t.Entry(self.enter_pokemon_frame, width = 20)
        self.pokemon_label.pack(side = "left")
        self.pokemon_entry.pack(side = "left")

        #Enter Level
        self.level_label = t.Label(self.enter_level_frame, text = "Level:")
        self.level_entry = t.Entry(self.enter_level_frame, width = 10)
        self.level_label.pack(side = "left")
        self.level_entry.pack(side = "left")

        #Stats Label
        self.hp_label = t.Label(self.stats_label_frame, text = "HP")
        self.atk_label = t.Label(self.stats_label_frame, text = "ATK")
        self.def_label = t.Label(self.stats_label_frame, text = "DEF")
        self.spatk_label = t.Label(self.stats_label_frame, text = "SP ATK")
        self.spdef_label = t.Label(self.stats_label_frame, text = "SP DEF")
        self.spd_label = t.Label(self.stats_label_frame, text = "SPD")
        self.hp_label.pack(side = "left")
        self.atk_label.pack(side = "left")
        self.def_label.pack(side = "left")
        self.spatk_label.pack(side = "left")
        self.spdef_label.pack(side = "left")
        self.spd_label.pack(side = "left")
        
        #Enter Stats
        



        #Calculate Button
        self.login_button = t.Button(self.login_frame, text = "Login", command = self.access_database, width = 20)
        self.login_button.pack(side = "top")
        

        #Pack Frames
        self.enter_pokemon_frame.pack()
        self.enter_level_frame.pack()
        self.stats_label_frame.pack()
        self.enter_stats_frame.pack()
        self.enter_ev_frame.pack()
        self.enter_nature_frame.pack()
        self.iv_frame.pack()
        self.calc_frame.pack()


        #Loop
        t.mainloop()

    def access_database(self):
        print()


#Run GUI
RunIVCalc = IVCalc()
