"""
Ultimate IV Calculator
Enhanced UI with exact IV matching, validation, and richer Pokémon info.
"""

from __future__ import annotations

import io
import webbrowser
from typing import Dict, List, Optional

import customtkinter
import requests
import tkinter.messagebox
from PIL import Image

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

API_TIMEOUT = 15
POKEMON_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/{name}"
NATURE_URL = "https://pokeapi.co/api/v2/nature/{name}"

STAT_KEYS = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
STAT_LABELS = {
    "hp": "HP",
    "attack": "ATK",
    "defense": "DEF",
    "special-attack": "SPATK",
    "special-defense": "SPDEF",
    "speed": "SPD",
}
STAT_COLORS = {
    "hp": "#FF5959",
    "attack": "#F5AC78",
    "defense": "#FAE078",
    "special-attack": "#9DB7F5",
    "special-defense": "#A7DB8D",
    "speed": "#FA92B2",
}
NEUTRAL_NATURES = {"hardy", "docile", "bashful", "quirky", "serious"}
NATURES = [
    "Adamant", "Bashful", "Bold", "Brave", "Calm", "Careful", "Docile", "Gentle",
    "Hardy", "Hasty", "Impish", "Jolly", "Lax", "Lonely", "Mild", "Modest", "Naive",
    "Naughty", "Quiet", "Quirky", "Rash", "Relaxed", "Sassy", "Serious", "Timid",
]

CHANGELOG = '''Version 2.0

what's new
• exact IV matching checks every IV from 0 to 31
• bigger dashboard layout with info cards and stat quality tags
• Pokémon info panel now shows typing, size, abilities, and forms
• EV tracker shows total EVs used and how much room is left
• impossible stat lines clearly show N/A and no-match status
• cleaner sprite panel, faster repeated loads, and safer API handling

how to use
• enter species, level, nature, stats, and EVs
• hit Calculate IVs
• look at the IV range plus the quick quality label
• if you know EVs are wrong, fix those first before trusting the range
'''

HELP = '''Quick tips

Pokémon names
-----------------------
• spelling has to match the API
• forms usually need the full form name
• use the autocomplete box when possible

Best results
-----------------------
• level 100 gives the tightest results
• exact EVs matter a lot
• comparing stats across multiple levels helps narrow spreads

What N/A means
-----------------------
• that stat is impossible for the entered species
• or the level / EV / nature combo is wrong

UI notes
-----------------------
• IV bars are a quick visual, not exact proof
• the quality tag is based on the best matching IV
'''


class PokeAPIClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self._pokemon_cache: Dict[str, dict] = {}
        self._nature_cache: Dict[str, dict] = {}
        self._image_cache: Dict[str, Optional[customtkinter.CTkImage]] = {}
        self._pokemon_names: Optional[List[str]] = None

    def get_pokemon_names(self) -> List[str]:
        if self._pokemon_names is not None:
            return self._pokemon_names
        response = self.session.get(POKEMON_LIST_URL, timeout=API_TIMEOUT)
        response.raise_for_status()
        payload = response.json()
        self._pokemon_names = [item["name"].title() for item in payload.get("results", [])]
        return self._pokemon_names

    def get_pokemon(self, name: str) -> dict:
        key = name.lower().strip()
        if key not in self._pokemon_cache:
            response = self.session.get(POKEMON_URL.format(name=key), timeout=API_TIMEOUT)
            response.raise_for_status()
            self._pokemon_cache[key] = response.json()
        return self._pokemon_cache[key]

    def get_nature(self, name: str) -> dict:
        key = name.lower().strip()
        if key not in self._nature_cache:
            response = self.session.get(NATURE_URL.format(name=key), timeout=API_TIMEOUT)
            response.raise_for_status()
            self._nature_cache[key] = response.json()
        return self._nature_cache[key]

    def get_sprite_image(self, url: Optional[str], size: tuple[int, int] = (220, 220)) -> Optional[customtkinter.CTkImage]:
        if not url:
            return None
        cache_key = f"{url}|{size[0]}x{size[1]}"
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        response = self.session.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        tk_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=size)
        self._image_cache[cache_key] = tk_image
        return tk_image


