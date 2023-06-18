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

#Global Constant
NATURES = ['Adamant', 'Bashful', 'Bold', 'Brave', 'Calm', 'Careful',
            'Docile', 'Gentle', 'Hardy', 'Hasty', 'Impish', 'Jolly', 'Lax',
            'Lonely', 'Mild', 'Modest', 'Naive', 'Naughty', 'Quiet', 'Quirky',
            'Rash', 'Relaxed', 'Sassy', 'Serious', 'Timid']

#Global Variables
pokelist_response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")
all_pokelist = []
pokelist = pokelist_response.json()

for i in range(0, len(pokelist['results'])):
    all_pokelist.append(pokelist['results'][i]['name'].title())

#Changelog Constant
CHANGELOG = '''Beta 1.0

changelog
-finally into beta!
-iv calculator now gives accurate ranges of pokemon ivs
-autocomplete combobox now functional (begin typing and click box to see available pokemon)

notes
-nearing the final version of the calculator soon
-only want to add some more niche things to fill up white space now
-this calculator is essentially fully operational now (and always will be until pokemon changes their equations or PokeAPI stops updating)Alpha 1.2

changelog
-added clear ev button
-added clear stats button
-removed un-useable buttons and tabs
-bulbasaur now default pokemon
-added default and shiny image tabs
-added help tab
-changelog textbox now slightly longer

Alpha 1.1

changelog
-expansive graphical overhaul
-added light and dark modes
-now displays base stats
-built using customtkinter instead of tkinter now
-added changelog textbook
-added sidebuttons (non-functional)
-added tabview (non-functional)
-added color theme button (non-functional)

future additions
-autocomplete for entering in pokemon names
-~~clear ev button~~
-~~clear stats button~~
-more info about pokemon next to base stats and ivs
-etc.

'''

