'''
WELCOME!
This is expopunch's Ultimate IV Calculator

Currently this is version alpha 1.1

Shoutout to PokeAPI!

'''


import tkinter as t
import tkinter.messagebox
import customtkinter
import requests
import os
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

NATURES = ['Adamant', 'Bashful', 'Bold', 'Brave', 'Calm', 'Careful',
            'Docile', 'Gentle', 'Hardy', 'Hasty', 'Impish', 'Jolly', 'Lax',
            'Lonely', 'Mild', 'Modest', 'Naive', 'Naughty', 'Quiet', 'Quirky',
            'Rash', 'Relaxed', 'Sassy', 'Serious', 'Timid']



class CalcIV(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Ultimate IV Calculator")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ultimate IV Calculator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(20), pady=(20, 10))
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=140)
        self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text = "Sidebar button 2")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Color Theme:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.colortheme_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Blue", "Dark-Blue", "Green"],
                                                               command=self.change_color_event)
        self.colortheme_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create calc frame with widgets
        self.calc_frame = customtkinter.CTkFrame(self, width=250)
        self.calc_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.pokemon_label = customtkinter.CTkLabel(self.calc_frame, text=" Enter Pokemon:")
        self.pokemon_label.grid(row=0, column=0, padx=(20,10), pady=(10,0))
        self.pokemon_entry = customtkinter.CTkEntry(self.calc_frame)
        self.pokemon_entry.grid(row=0,column=1, padx=10, pady=(10,0))
        self.level_label = customtkinter.CTkLabel(self.calc_frame, text="Enter Level:", anchor="w")
        self.level_label.grid(row=1, column=0, padx=(0,10), pady=(10,0))
        self.level_entry = customtkinter.CTkEntry(self.calc_frame, width=38)
        self.level_entry.grid(row=1,column=1, padx=10, pady=(10,0))
        self.nature_label = customtkinter.CTkLabel(self.calc_frame, text="   Enter Nature:", anchor="w")
        self.nature_label.grid(row=2, column=0, padx=(0,10), pady=(10,0))
        self.nature_optionmenu = customtkinter.CTkOptionMenu(self.calc_frame, values=NATURES)
        self.nature_optionmenu.grid(row=2, column=1, padx=(10,10), pady=(10,0))

        self.dummy_label2 = customtkinter.CTkLabel(self.calc_frame, text="")
        self.dummy_label2.grid(row=0, column=2, padx=30)

        self.dummy_label1 = customtkinter.CTkLabel(self.calc_frame, text="")
        self.dummy_label1.grid(row=0, column=3, padx=20, pady=(10,0))

        self.hp_label = customtkinter.CTkLabel(self.calc_frame, text="HP:")
        self.hp_label.grid(row=1, column=3, padx=(20,10), pady=(5,0))
        self.atk_label = customtkinter.CTkLabel(self.calc_frame, text="ATK:")
        self.atk_label.grid(row=2, column=3, padx=(20,10), pady=(5,0))
        self.def_label = customtkinter.CTkLabel(self.calc_frame, text="DEF:")
        self.def_label.grid(row=3, column=3, padx=(20,10), pady=(5,0))
        self.spatk_label = customtkinter.CTkLabel(self.calc_frame, text="SPATK:")
        self.spatk_label.grid(row=4, column=3, padx=(20,10), pady=(5,0))
        self.spdef_label = customtkinter.CTkLabel(self.calc_frame, text="SPDEF:")
        self.spdef_label.grid(row=5, column=3, padx=(20,10), pady=(5,0))
        self.spd_label = customtkinter.CTkLabel(self.calc_frame, text="SPD:")
        self.spd_label.grid(row=6, column=3, padx=(20,10), pady=(5,0))

        self.stats_label = customtkinter.CTkLabel(self.calc_frame, text="Stats", font=customtkinter.CTkFont(underline=True))
        self.stats_label.grid(row=0, column=4, padx=(10,10), pady=(0,0))

        self.hp_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text=" HP", width=38)
        self.hp_entry.grid(row=1, column=4, padx=2, pady=5)
        self.atk_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="ATK", width=38)
        self.atk_entry.grid(row=2, column=4, padx=2, pady=5)
        self.def_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="DEF", width=38)
        self.def_entry.grid(row=3, column=4, padx=2, pady=5)
        self.spatk_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="SPATK", width=38)
        self.spatk_entry.grid(row=4, column=4, padx=2, pady=5)
        self.spdef_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="SDEF", width=38)
        self.spdef_entry.grid(row=5, column=4, padx=2, pady=5)
        self.spd_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="SPD", width=38)
        self.spd_entry.grid(row=6, column=4, padx=2, pady=5)


        self.ev_label = customtkinter.CTkLabel(self.calc_frame, text="EVs", font=customtkinter.CTkFont(underline=True))
        self.ev_label.grid(row=0, column=5, padx=(10,10), pady=(0,0))

        self.ev_hp_entry = customtkinter.CTkEntry(self.calc_frame, width=38)
        self.ev_hp_entry.grid(row=1, column=5, padx=2, pady=5)
        self.ev_atk_entry = customtkinter.CTkEntry(self.calc_frame, width=38)
        self.ev_atk_entry.grid(row=2, column=5, padx=2, pady=5)
        self.ev_def_entry = customtkinter.CTkEntry(self.calc_frame, width=38)
        self.ev_def_entry.grid(row=3, column=5, padx=2, pady=5)
        self.ev_spatk_entry = customtkinter.CTkEntry(self.calc_frame, width=38)
        self.ev_spatk_entry.grid(row=4, column=5, padx=2, pady=5)
        self.ev_spdef_entry = customtkinter.CTkEntry(self.calc_frame, width=38)
        self.ev_spdef_entry.grid(row=5, column=5, padx=2, pady=5)
        self.ev_spd_entry = customtkinter.CTkEntry(self.calc_frame, width=38)
        self.ev_spd_entry.grid(row=6, column=5, padx=2, pady=5)

        self.calc_button = customtkinter.CTkButton(self.calc_frame, text="Calculate", command=self.calcIV)
        self.calc_button.grid(row=3, column=1, padx=(10,10), pady=(10,10))


        # enter stats and ev frame with widgets
        self.iv_frame = customtkinter.CTkFrame(self, width=250)
        self.iv_frame.grid(row=1, column=1, padx=(20,0), pady=(20,0), sticky="nsew")

        self.dummy_label3 = customtkinter.CTkLabel(self.iv_frame, text="")
        self.dummy_label3.grid(row=0, column=0)

        self.hp_label = customtkinter.CTkLabel(self.iv_frame, text="HP:")
        self.hp_label.grid(row=1, column=0, padx=(20,10), pady=(5,0))
        self.atk_label = customtkinter.CTkLabel(self.iv_frame, text="ATK:")
        self.atk_label.grid(row=2, column=0, padx=(20,10), pady=(5,0))
        self.def_label = customtkinter.CTkLabel(self.iv_frame, text="DEF:")
        self.def_label.grid(row=3, column=0, padx=(20,10), pady=(5,0))
        self.spatk_label = customtkinter.CTkLabel(self.iv_frame, text="SPATK:")
        self.spatk_label.grid(row=4, column=0, padx=(20,10), pady=(5,0))
        self.spdef_label = customtkinter.CTkLabel(self.iv_frame, text="SPDEF:")
        self.spdef_label.grid(row=5, column=0, padx=(20,10), pady=(5,0))
        self.spd_label = customtkinter.CTkLabel(self.iv_frame, text="SPD:")
        self.spd_label.grid(row=6, column=0, padx=(20,10), pady=(5,0))

        self.iv_label = customtkinter.CTkLabel(self.iv_frame, text="Possible IVs", font=customtkinter.CTkFont(underline=True))
        self.iv_label.grid(row=0, column=2, padx=(10,10), pady=(0,0))

        self.iv_hp_var = customtkinter.IntVar()
        self.iv_atk_var = customtkinter.IntVar()
        self.iv_def_var = customtkinter.IntVar()
        self.iv_spatk_var = customtkinter.IntVar()
        self.iv_spdef_var = customtkinter.IntVar()
        self.iv_spd_var = customtkinter.IntVar()

        self.iv_hp_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.iv_hp_var)
        self.iv_hp_entry.grid(row=1, column=2, padx=2, pady=5)
        self.iv_atk_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.iv_atk_var)
        self.iv_atk_entry.grid(row=2, column=2, padx=2, pady=5)
        self.iv_def_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.iv_def_var)
        self.iv_def_entry.grid(row=3, column=2, padx=2, pady=5)
        self.iv_spatk_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.iv_spatk_var)
        self.iv_spatk_entry.grid(row=4, column=2, padx=2, pady=5)
        self.iv_spdef_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.iv_spdef_var)
        self.iv_spdef_entry.grid(row=5, column=2, padx=2, pady=5)
        self.iv_spd_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.iv_spd_var)
        self.iv_spd_entry.grid(row=6, column=2, padx=2, pady=5)

        self.iv_label = customtkinter.CTkLabel(self.iv_frame, text="Base Stats", font=customtkinter.CTkFont(underline=True))
        self.iv_label.grid(row=0, column=1, padx=(10,10), pady=(0,0))

        self.base_hp_var = customtkinter.IntVar()
        self.base_atk_var = customtkinter.IntVar()
        self.base_def_var = customtkinter.IntVar()
        self.base_spatk_var = customtkinter.IntVar()
        self.base_spdef_var = customtkinter.IntVar()
        self.base_spd_var = customtkinter.IntVar()

        self.base_hp_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.base_hp_var)
        self.base_hp_entry.grid(row=1, column=1, padx=2, pady=5)
        self.base_atk_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.base_atk_var)
        self.base_atk_entry.grid(row=2, column=1, padx=2, pady=5)
        self.base_def_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.base_def_var)
        self.base_def_entry.grid(row=3, column=1, padx=2, pady=5)
        self.base_spatk_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.base_spatk_var)
        self.base_spatk_entry.grid(row=4, column=1, padx=2, pady=5)
        self.base_spdef_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.base_spdef_var)
        self.base_spdef_entry.grid(row=5, column=1, padx=2, pady=5)
        self.base_spd_entry = customtkinter.CTkEntry(self.iv_frame, width=50, textvariable=self.base_spd_var)
        self.base_spd_entry.grid(row=6, column=1, padx=2, pady=5)



        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)


        # create image frame
        self.image_frame = customtkinter.CTkFrame(self, width=250)
        self.image_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.image_label1 = customtkinter.CTkLabel(self.image_frame, text="Pokemon Image:", font=customtkinter.CTkFont(underline=True))
        self.image_label1.grid(row=0, column=0)



        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.textbox.insert("0.0", "Changelog\n\n" + "This is currently not functional.\n\n" * 20)
        self.appearance_mode_optionemenu.set("System")
        self.colortheme_optionmenu.set("Green")
        self.colortheme_optionmenu.configure(state='disabled')
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.nature_optionmenu.set("Adamant")
        self.level_entry.insert(0,100)
        self.ev_hp_entry.insert(0, 0)
        self.ev_atk_entry.insert(0, 0)
        self.ev_def_entry.insert(0, 0)
        self.ev_spatk_entry.insert(0, 0)
        self.ev_spdef_entry.insert(0, 0)
        self.ev_spd_entry.insert(0, 0)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_color_event(self, color: str):
        customtkinter.set_default_color_theme(color.lower())

    def sidebar_button_event(self):
        print("sidebar_button click")

    def calcIV(self):
        #API
        usr_input = self.pokemon_entry.get().lower()
        nature = self.nature_optionmenu.get().lower()
        poke_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{usr_input}")
        nature_response = requests.get(f"https://pokeapi.co/api/v2/nature/{nature}")
        pokemon = poke_response.json()
        nature_dict = nature_response.json()

        #Sprite
        sprite = pokemon['sprites']['front_default']
        pokeimage = customtkinter.CTkImage(Image.open(requests.get(sprite, stream=True).raw), size=(192,192))


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

        #Set IVs to gui
        self.iv_hp_var.set(iv_hp)
        self.iv_atk_var.set(iv_atk)
        self.iv_def_var.set(iv_def)
        self.iv_spatk_var.set(iv_spatk)
        self.iv_spdef_var.set(iv_spdef)
        self.iv_spd_var.set(iv_spd)

        # set base stats to gui
        self.base_hp_var.set(base_hp)
        self.base_atk_var.set(base_atk)
        self.base_def_var.set(base_def)
        self.base_spatk_var.set(base_spatk)
        self.base_spdef_var.set(base_spdef)
        self.base_spd_var.set(base_spd)


        #Set image
        self.image_label2 = customtkinter.CTkLabel(self.image_frame, text="", image=pokeimage)
        self.image_label2.grid(row=1, column=0)

    # calc hp IV
    def CalcHp(self, stat_hp, base_hp, ev_hp, level):
        iv_hp = ((stat_hp - 10) * 100) / level - 2*base_hp - ev_hp/4 - 100
        return iv_hp
    
    # calc other stats IV
    def CalcStats(self, stat, base, ev, level):
        iv = ((stat - 5) * 100) / level - 2 * base - ev/4
        return iv

if __name__ == "__main__":
    app = CalcIV()
    app.mainloop()