class CalcIV(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.api = PokeAPIClient()
        self.all_pokelist = self._load_pokemon_names()

        self.stat_vars: Dict[str, customtkinter.StringVar] = {}
        self.ev_vars: Dict[str, customtkinter.StringVar] = {}
        self.base_vars: Dict[str, customtkinter.StringVar] = {}
        self.iv_vars: Dict[str, customtkinter.StringVar] = {}
        self.quality_vars: Dict[str, customtkinter.StringVar] = {}
        self.stat_entries: Dict[str, customtkinter.CTkEntry] = {}
        self.ev_entries: Dict[str, customtkinter.CTkEntry] = {}
        self.iv_bars: Dict[str, customtkinter.CTkProgressBar] = {}

        self.default_sprite_image: Optional[customtkinter.CTkImage] = None
        self.shiny_sprite_image: Optional[customtkinter.CTkImage] = None

        self.species_var = customtkinter.StringVar(value="-")
        self.types_var = customtkinter.StringVar(value="-")
        self.abilities_var = customtkinter.StringVar(value="-")
        self.size_var = customtkinter.StringVar(value="-")
        self.forms_var = customtkinter.StringVar(value="-")
        self.ev_summary_var = customtkinter.StringVar(value="EV Total: 0 / 510")
        self.status_var = customtkinter.StringVar(value="Ready. Load a Pokémon and calculate IVs.")
        self.best_stat_var = customtkinter.StringVar(value="Best Match: -")
        self.perfect_iv_var = customtkinter.StringVar(value="31 IV Stats: -")

        self.title("Ultimate IV Calculator")
        self._set_startup_geometry()
        self.minsize(1580, 780)
        self.grid_columnconfigure(0, weight=0, minsize=230)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_area()
        self._set_defaults()
        self._load_default_pokemon()

    def _set_startup_geometry(self) -> None:
        self.update_idletasks()

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        target_w = min(1800, max(1625, int(screen_w * 0.925)))
        target_h = 780

        x = max(0, (screen_w - target_w) // 2)
        y = max(0, (screen_h - target_h) // 2)

        self.geometry(f"{target_w}x{target_h}+{x}+{y}")

    def _load_pokemon_names(self) -> List[str]:
        try:
            return self.api.get_pokemon_names()
        except requests.RequestException:
            tkinter.messagebox.showwarning(
                "Warning",
                "Could not preload Pokémon names from PokeAPI. Autocomplete may be unavailable until the API is reachable.",
            )
            return ["Bulbasaur"]

    def _build_sidebar(self) -> None:
        self.sidebar_frame = customtkinter.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Ultimate IV Calculator",
            font=customtkinter.CTkFont(size=24, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(22, 8))

        self.tagline_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="https://github.com/brendonbusker",
            text_color=("dodgerblue2", "lightskyblue"),
            wraplength=0,
            justify="center",
            cursor="hand2",
            font=customtkinter.CTkFont(underline=True)
        )
        self.tagline_label.grid(row=1, column=0, padx=20, pady=(0, 12))
        self.tagline_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/brendonbusker"))

        self.sidebar_tabview = customtkinter.CTkTabview(self.sidebar_frame, width=200)
        self.sidebar_tabview.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")
        self.sidebar_tabview.add("Updates")
        self.sidebar_tabview.add("Help")

        self.textbox = customtkinter.CTkTextbox(self.sidebar_tabview.tab("Updates"), width=190, height=370)
        self.textbox.pack(fill="both", expand=True, padx=8, pady=8)

        self.help_textbox = customtkinter.CTkTextbox(self.sidebar_tabview.tab("Help"), width=190, height=370)
        self.help_textbox.pack(fill="both", expand=True, padx=8, pady=8)

        self.status_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.status_frame.grid(row=3, column=0, padx=18, pady=10, sticky="ew")
        self.status_title = customtkinter.CTkLabel(
            self.status_frame,
            text="Status",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.status_title.grid(row=0, column=0, padx=12, pady=(10, 4), sticky="w")
        self.status_label = customtkinter.CTkLabel(
            self.status_frame,
            textvariable=self.status_var,
            wraplength=180,
            justify="left",
        )
        self.status_label.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="w")

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(8, 0), sticky="w")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(8, 20), sticky="ew")

    def _build_main_area(self) -> None:
        self.main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=3, minsize=860)
        self.main_container.grid_columnconfigure(1, weight=2, minsize=600)
        self.main_container.grid_rowconfigure(1, weight=1)

        self._build_header_card()
        self._build_center_panel()
        self._build_right_panel()

    def _build_header_card(self) -> None:
        self.header_card = customtkinter.CTkFrame(self.main_container)
        self.header_card.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        self.header_card.grid_columnconfigure(0, weight=1)
        self.header_card.grid_columnconfigure(1, weight=1)
        self.header_card.grid_columnconfigure(2, weight=1)
        self.header_card.grid_columnconfigure(3, weight=1)

        self.species_title = customtkinter.CTkLabel(
            self.header_card,
            textvariable=self.species_var,
            font=customtkinter.CTkFont(size=28, weight="bold"),
        )
        self.species_title.grid(row=0, column=0, padx=18, pady=(14, 2), sticky="w")

        self.types_label = customtkinter.CTkLabel(self.header_card, textvariable=self.types_var)
        self.types_label.grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

        self.best_label = customtkinter.CTkLabel(self.header_card, textvariable=self.best_stat_var)
        self.best_label.grid(row=0, column=1, padx=12, pady=(14, 2), sticky="w")

        self.perfect_label = customtkinter.CTkLabel(self.header_card, textvariable=self.perfect_iv_var)
        self.perfect_label.grid(row=1, column=1, padx=12, pady=(0, 14), sticky="w")

        self.abilities_label = customtkinter.CTkLabel(self.header_card, textvariable=self.abilities_var, wraplength=260, justify="left")
        self.abilities_label.grid(row=0, column=2, padx=12, pady=(14, 2), sticky="w")

        self.size_label = customtkinter.CTkLabel(self.header_card, textvariable=self.size_var)
        self.size_label.grid(row=1, column=2, padx=12, pady=(0, 14), sticky="w")

        self.forms_label = customtkinter.CTkLabel(self.header_card, textvariable=self.forms_var, wraplength=240, justify="left")
        self.forms_label.grid(row=0, column=3, rowspan=2, padx=12, pady=14, sticky="w")

    def _build_center_panel(self) -> None:
        self.center_panel = customtkinter.CTkFrame(self.main_container)
        self.center_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.center_panel.grid_columnconfigure(0, weight=1)
        self.center_panel.grid_rowconfigure(1, weight=1)

        self.controls_frame = customtkinter.CTkFrame(self.center_panel)
        self.controls_frame.grid(row=0, column=0, padx=16, pady=(16, 10), sticky="ew")
        for i in range(6):
            self.controls_frame.grid_columnconfigure(i, weight=1)

        self.pokemon_label = customtkinter.CTkLabel(self.controls_frame, text="Pokémon")
        self.pokemon_label.grid(row=0, column=0, padx=8, pady=(12, 4), sticky="w")
        self.pokemon_combobox = customtkinter.CTkComboBox(self.controls_frame, values=self.all_pokelist)
        self.pokemon_combobox.bind("<KeyRelease>", self.update_list)
        self.pokemon_combobox.grid(row=1, column=0, padx=8, pady=(0, 12), sticky="ew")

        self.level_label = customtkinter.CTkLabel(self.controls_frame, text="Level")
        self.level_label.grid(row=0, column=1, padx=8, pady=(12, 4), sticky="w")
        self.level_var = customtkinter.StringVar()
        self.level_entry = customtkinter.CTkEntry(self.controls_frame, textvariable=self.level_var)
        self.level_entry.grid(row=1, column=1, padx=8, pady=(0, 12), sticky="ew")

        self.nature_label = customtkinter.CTkLabel(self.controls_frame, text="Nature")
        self.nature_label.grid(row=0, column=2, padx=8, pady=(12, 4), sticky="w")
        self.nature_optionmenu = customtkinter.CTkOptionMenu(self.controls_frame, values=NATURES)
        self.nature_optionmenu.grid(row=1, column=2, padx=8, pady=(0, 12), sticky="ew")

        self.ev_summary_label = customtkinter.CTkLabel(
            self.controls_frame,
            textvariable=self.ev_summary_var,
            font=customtkinter.CTkFont(weight="bold"),
        )
        self.ev_summary_label.grid(row=0, column=3, columnspan=2, padx=8, pady=(12, 4), sticky="w")

        self.calculate_button = customtkinter.CTkButton(self.controls_frame, text="Calculate IVs", height=36, command=self.calcIV)
        self.calculate_button.grid(row=1, column=3, padx=8, pady=(0, 12), sticky="ew")

        self.reset_stats_button = customtkinter.CTkButton(self.controls_frame, text="Clear Stats", height=36, command=self.reset_stats_event)
        self.reset_stats_button.grid(row=1, column=4, padx=8, pady=(0, 12), sticky="ew")

        self.reset_evs_button = customtkinter.CTkButton(self.controls_frame, text="Clear EVs", height=36, command=self.reset_evs_event)
        self.reset_evs_button.grid(row=1, column=5, padx=8, pady=(0, 12), sticky="ew")

        self.stats_frame = customtkinter.CTkFrame(self.center_panel)
        self.stats_frame.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        self.stats_frame.grid_columnconfigure(0, weight=0, minsize=70)
        self.stats_frame.grid_columnconfigure(1, weight=1, minsize=110)
        self.stats_frame.grid_columnconfigure(2, weight=1, minsize=90)
        self.stats_frame.grid_columnconfigure(3, weight=1, minsize=90)
        self.stats_frame.grid_columnconfigure(4, weight=1, minsize=120)
        self.stats_frame.grid_columnconfigure(5, weight=2, minsize=180)
        self.stats_frame.grid_columnconfigure(6, weight=1, minsize=130)

        headers = ["Stat", "Observed", "EV", "Base", "IV Range", "IV Meter", "Quality"]
        for col, header in enumerate(headers):
            customtkinter.CTkLabel(
                self.stats_frame,
                text=header,
                font=customtkinter.CTkFont(size=14, weight="bold"),
            ).grid(row=0, column=col, padx=10, pady=(14, 8), sticky="w")

        for row_index, stat_key in enumerate(STAT_KEYS, start=1):
            stat_label = customtkinter.CTkLabel(
            self.stats_frame,
            text=STAT_LABELS[stat_key],
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=STAT_COLORS[stat_key],
            )
            stat_label.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")

            stat_var = customtkinter.StringVar()
            ev_var = customtkinter.StringVar()
            base_var = customtkinter.StringVar(value="-")
            iv_var = customtkinter.StringVar(value="N/A")
            quality_var = customtkinter.StringVar(value="-")

            stat_entry = customtkinter.CTkEntry(self.stats_frame, textvariable=stat_var, placeholder_text="0")
            ev_entry = customtkinter.CTkEntry(self.stats_frame, textvariable=ev_var, placeholder_text="0")
            base_entry = customtkinter.CTkEntry(self.stats_frame, textvariable=base_var, state="disabled")
            iv_entry = customtkinter.CTkEntry(self.stats_frame, textvariable=iv_var, state="disabled")

            iv_bar = customtkinter.CTkProgressBar(
                self.stats_frame,
                progress_color=STAT_COLORS[stat_key],
            )
            iv_bar.set(0)
            quality_label = customtkinter.CTkLabel(self.stats_frame, textvariable=quality_var)

            stat_entry.grid(row=row_index, column=1, padx=10, pady=10, sticky="ew")
            ev_entry.grid(row=row_index, column=2, padx=10, pady=10, sticky="ew")
            base_entry.grid(row=row_index, column=3, padx=10, pady=10, sticky="ew")
            iv_entry.grid(row=row_index, column=4, padx=10, pady=10, sticky="ew")
            iv_bar.grid(row=row_index, column=5, padx=10, pady=10, sticky="ew")
            quality_label.grid(row=row_index, column=6, padx=10, pady=10, sticky="w")

            self.stat_vars[stat_key] = stat_var
            self.ev_vars[stat_key] = ev_var
            self.base_vars[stat_key] = base_var
            self.iv_vars[stat_key] = iv_var
            self.quality_vars[stat_key] = quality_var
            self.stat_entries[stat_key] = stat_entry
            self.ev_entries[stat_key] = ev_entry
            self.iv_bars[stat_key] = iv_bar

            ev_var.trace_add("write", self._on_ev_change)

    def _build_right_panel(self) -> None:
        self.right_panel = customtkinter.CTkFrame(self.main_container)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        self.right_panel.grid_rowconfigure(0, weight=0)
        self.right_panel.grid_rowconfigure(1, weight=0)
        self.right_panel.grid_rowconfigure(2, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.image_card = customtkinter.CTkFrame(self.right_panel)
        self.image_card.grid(row=0, column=0, padx=10, pady=(10, 8), sticky="ew")
        self.image_tabview = customtkinter.CTkTabview(self.image_card, width=300, height=245)
        self.image_tabview.pack(fill="both", expand=True, padx=6, pady=6)
        self.image_tabview.add("Default")
        self.image_tabview.add("Shiny")

        self.image_label1 = customtkinter.CTkLabel(self.image_tabview.tab("Default"), text="Loading...")
        self.image_label1.pack(padx=12, pady=12)
        self.image_label2 = customtkinter.CTkLabel(self.image_tabview.tab("Shiny"), text="Loading...")
        self.image_label2.pack(padx=12, pady=12)

        self.summary_card = customtkinter.CTkFrame(self.right_panel)
        self.summary_card.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")
        self.summary_card.grid_columnconfigure((0, 1), weight=1)

        self.summary_title = customtkinter.CTkLabel(
            self.summary_card,
            text="Quick Readout",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.summary_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(8, 4), sticky="w")

        self.summary_value_labels = []
        for idx, (title, var) in enumerate([
            ("Species", self.species_var),
            ("Typing", self.types_var),
            ("Size", self.size_var),
            ("Forms", self.forms_var),
        ], start=1):
            title_label = customtkinter.CTkLabel(self.summary_card, text=title, text_color=("gray35", "gray70"))
            value_label = customtkinter.CTkLabel(self.summary_card, textvariable=var, wraplength=220, justify="left")
            title_label.grid(row=idx, column=0, padx=10, pady=1, sticky="w")
            value_label.grid(row=idx, column=1, padx=8, pady=1, sticky="w")
            self.summary_value_labels.append((title_label, value_label))

        self.notes_card = customtkinter.CTkFrame(self.right_panel)
        self.notes_card.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.notes_card.grid_rowconfigure(1, weight=1)
        self.notes_card.grid_columnconfigure(0, weight=1)

        self.notes_title = customtkinter.CTkLabel(
            self.notes_card,
            text="Extra Notes",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.notes_title.grid(row=0, column=0, padx=10, pady=(8, 4), sticky="w")

        self.notes_box = customtkinter.CTkTextbox(self.notes_card, height=145)
        self.notes_box.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")

    def _set_defaults(self) -> None:
        self.textbox.insert("0.0", CHANGELOG)
        self.help_textbox.insert("0.0", HELP)
        self.textbox.configure(state="disabled")
        self.help_textbox.configure(state="disabled")
        self.notes_box.insert(
            "0.0",
            "• A perfect 31 IV shows as a full meter.\n"
            "• Wide ranges usually mean low level or uncertain EVs.\n"
            "• Neutral natures leave all non-HP stats unchanged.\n"
            "• Hidden abilities are marked in the abilities line when available."
        )
        self.notes_box.configure(state="disabled")
        self.appearance_mode_optionemenu.set("System")
        self.nature_optionmenu.set("Adamant")
        self.level_var.set("100")
        self.pokemon_combobox.set("Bulbasaur")
        self.reset_evs_event()
        self.reset_stats_event()
        self._update_ev_summary()

    def _load_default_pokemon(self) -> None:
        try:
            pokemon = self.api.get_pokemon("bulbasaur")
            self._apply_pokemon_to_ui(pokemon)
        except requests.RequestException:
            self.image_label1.configure(text="Sprite unavailable", image=None)
            self.image_label2.configure(text="Sprite unavailable", image=None)
            self.status_var.set("Could not load default Pokémon data.")

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        customtkinter.set_appearance_mode(new_appearance_mode)

    def update_list(self, event) -> None:
        typed = self.pokemon_combobox.get().strip().lower()
        if not typed:
            data = self.all_pokelist
        else:
            data = [name for name in self.all_pokelist if typed in name.lower()]
        self.pokemon_combobox.configure(values=data if data else self.all_pokelist)

    def reset_evs_event(self) -> None:
        for stat_key in STAT_KEYS:
            self.ev_vars[stat_key].set("0")
        self._update_ev_summary()

    def reset_stats_event(self) -> None:
        for stat_key in STAT_KEYS:
            self.stat_vars[stat_key].set("")
            self.iv_vars[stat_key].set("N/A")
            self.quality_vars[stat_key].set("-")
            self.iv_bars[stat_key].set(0)
        self.best_stat_var.set("Best Match: -")
        self.perfect_iv_var.set("31 IV Stats: -")

    def _on_ev_change(self, *_args) -> None:
        self._update_ev_summary()

    def _update_ev_summary(self) -> None:
        total = 0
        for stat_key in STAT_KEYS:
            raw = self.ev_vars.get(stat_key).get().strip() if stat_key in self.ev_vars else "0"
            if raw.isdigit():
                total += int(raw)
        remaining = max(0, 510 - total)
        suffix = "  •  Over cap" if total > 510 else f"  •  {remaining} left"
        self.ev_summary_var.set(f"EV Total: {total} / 510{suffix}")

    def calcIV(self) -> None:
        try:
            pokemon_name = self.pokemon_combobox.get().strip()
            if not pokemon_name:
                raise ValueError("Enter a Pokémon name.")

            level = self._parse_level()
            nature_name = self.nature_optionmenu.get().strip().lower()
            entered_stats = self._parse_stat_inputs(self.stat_vars, field_name="stat", minimum=1, maximum=999)
            evs = self._parse_stat_inputs(self.ev_vars, field_name="EV", minimum=0, maximum=255)
            self._validate_total_evs(evs)

            pokemon = self.api.get_pokemon(pokemon_name)
            nature = self.api.get_nature(nature_name)
        except ValueError as exc:
            self.status_var.set(f"Input error: {exc}")
            tkinter.messagebox.showerror("Input Error", str(exc))
            return
        except requests.HTTPError:
            self.status_var.set("Pokémon not found. Try the autocomplete list or a full form name.")
            tkinter.messagebox.showerror(
                "Error - Pokemon Not Found",
                "Check spelling and re-enter the Pokémon. If it has a form, use the full form name from the autocomplete list.",
            )
            return
        except requests.RequestException:
            self.status_var.set("Network issue while talking to PokeAPI.")
            tkinter.messagebox.showerror(
                "Network Error",
                "Could not reach PokeAPI. Please try again when your connection is stable.",
            )
            return

        base_stats = self._extract_base_stats(pokemon)
        self._apply_pokemon_to_ui(pokemon)

        nature_modifiers = self._get_nature_modifiers(nature)
        iv_matches = {
            stat_key: self._find_matching_ivs(
                stat_key=stat_key,
                observed_stat=entered_stats[stat_key],
                base_stat=base_stats[stat_key],
                ev=evs[stat_key],
                level=level,
                nature_modifier=nature_modifiers[stat_key],
            )
            for stat_key in STAT_KEYS
        }

        perfect_stats = []
        best_stat_name = None
        best_iv_value = -1

        for stat_key in STAT_KEYS:
            matches = iv_matches[stat_key]
            if not matches:
                self.iv_vars[stat_key].set("N/A")
                self.quality_vars[stat_key].set("No match")
                self.iv_bars[stat_key].set(0)
                continue

            if len(matches) == 1:
                self.iv_vars[stat_key].set(str(matches[0]))
            else:
                self.iv_vars[stat_key].set(f"{matches[0]} - {matches[-1]}")

            best_match = matches[-1]
            self.quality_vars[stat_key].set(self._describe_iv_quality(best_match, len(matches)))
            self.iv_bars[stat_key].set(best_match / 31)

            if 31 in matches:
                perfect_stats.append(STAT_LABELS[stat_key])
            if best_match > best_iv_value:
                best_iv_value = best_match
                best_stat_name = STAT_LABELS[stat_key]

        if best_stat_name is not None:
            self.best_stat_var.set(f"Best Match: {best_stat_name} at up to {best_iv_value} IV")
        else:
            self.best_stat_var.set("Best Match: None")

        self.perfect_iv_var.set(
            f"31 IV Stats: {', '.join(perfect_stats)}" if perfect_stats else "31 IV Stats: None confirmed"
        )

        impossible_count = sum(1 for matches in iv_matches.values() if not matches)
        if impossible_count:
            self.status_var.set(f"Calculated with {impossible_count} impossible stat slot(s). Double-check inputs.")
        else:
            self.status_var.set(f"Calculation complete for {pokemon['name'].title()} at level {level}.")

    def _parse_level(self) -> int:
        raw_level = self.level_var.get().strip()
        if not raw_level:
            raise ValueError("Enter a level from 1 to 100.")
        if not raw_level.isdigit():
            raise ValueError("Level must be a whole number from 1 to 100.")
        level = int(raw_level)
        if not 1 <= level <= 100:
            raise ValueError("Level must be between 1 and 100.")
        return level

    def _parse_stat_inputs(
        self,
        value_map: Dict[str, customtkinter.StringVar],
        field_name: str,
        minimum: int,
        maximum: int,
    ) -> Dict[str, int]:
        parsed: Dict[str, int] = {}
        for stat_key, value_var in value_map.items():
            raw = value_var.get().strip()
            label = STAT_LABELS[stat_key]
            if raw == "":
                raise ValueError(f"Enter {field_name} for {label}.")
            if not raw.isdigit():
                raise ValueError(f"{field_name} for {label} must be a whole number.")
            value = int(raw)
            if not minimum <= value <= maximum:
                raise ValueError(f"{field_name} for {label} must be between {minimum} and {maximum}.")
            parsed[stat_key] = value
        return parsed

    def _validate_total_evs(self, evs: Dict[str, int]) -> None:
        if sum(evs.values()) > 510:
            raise ValueError("Total EVs cannot exceed 510.")

    def _extract_base_stats(self, pokemon: dict) -> Dict[str, int]:
        stat_map = {entry["stat"]["name"]: entry["base_stat"] for entry in pokemon["stats"]}
        return {stat_key: stat_map[stat_key] for stat_key in STAT_KEYS}

    def _get_nature_modifiers(self, nature: dict) -> Dict[str, float]:
        modifiers = {stat_key: 1.0 for stat_key in STAT_KEYS}
        nature_name = nature["name"]
        if nature_name in NEUTRAL_NATURES:
            return modifiers

        increased = nature.get("increased_stat")
        decreased = nature.get("decreased_stat")
        if increased is not None:
            modifiers[increased["name"]] = 1.1
        if decreased is not None:
            modifiers[decreased["name"]] = 0.9
        return modifiers

    def _find_matching_ivs(
        self,
        stat_key: str,
        observed_stat: int,
        base_stat: int,
        ev: int,
        level: int,
        nature_modifier: float,
    ) -> List[int]:
        matches: List[int] = []
        for iv in range(32):
            calculated = self._calculate_stat(stat_key, base_stat, iv, ev, level, nature_modifier)
            if calculated == observed_stat:
                matches.append(iv)
        return matches

    @staticmethod
    def _calculate_stat(
        stat_key: str,
        base_stat: int,
        iv: int,
        ev: int,
        level: int,
        nature_modifier: float,
    ) -> int:
        ev_term = ev // 4
        if stat_key == "hp":
            if base_stat == 1:
                return 1
            return ((2 * base_stat + iv + ev_term) * level) // 100 + level + 10

        raw_stat = ((2 * base_stat + iv + ev_term) * level) // 100 + 5
        return int(raw_stat * nature_modifier)

    @staticmethod
    def _describe_iv_quality(best_iv: int, match_count: int) -> str:
        if match_count > 8:
            return "Wide range"
        if best_iv == 31:
            return "Perfect possible"
        if best_iv >= 28:
            return "Elite"
        if best_iv >= 24:
            return "Strong"
        if best_iv >= 16:
            return "Decent"
        return "Low"

    def _apply_pokemon_to_ui(self, pokemon: dict) -> None:
        base_stats = self._extract_base_stats(pokemon)
        for stat_key, base_stat in base_stats.items():
            self.base_vars[stat_key].set(str(base_stat))
        self._update_pokemon_summary(pokemon)
        self._update_sprite_labels(pokemon)

    def _update_pokemon_summary(self, pokemon: dict) -> None:
        self.species_var.set(pokemon["name"].title())

        types = [entry["type"]["name"].title() for entry in sorted(pokemon.get("types", []), key=lambda x: x["slot"])]
        self.types_var.set(f"Typing: {' / '.join(types) if types else '-'}")

        ability_names = []
        for ability in pokemon.get("abilities", []):
            label = ability["ability"]["name"].replace("-", " ").title()
            if ability.get("is_hidden"):
                label += " (Hidden)"
            ability_names.append(label)
        self.abilities_var.set(f"Abilities: {', '.join(ability_names) if ability_names else '-'}")

        height_m = pokemon.get("height", 0) / 10
        weight_kg = pokemon.get("weight", 0) / 10
        self.size_var.set(f"Size: {height_m:.1f} m • {weight_kg:.1f} kg")

        forms = [form["name"].title() for form in pokemon.get("forms", [])]
        self.forms_var.set(f"Forms: {', '.join(forms[:5]) if forms else '-'}")

    def _update_sprite_labels(self, pokemon: dict) -> None:
        sprites = pokemon.get("sprites", {})
        try:
            default_image = self.api.get_sprite_image(sprites.get("front_default"), size=(220, 220))
        except requests.RequestException:
            default_image = None
        try:
            shiny_image = self.api.get_sprite_image(sprites.get("front_shiny"), size=(220, 220))
        except requests.RequestException:
            shiny_image = None

        self.default_sprite_image = default_image
        self.shiny_sprite_image = shiny_image

        if default_image is not None:
            self.image_label1.configure(text="", image=default_image)
        else:
            self.image_label1.configure(text="No default sprite in database", image=None)

        if shiny_image is not None:
            self.image_label2.configure(text="", image=shiny_image)
        else:
            self.image_label2.configure(text="No shiny sprite in database", image=None)


if __name__ == "__main__":
    app = CalcIV()
    app.mainloop()