#Help Doc Constant
HELP = '''Help Documentation

Enter Pokemon Error
----------------------------------
-Spelling needs to be correct, 
 so make sure it is.
-If spelling is correct and still
 error, then it's likely that 
 pokemon has a form.
-For example: "Giratina" will not  work, try "Giratina-Altered" or 
 "Giratina-Origin"
-Try the autocomplete,
 start to type the name and click the
 combobox on the side to see available pokemon

IVs not 100% accurate
----------------------------------
-Double check nature, stats
 and EVs entries.

Color theme doesn't work
---------------------------------------
-This is a customtkinter issue
 unsure if it will ever be fixed.

'''



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

        # configure api
        poke_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/bulbasaur")
        pokemon = poke_response.json()
        sprite1 = pokemon['sprites']['front_default']
        sprite2 = pokemon['sprites']['front_shiny']
        pokeimage1 = customtkinter.CTkImage(Image.open(requests.get(sprite1, stream=True).raw), size=(192,192))
        pokeimage2 = customtkinter.CTkImage(Image.open(requests.get(sprite2, stream=True).raw), size=(192,192))



        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ultimate IV Calculator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(20), pady=(20, 10))
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=140, height=300)
        self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.colortheme_label = customtkinter.CTkLabel(self.sidebar_frame, text="Color Theme:", anchor="w")
        self.colortheme_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.colortheme_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Blue", "Dark-Blue", "Green"],
                                                               command=self.change_color_event)
        self.colortheme_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create calc frame with widgets
        self.calc_frame = customtkinter.CTkFrame(self, width=250)
        self.calc_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.pokemon_label = customtkinter.CTkLabel(self.calc_frame, text=" Enter Pokemon:")
        self.pokemon_label.grid(row=0, column=0, padx=(20,10), pady=(10,0))
        self.pokemon_combobox = customtkinter.CTkComboBox(self.calc_frame, values=all_pokelist)
        self.pokemon_combobox.bind('<KeyRelease>', self.update_list)
        self.pokemon_combobox.grid(row=0,column=1, padx=10, pady=(10,0))
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

        self.hp_var = customtkinter.IntVar()
        self.atk_var = customtkinter.IntVar()
        self.def_var = customtkinter.IntVar()
        self.spatk_var = customtkinter.IntVar()
        self.spdef_var = customtkinter.IntVar()
        self.spd_var = customtkinter.IntVar()

        self.hp_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text=" HP", width=38, textvariable=self.hp_var)
        self.hp_entry.grid(row=1, column=4, padx=2, pady=5)
        self.atk_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="ATK", width=38, textvariable=self.atk_var)
        self.atk_entry.grid(row=2, column=4, padx=2, pady=5)
        self.def_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="DEF", width=38, textvariable=self.def_var)
        self.def_entry.grid(row=3, column=4, padx=2, pady=5)
        self.spatk_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="SPATK", width=38, textvariable=self.spatk_var)
        self.spatk_entry.grid(row=4, column=4, padx=2, pady=5)
        self.spdef_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="SDEF", width=38, textvariable=self.spdef_var)
        self.spdef_entry.grid(row=5, column=4, padx=2, pady=5)
        self.spd_entry = customtkinter.CTkEntry(self.calc_frame, placeholder_text="SPD", width=38, textvariable=self.spd_var)
        self.spd_entry.grid(row=6, column=4, padx=2, pady=5)


        self.ev_label = customtkinter.CTkLabel(self.calc_frame, text="EVs", font=customtkinter.CTkFont(underline=True))
        self.ev_label.grid(row=0, column=5, padx=(10,10), pady=(0,0))

        self.ev_hp_var = customtkinter.IntVar()
        self.ev_atk_var = customtkinter.IntVar()
        self.ev_def_var = customtkinter.IntVar()
        self.ev_spatk_var = customtkinter.IntVar()
        self.ev_spdef_var = customtkinter.IntVar()
        self.ev_spd_var = customtkinter.IntVar()

        self.ev_hp_entry = customtkinter.CTkEntry(self.calc_frame, width=38, textvariable=self.ev_hp_var)
        self.ev_hp_entry.grid(row=1, column=5, padx=2, pady=5)
        self.ev_atk_entry = customtkinter.CTkEntry(self.calc_frame, width=38, textvariable=self.ev_atk_var)
        self.ev_atk_entry.grid(row=2, column=5, padx=2, pady=5)
        self.ev_def_entry = customtkinter.CTkEntry(self.calc_frame, width=38, textvariable=self.ev_def_var)
        self.ev_def_entry.grid(row=3, column=5, padx=2, pady=5)
        self.ev_spatk_entry = customtkinter.CTkEntry(self.calc_frame, width=38, textvariable=self.ev_spatk_var)
        self.ev_spatk_entry.grid(row=4, column=5, padx=2, pady=5)
        self.ev_spdef_entry = customtkinter.CTkEntry(self.calc_frame, width=38, textvariable=self.ev_spdef_var)
        self.ev_spdef_entry.grid(row=5, column=5, padx=2, pady=5)
        self.ev_spd_entry = customtkinter.CTkEntry(self.calc_frame, width=38, textvariable=self.ev_spd_var)
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

        self.iv_hp_var = customtkinter.StringVar()
        self.iv_atk_var = customtkinter.StringVar()
        self.iv_def_var = customtkinter.StringVar()
        self.iv_spatk_var = customtkinter.StringVar()
        self.iv_spdef_var = customtkinter.StringVar()
        self.iv_spd_var = customtkinter.StringVar()

        self.iv_hp_entry = customtkinter.CTkEntry(self.iv_frame, width=53, textvariable=self.iv_hp_var)
        self.iv_hp_entry.grid(row=1, column=2, padx=2, pady=5)
        self.iv_atk_entry = customtkinter.CTkEntry(self.iv_frame, width=53, textvariable=self.iv_atk_var)
        self.iv_atk_entry.grid(row=2, column=2, padx=2, pady=5)
        self.iv_def_entry = customtkinter.CTkEntry(self.iv_frame, width=53, textvariable=self.iv_def_var)
        self.iv_def_entry.grid(row=3, column=2, padx=2, pady=5)
        self.iv_spatk_entry = customtkinter.CTkEntry(self.iv_frame, width=53, textvariable=self.iv_spatk_var)
        self.iv_spatk_entry.grid(row=4, column=2, padx=2, pady=5)
        self.iv_spdef_entry = customtkinter.CTkEntry(self.iv_frame, width=53, textvariable=self.iv_spdef_var)
        self.iv_spdef_entry.grid(row=5, column=2, padx=2, pady=5)
        self.iv_spd_entry = customtkinter.CTkEntry(self.iv_frame, width=53, textvariable=self.iv_spd_var)
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



        # create tabview with buttons
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Tools")
        self.tabview.add("Help")
        self.tabview.tab("Tools").grid_columnconfigure(0, weight=1) 
        self.tabview.tab("Help").grid_columnconfigure(0, weight=1)

        self.reset_stats = customtkinter.CTkButton(self.tabview.tab("Tools"), text="Reset Stats", command=self.reset_stats_event)
        self.reset_stats.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.reset_evs = customtkinter.CTkButton(self.tabview.tab("Tools"), text="Reset EVs", command=self.reset_evs_event)
        self.reset_evs.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.help_textbox = customtkinter.CTkTextbox(self.tabview.tab("Help"), width=200, height=180)
        self.help_textbox.grid(row=0, column=0, padx=20, pady=20)


        # create image tabview
        self.image_tabview = customtkinter.CTkTabview(self, width=250)
        self.image_tabview.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.image_tabview.add("Default Sprite")
        self.image_tabview.add("Shiny Sprite")
        self.image_tabview.tab("Default Sprite").grid_columnconfigure(0, weight=1)
        self.image_tabview.tab("Shiny Sprite").grid_columnconfigure(0, weight=1)
        self.image_tabview.grid_columnconfigure(0, weight=1)

        self.image_label1 = customtkinter.CTkLabel(self.image_tabview.tab("Default Sprite"), text="", image=pokeimage1)
        self.image_label1.grid(row=0, column=0)

        self.image_label2 = customtkinter.CTkLabel(self.image_tabview.tab("Shiny Sprite"), text="", image=pokeimage2)
        self.image_label2.grid(row=0, column=0)


        # set default values
        self.textbox.insert("0.0", CHANGELOG)
        self.appearance_mode_optionemenu.set("System")
        self.colortheme_optionmenu.set("Green")
        self.colortheme_optionmenu.configure(state='disabled')
        self.nature_optionmenu.set("Adamant")
        self.level_entry.insert(0,100)
        self.help_textbox.insert("0.0", HELP)
        self.iv_hp_var.set("N/A")
        self.iv_atk_var.set("N/A")
        self.iv_def_var.set("N/A")
        self.iv_spatk_var.set("N/A")
        self.iv_spdef_var.set("N/A")
        self.iv_spd_var.set("N/A")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_color_event(self, color: str):
        customtkinter.set_default_color_theme(color.lower())

    def update_list(self, event):
        typed = self.pokemon_combobox.get()
        data = []
        
        if typed == '':
            data = all_pokelist
            self.pokemon_combobox.configure(values=data)
        else:
            for i in range(0, len(all_pokelist)):
                if typed.lower() in all_pokelist[i].lower():
                    data.append(all_pokelist[i])
            self.pokemon_combobox.configure(values=data)
            

    def reset_evs_event(self):
        self.ev_hp_var.set(0)
        self.ev_atk_var.set(0)
        self.ev_def_var.set(0)
        self.ev_spatk_var.set(0)
        self.ev_spdef_var.set(0)
        self.ev_spd_var.set(0)

    def reset_stats_event(self):
        self.hp_var.set(0)
        self.atk_var.set(0)
        self.def_var.set(0)
        self.spatk_var.set(0)
        self.spdef_var.set(0)
        self.spd_var.set(0)

    def calcIV(self):
        #API
        usr_input = self.pokemon_combobox.get().lower()
        nature = self.nature_optionmenu.get().lower()
        poke_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{usr_input}")
        nature_response = requests.get(f"https://pokeapi.co/api/v2/nature/{nature}")
        
        try:
            pokemon = poke_response.json()
        except:
            tkinter.messagebox.showerror("Error - Pokemon Not Found", "Check spelling and re-enter pokemon, see combobox for valid options.")

        nature_dict = nature_response.json()

        #Set image
        sprite1 = pokemon['sprites']['front_default']
        pokeimage1 = customtkinter.CTkImage(Image.open(requests.get(sprite1, stream=True).raw), size=(192,192))

        self.image_label1 = customtkinter.CTkLabel(self.image_tabview.tab("Default Sprite"), text="", image=pokeimage1)
        self.image_label1.grid(row=0, column=0)

        try:
            sprite2 = pokemon['sprites']['front_shiny']
            pokeimage2 = customtkinter.CTkImage(Image.open(requests.get(sprite2, stream=True).raw), size=(192,192))

            self.image_label2.destroy()
            self.image_label2 = customtkinter.CTkLabel(self.image_tabview.tab("Shiny Sprite"), text="", image=pokeimage2)
            self.image_label2.grid(row=0, column=0)


        except:
            self.image_label2.destroy()
            self.image_label2 = customtkinter.CTkLabel(self.image_tabview.tab("Shiny Sprite"), text="No shiny sprite in database")
            self.image_label2.grid(row=0, column=0)



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
            stat_spatk = int(stat_spatk / 1.1) + (stat_spatk % 1.1 > 0)
        
        elif inc_stat == "attack":
            stat_atk = int(stat_atk / 1.1) + (stat_atk % 1.1 > 0)

        elif inc_stat == "speed":
            stat_spd = int(stat_spd / 1.1) + (stat_spd % 1.1 > 0)

        elif inc_stat == "special-defense":
            stat_spdef = int(stat_spdef / 1.1) + (stat_spdef % 1.1 > 0)

        elif inc_stat == "defense":
            stat_def = int(stat_def / 1.1) + (stat_def % 1.1 > 0)

        if dec_stat == "special-attack":
            stat_spatk = int(stat_spatk / 0.9) + (stat_spatk % .9 > 0)
        
        elif dec_stat == "attack":
            stat_atk = int(stat_atk / 0.9) + (stat_atk % .9 > 0)

        elif dec_stat == "speed":
            stat_spd = int(stat_spd / 0.9) + (stat_spd % .9 > 0)

        elif dec_stat == "special-defense":
            stat_spdef = int(stat_spdef / 0.9) + (stat_spdef % .9 > 0)

        elif dec_stat == "defense":
            stat_def = int(stat_def / 0.9) + (stat_def % .9 > 0)

        #Get Min IVs
        iv_hp_min = round(self.CalcIvHpMin(stat_hp, base_hp, ev_hp, level))
        iv_atk_min = round(self.CalcIvStatsMin(stat_atk, base_atk, ev_atk, level))
        iv_def_min = round(self.CalcIvStatsMin(stat_def, base_def, ev_def, level))
        iv_spatk_min = round(self.CalcIvStatsMin(stat_spatk, base_spatk, ev_spatk, level))
        iv_spdef_min = round(self.CalcIvStatsMin(stat_spdef, base_spdef, ev_spdef, level))
        iv_spd_min = round(self.CalcIvStatsMin(stat_spd, base_spd, ev_spd, level))

        #Get Max IVs
        iv_hp_max = self.CalcIvHpMax(base_hp, iv_hp_min, ev_hp, level, stat_hp)
        iv_atk_max = self.CalcIvStatsMax(base_atk, iv_atk_min, ev_atk, level, stat_atk)
        iv_def_max = self.CalcIvStatsMax(base_def, iv_def_min, ev_def, level, stat_def)
        iv_spatk_max = self.CalcIvStatsMax(base_spatk, iv_spatk_min, ev_spatk, level, stat_spatk)
        iv_spdef_max = self.CalcIvStatsMax(base_spdef, iv_spdef_min, ev_spdef, level, stat_spdef)
        iv_spd_max = self.CalcIvStatsMax(base_spd, iv_spd_min, ev_spd, level, stat_spd)

        
        #Set IVs to gui
        if iv_hp_min < 0 or iv_hp_min > 31 or iv_hp_max < 0 or iv_hp_max > 31:
            self.iv_hp_var.set("N/A")
        else:
            self.iv_hp_var.set(f'{iv_hp_min} - {iv_hp_max}')

        if iv_atk_min < 0 or iv_atk_min > 31 or iv_atk_max < 0 or iv_atk_max > 31:
            self.iv_atk_var.set("N/A")
        else:
            self.iv_atk_var.set(f'{iv_atk_min} - {iv_atk_max}')

        if iv_def_min < 0 or iv_def_min > 31 or iv_def_max < 0 or iv_def_max > 31:
            self.iv_def_var.set("N/A")
        else:
            self.iv_def_var.set(f'{iv_def_min} - {iv_def_max}')

        if iv_spatk_min < 0 or iv_spatk_min > 31 or iv_spatk_max < 0 or iv_spatk_max > 31:
            self.iv_spatk_var.set("N/A")
        else:
            self.iv_spatk_var.set(f'{iv_spatk_min} - {iv_spatk_max}')

        if iv_spdef_min < 0 or iv_spdef_min > 31 or iv_spdef_max < 0 or iv_spdef_max > 31:
            self.iv_spdef_var.set("N/A")
        else:
            self.iv_spdef_var.set(f'{iv_spdef_min} - {iv_spdef_max}')

        if iv_spd_min < 0 or iv_spd_min > 31 or iv_spd_max < 0 or iv_spd_max > 31:
            self.iv_spd_var.set("N/A")
        else:
            self.iv_spd_var.set(f'{iv_spd_min} - {iv_spd_max}')
        

        # set base stats to gui
        self.base_hp_var.set(base_hp)
        self.base_atk_var.set(base_atk)
        self.base_def_var.set(base_def)
        self.base_spatk_var.set(base_spatk)
        self.base_spdef_var.set(base_spdef)
        self.base_spd_var.set(base_spd)


    # calc hp IV
    def CalcIvHpMin(self, stat_hp, base_hp, ev_hp, level):
        iv_hp = ((stat_hp - 10) * 100) / level - 2*base_hp - ev_hp/4 - 100
        return iv_hp
    
    # calc other stats IV
    def CalcIvStatsMin(self, stat, base, ev, level):
        iv = ((stat - 5) * 100) / level - 2 * base - ev/4
        return iv
    
    def CalcIvStatsMax(self, base, iv, ev, level, stat):
        iv_max = iv
        loop = True

        while loop:
            iv_max += 1
            stat_max = int(((((2 * base + iv_max + (ev/4)) * level) / 100) + 5))

            if stat_max > stat:
                loop = False
                iv_max -= 1
            
            else:
                loop = True
        
        return iv_max

    def CalcIvHpMax(self, base, iv, ev, level, stat):
        iv_max = iv
        loop = True

        while loop:
            iv_max += 1
            stat_max = int((((2 * base + iv_max + (ev/4)) * level) / 100) + level + 10)

            if stat_max > stat:
                loop = False
                iv_max -= 1
            
            else:
                loop = True

        return iv_max

if __name__ == "__main__":
    app = CalcIV()
    app.mainloop()