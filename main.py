'''
WELCOME!
This is expopunch's Ultimate IV Calculator

Currently this is version alpha 1.0

Shoutout to PokeAPI!

'''

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
        self.calc_frame = t.Frame(self.main_window)


        #Enter Pokemon
        self.pokemon_label = t.Label(self.enter_pokemon_frame, text = "Enter Pokemon: ")
        self.pokemon_entry = t.Entry(self.enter_pokemon_frame, width = 20)
        self.pokemon_label.pack(side = "left")
        self.pokemon_entry.pack(side = "left")

        #Enter Level
        self.level_label = t.Label(self.enter_level_frame, text = "Level:")
        self.level_entry = t.Entry(self.enter_level_frame, width = 5)
        self.level_entry.insert(0, 100)
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
        self.stats_label = t.Label(self.enter_stats_frame, text = "Stats:")
        self.hp_entry = t.Entry(self.enter_stats_frame, width = 5)
        self.atk_entry = t.Entry(self.enter_stats_frame, width = 5)
        self.def_entry = t.Entry(self.enter_stats_frame, width = 5)
        self.spatk_entry = t.Entry(self.enter_stats_frame, width = 5)
        self.spdef_entry = t.Entry(self.enter_stats_frame, width = 5)
        self.spd_entry = t.Entry(self.enter_stats_frame, width = 5)

        self.hp_entry.insert(0, 0)
        self.atk_entry.insert(0, 0)
        self.def_entry.insert(0, 0)
        self.spatk_entry.insert(0, 0)
        self.spdef_entry.insert(0, 0)
        self.spd_entry.insert(0, 0)

        self.stats_label.pack(side = "left")
        self.hp_entry.pack(side = "left")
        self.atk_entry.pack(side = "left")
        self.def_entry.pack(side = "left")
        self.spatk_entry.pack(side = "left")
        self.spdef_entry.pack(side = "left")
        self.spd_entry.pack(side = "left")

        #Enter EV
        self.ev_label = t.Label(self.enter_ev_frame, text = "EVs:   ")
        self.ev_hp_entry = t.Entry(self.enter_ev_frame, width = 5)
        self.ev_atk_entry = t.Entry(self.enter_ev_frame, width = 5)
        self.ev_def_entry = t.Entry(self.enter_ev_frame, width = 5)
        self.ev_spatk_entry = t.Entry(self.enter_ev_frame, width = 5)
        self.ev_spdef_entry = t.Entry(self.enter_ev_frame, width = 5)
        self.ev_spd_entry = t.Entry(self.enter_ev_frame, width = 5)

        self.ev_hp_entry.insert(0, 0)
        self.ev_atk_entry.insert(0, 0)
        self.ev_def_entry.insert(0, 0)
        self.ev_spatk_entry.insert(0, 0)
        self.ev_spdef_entry.insert(0, 0)
        self.ev_spd_entry.insert(0, 0)


        self.ev_label.pack(side = "left")
        self.ev_hp_entry.pack(side = "left")
        self.ev_atk_entry.pack(side = "left")
        self.ev_def_entry.pack(side = "left")
        self.ev_spatk_entry.pack(side = "left")
        self.ev_spdef_entry.pack(side = "left")
        self.ev_spd_entry.pack(side = "left")

        #Enter Nature
        self.nature_label = t.Label(self.enter_nature_frame, text = "Nature:")
        self.nature_entry = t.Entry(self.enter_nature_frame, width = 10)

        self.nature_label.pack(side = "left")
        self.nature_entry.pack(side = "left")

        #Calculate Button
        self.login_button = t.Button(self.calc_frame, text = "Calculate", command = self.calcIV, width = 20)
        self.login_button.pack(side = "top")
        

        #Pack Frames
        self.enter_pokemon_frame.pack()
        self.enter_level_frame.pack()
        self.stats_label_frame.pack()
        self.enter_stats_frame.pack()
        self.enter_ev_frame.pack()
        self.enter_nature_frame.pack()
        self.calc_frame.pack()


        #Loop
        t.mainloop()

    def calcIV(self):
        #API
        usr_input = self.pokemon_entry.get().lower()
        nature = self.nature_entry.get().lower()
        poke_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{usr_input}")
        nature_response = requests.get(f"https://pokeapi.co/api/v2/nature/{nature}")
        pokemon = poke_response.json()
        nature_dict = nature_response.json()

        #Base Stats
        base_hp = pokemon['stats'][0]['base_stat']
        base_atk = pokemon['stats'][1]['base_stat']
        base_def = pokemon['stats'][2]['base_stat']
        base_spatk = pokemon['stats'][3]['base_stat']
        base_spdef = pokemon['stats'][4]['base_stat']
        base_spd = pokemon['stats'][5]['base_stat']

        #Pokemon Stats
        stat_hp = int(self.hp_entry.get())
        stat_atk = int(self.atk_entry.get())
        stat_def = int(self.def_entry.get())
        stat_spatk = int(self.spatk_entry.get())
        stat_spdef = int(self.spdef_entry.get())
        stat_spd = int(self.spd_entry.get())

        #Pokemon EVs
        ev_hp = int(self.ev_hp_entry.get())
        ev_atk = int(self.ev_atk_entry.get())
        ev_def = int(self.ev_def_entry.get())
        ev_spatk = int(self.ev_spatk_entry.get())
        ev_spdef = int(self.ev_spdef_entry.get())
        ev_spd = int(self.ev_spd_entry.get())

        #Level
        level = int(self.level_entry.get())

        #Nature inc stat, dec stat
        if nature == "hardy" or nature == "docile" or nature == "bashful" or nature == "quirky" or nature == "serious":
            inc_stat = ""
            dec_stat = ""

        else:
            inc_stat = nature_dict['increased_stat']['name']
            dec_stat = nature_dict['decreased_stat']['name']

        #Adjust stats for nature
        if inc_stat == "special-attack":
            stat_spatk = stat_spatk / 1.1
        
        elif inc_stat == "attack":
            stat_atk = stat_atk / 1.1

        elif inc_stat == "speed":
            stat_spd = stat_spd / 1.1

        elif inc_stat == "special-defense":
            stat_spdef = stat_spdef / 1.1

        elif inc_stat == "defense":
            stat_def = stat_def / 1.1

        if dec_stat == "special-attack":
            stat_spatk = stat_spatk / 0.9
        
        elif dec_stat == "attack":
            stat_atk = stat_atk / 0.9

        elif dec_stat == "speed":
            stat_spd = stat_spd / 0.9

        elif dec_stat == "special-defense":
            stat_spdef = stat_spdef / 0.9

        elif dec_stat == "defense":
            stat_def = stat_def / 0.9

        #Get IVs
        iv_hp = round(self.CalcHp(stat_hp, base_hp, ev_hp, level))
        iv_atk = round(self.CalcStats(stat_atk, base_atk, ev_atk, level))
        iv_def = round(self.CalcStats(stat_def, base_def, ev_def, level))
        iv_spatk = round(self.CalcStats(stat_spatk, base_spatk, ev_spatk, level))
        iv_spdef = round(self.CalcStats(stat_spdef, base_spdef, ev_spdef, level))
        iv_spd = round(self.CalcStats(stat_spd, base_spd, ev_spd, level))

        #Displays IVs
        tkinter.messagebox.showinfo("IVs", f"HP: {iv_hp}, ATK: {iv_atk}, DEF: {iv_def}, SPATK: {iv_spatk}, SPDEF: {iv_spdef}, SPD: {iv_spd}")


    #Calc HP IV
    def CalcHp(self, stat_hp, base_hp, ev_hp, level):
        iv_hp = ((stat_hp - 10) * 100) / level - 2*base_hp - ev_hp/4 - 100
        return iv_hp
    
    def CalcStats(self, stat, base, ev, level):
        iv = ((stat - 5) * 100) / level - 2 * base - ev/4
        return iv


        



#Run GUI
RunIVCalc = IVCalc()
