import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np

from model_coefficients import (
    CRIME_CLASSES, INTERCEPTS, COEFFICIENTS,
    LOCATION_DESCRIPTION_MAPPING, WEAPON_MAPPING, LIGHTING_CONDITION_MAPPING,
    WEATHER_MAPPING, VICTIM_GENDER_MAPPING, VICTIM_RACE_MAPPING
)

class PredictPage:
    def __init__(self, app):
        self.app = app

    def __getattr__(self, name):
        return getattr(self.app, name)

    def show_predict_screen(self):
        self.clear_content()
        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()

        tk.Label(
            self.scrollable_frame,
            text="Crime Type Predictor",
            font=self.font_title,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(padx=25, pady=15, anchor=tk.W)

        tk.Label(
            self.scrollable_frame,
            text="Enter incident details to predict the most likely crime type",
            font=self.font_body,
            bg=self.bg_gradient_mid,
            fg=self.text_dim
        ).pack(padx=25, pady=(0, 20), anchor=tk.W)

        form = tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid)
        form.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        self.create_form_field(form, "Location Description", "location")
        self.location_var = tk.StringVar()
        locations = sorted(LOCATION_DESCRIPTION_MAPPING.keys())
        location_dropdown = ttk.Combobox(
            form, textvariable=self.location_var, values=locations,
            font=("Arial", 13), state="readonly", width=40
        )
        location_dropdown.pack(fill=tk.X, pady=(5, 15))
        location_dropdown.set(locations[0])

        self.create_form_field(form, "Weapon Used", "weapon")
        self.weapon_var = tk.StringVar()
        weapons = sorted(WEAPON_MAPPING.keys())
        weapon_dropdown = ttk.Combobox(
            form, textvariable=self.weapon_var, values=weapons,
            font=("Arial", 13), state="readonly", width=40
        )
        weapon_dropdown.pack(fill=tk.X, pady=(5, 15))
        weapon_dropdown.set(weapons[0])

        self.create_form_field(form, "Lighting Condition", "lighting")
        self.lighting_var = tk.StringVar()
        lighting_conditions = sorted(LIGHTING_CONDITION_MAPPING.keys())
        lighting_dropdown = ttk.Combobox(
            form, textvariable=self.lighting_var, values=lighting_conditions,
            font=("Arial", 13), state="readonly", width=40
        )
        lighting_dropdown.pack(fill=tk.X, pady=(5, 15))
        lighting_dropdown.set(lighting_conditions[0])

        self.create_form_field(form, "Weather", "weather")
        self.weather_var = tk.StringVar()
        weather_conditions = sorted(WEATHER_MAPPING.keys())
        weather_dropdown = ttk.Combobox(
            form, textvariable=self.weather_var, values=weather_conditions,
            font=("Arial", 13), state="readonly", width=40
        )
        weather_dropdown.pack(fill=tk.X, pady=(5, 15))
        weather_dropdown.set(weather_conditions[0])

        self.create_form_field(form, "Victim Gender", "gender")
        self.gender_var = tk.StringVar()
        genders = sorted(VICTIM_GENDER_MAPPING.keys())
        gender_dropdown = ttk.Combobox(
            form, textvariable=self.gender_var, values=genders,
            font=("Arial", 13), state="readonly", width=40
        )
        gender_dropdown.pack(fill=tk.X, pady=(5, 15))
        gender_dropdown.set(genders[0])

        self.create_form_field(form, "Victim Race", "race")
        self.race_var = tk.StringVar()
        races = sorted(VICTIM_RACE_MAPPING.keys())
        race_dropdown = ttk.Combobox(
            form, textvariable=self.race_var, values=races,
            font=("Arial", 13), state="readonly", width=40
        )
        race_dropdown.pack(fill=tk.X, pady=(5, 15))
        race_dropdown.set(races[0])

        self.create_form_field(form, "Victim Age", "age")
        self.age_var = tk.StringVar(value="")
        age_entry = tk.Entry(
            form, textvariable=self.age_var, font=("Arial", 14),
            bg=self.card_dark, fg=self.text_bright,
            insertbackground="white", bd=0
        )
        age_entry.pack(fill=tk.X, pady=(5, 15), ipady=10)

        self.results_container = tk.Frame(form, bg=self.bg_gradient_mid)
        self.results_container.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        shadow = tk.Frame(form, bg="#000000")
        shadow.pack(fill=tk.X, pady=25)
        tk.Button(
            shadow, text="Predict Crime Type",
            font=("Arial", 16, "bold"),
            bg=self.accent_cyan, fg="white",
            activebackground="#3a7bc8", bd=0,
            cursor="hand2", command=self.predict_crime, height=3
        ).pack(fill=tk.X, padx=2, pady=2)

        tk.Frame(form, bg=self.bg_gradient_mid, height=100).pack()

    def create_form_field(self, parent, label_text, field_id):
        tk.Label(
            parent, text=label_text, font=self.font_subheader,
            bg=self.bg_gradient_mid, fg=self.text_bright
        ).pack(anchor=tk.W, pady=(10, 8))

    def predict_crime(self):
        for w in self.results_container.winfo_children():
            w.destroy()

        try:
            location = self.location_var.get()
            weapon = self.weapon_var.get()
            lighting = self.lighting_var.get()
            weather = self.weather_var.get()
            gender = self.gender_var.get()
            race = self.race_var.get()
            age = int(self.age_var.get())

            if age < 0 or age > 100:
                messagebox.showwarning("Invalid Age", "Please enter a valid age between 0 and 100")
                return

            location_encoded = LOCATION_DESCRIPTION_MAPPING[location]
            weapon_encoded = WEAPON_MAPPING[weapon]
            lighting_encoded = LIGHTING_CONDITION_MAPPING[lighting]
            weather_encoded = WEATHER_MAPPING[weather]
            gender_encoded = VICTIM_GENDER_MAPPING[gender]
            race_encoded = VICTIM_RACE_MAPPING[race]

            X = np.array([location_encoded, weapon_encoded, lighting_encoded,
                          weather_encoded, gender_encoded, race_encoded, age])

            logits = INTERCEPTS + np.dot(COEFFICIENTS, X)

            exp_logits = np.exp(logits - np.max(logits))
            probabilities = exp_logits / np.sum(exp_logits)

            sorted_indices = np.argsort(probabilities)[::-1]

            loading_label = tk.Label(
                self.results_container,
                text="Analyzing crime patterns...",
                font=self.font_subheader,
                bg=self.bg_gradient_mid,
                fg=self.accent_cyan
            )
            loading_label.pack(pady=20)
            self.root.update()
            self.root.after(800)
            loading_label.destroy()

            tk.Label(
                self.results_container,
                text="Prediction Results",
                font=self.font_header,
                bg=self.bg_gradient_mid,
                fg=self.text_bright
            ).pack(anchor=tk.W, pady=(10, 15))

            most_likely_idx = sorted_indices[0]
            most_likely_crime = CRIME_CLASSES[most_likely_idx]
            most_likely_prob = probabilities[most_likely_idx] * 100

            self.create_predicted_crime_card(
                most_likely_crime,
                most_likely_prob
            )

            tk.Label(
                self.results_container,
                text="All Crime Type Probabilities",
                font=self.font_subheader,
                bg=self.bg_gradient_mid,
                fg=self.text_bright
            ).pack(anchor=tk.W, pady=(25, 15))

            for idx in sorted_indices:
                crime_type = CRIME_CLASSES[idx]
                probability = probabilities[idx] * 100
                self.create_probability_bar(crime_type, probability)

            self.update_scroll_region()
            self.root.after(100, lambda: self.canvas.yview_moveto(1.0))

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter a valid number for age.\n\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("Prediction Error", f"An error occurred during prediction:\n\n{str(e)}")

    def create_predicted_crime_card(self, crime_type, probability):
        shadow = tk.Frame(self.results_container, bg="#000000")
        shadow.pack(fill=tk.X, pady=10)

        card = tk.Frame(shadow, bg=self.accent_cyan)
        card.pack(fill=tk.X, padx=3, pady=3)

        content = tk.Frame(card, bg=self.accent_cyan)
        content.pack(fill=tk.X, padx=25, pady=20)

        tk.Label(
            content, text="⭐ MOST LIKELY",
            font=("Arial", 11, "bold"),
            bg="white", fg=self.accent_cyan,
            padx=12, pady=5
        ).pack(pady=(0, 15))

        tk.Label(
            content, text=crime_type,
            font=("Arial", 32, "bold"),
            bg=self.accent_cyan, fg="white"
        ).pack(pady=(0, 10))

        tk.Label(
            content, text=f"{probability:.1f}% Probability",
            font=self.font_header,
            bg=self.accent_cyan, fg="white"
        ).pack()

    def create_probability_bar(self, crime_type, probability):
        shadow = tk.Frame(self.results_container, bg="#000000")
        shadow.pack(fill=tk.X, pady=6)

        card = tk.Frame(shadow, bg=self.card_dark)
        card.pack(fill=tk.X, padx=2, pady=2)

        content = tk.Frame(card, bg=self.card_dark)
        content.pack(fill=tk.X, padx=20, pady=15)

        header = tk.Frame(content, bg=self.card_dark)
        header.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            header, text=crime_type,
            font=self.font_subheader,
            bg=self.card_dark, fg=self.text_bright
        ).pack(side=tk.LEFT)

        tk.Label(
            header, text=f"{probability:.2f}%",
            font=("Arial", 14, "bold"),
            bg=self.card_dark, fg=self.accent_cyan
        ).pack(side=tk.RIGHT)

        bar_bg = tk.Frame(content, bg=self.bg_gradient_start, height=12)
        bar_bg.pack(fill=tk.X)

        bar_width = int((probability / 100.0) * 560)

        if probability >= 20:
            bar_color = self.accent_green
        elif probability >= 10:
            bar_color = self.accent_orange
        else:
            bar_color = self.accent_pink

        if bar_width > 0:
            bar_fill = tk.Frame(bar_bg, bg=bar_color, width=bar_width, height=12)
            bar_fill.pack(side=tk.LEFT)
