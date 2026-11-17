import tkinter as tk
from tkinter import messagebox
import time
import random

class RoutePage:
    def __init__(self, app):
        self.app = app
    def __getattr__(self, name):
        return getattr(self.app, name)


    def show_route_screen(self):
        self.clear_content()
        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()

        tk.Label(self.scrollable_frame, text="Route Finder", font=self.font_title,
                 bg=self.bg_gradient_mid, fg=self.text_bright
                 ).pack(padx=25, pady=15, anchor=tk.W)

        form = tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid)
        form.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        tk.Label(form, text="📍 Current Location", font=self.font_subheader,
                 bg=self.bg_gradient_mid, fg=self.text_bright).pack(anchor=tk.W, pady=(10, 8))

        self.current_var = tk.StringVar(value=self.user_location)
        current_entry = tk.Entry(form, textvariable=self.current_var, font=("Arial", 14),
                                 bg=self.card_dark, fg=self.text_bright, insertbackground="white", bd=0, state=tk.DISABLED)
        current_entry.pack(fill=tk.X, pady=5, ipady=10)

        tk.Label(form, text="🎯 Destination", font=self.font_subheader,
                 bg=self.bg_gradient_mid, fg=self.text_bright).pack(anchor=tk.W, pady=(20, 8))

        self.destination_var = tk.StringVar()
        destination_entry = tk.Entry(form, textvariable=self.destination_var, font=("Arial", 14),
                                     bg=self.card_dark, fg=self.text_bright, insertbackground="white", bd=0)
        destination_entry.pack(fill=tk.X, pady=5, ipady=10)

        tk.Label(form, text="Route Preference", font=self.font_subheader,
                 bg=self.bg_gradient_mid, fg=self.text_bright).pack(anchor=tk.W, pady=(20, 8))

        self.preference_var = tk.StringVar(value="Safest")
        preferences = [
            ("Safest Route (Recommended)", "Safest"),
            ("Balanced (Safety + Speed)", "Balanced"),
            ("Fastest Route", "Fastest")
        ]
        for text, val in preferences:
            tk.Radiobutton(form, text=text, variable=self.preference_var, value=val,
                           font=self.font_body, bg=self.bg_gradient_mid, fg=self.text_bright,
                           selectcolor=self.card_dark, activebackground=self.bg_gradient_mid
                           ).pack(anchor=tk.W, padx=12, pady=3)

        self.results_container = tk.Frame(form, bg=self.bg_gradient_mid)
        self.results_container.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        shadow = tk.Frame(form, bg="#000000"); shadow.pack(fill=tk.X, pady=25)
        tk.Button(shadow, text="Find Routes", font=("Arial", 16, "bold"),
                  bg=self.accent_blue, fg="white", activebackground="#3a7bc8", bd=0,
                  cursor="hand2", command=self.find_route, height=3
                  ).pack(fill=tk.X, padx=2, pady=2)
        tk.Frame(form, bg=self.bg_gradient_mid, height=100).pack()

    def find_route(self):
        if not self.destination_var.get().strip():
            messagebox.showwarning("Error", "⚠️ Please enter a destination!")
            return
        for w in self.results_container.winfo_children(): w.destroy()

        current = self.current_var.get()
        destination = self.destination_var.get()
        preference = self.preference_var.get()

        loading_label = tk.Label(self.results_container, text="🔍 Calculating routes...",
                                 font=self.font_subheader, bg=self.bg_gradient_mid, fg=self.accent_cyan)
        loading_label.pack(pady=20); self.root.update()
        time.sleep(1); loading_label.destroy()

        routes = self.generate_sample_routes(current, destination, preference)

        tk.Label(self.results_container, text="Available Routes", font=self.font_header,
                 bg=self.bg_gradient_mid, fg=self.text_bright
                 ).pack(anchor=tk.W, pady=(10, 15))

        for idx, route in enumerate(routes, 1):
            self.create_route_card(self.results_container, route, idx)

        self.update_scroll_region()
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))

    def generate_sample_routes(self, current, destination, preference):
        routes = [
            {"name":"Main Street Route","distance":round(random.uniform(3.0,5.0),1),
             "duration":f"{random.randint(15,25)} min","safety_score":round(random.uniform(8.0,9.5),1),
             "crime_level":"Low","lighting":"Excellent","traffic":"Moderate","recommended":True},
            {"name":"Highway Route","distance":round(random.uniform(4.0,6.0),1),
             "duration":f"{random.randint(10,18)} min","safety_score":round(random.uniform(7.0,8.5),1),
             "crime_level":"Low","lighting":"Good","traffic":"Heavy","recommended":False},
            {"name":"Backstreet Route","distance":round(random.uniform(2.5,4.0),1),
             "duration":f"{random.randint(12,20)} min","safety_score":round(random.uniform(5.0,7.0),1),
             "crime_level":"Medium","lighting":"Poor","traffic":"Light","recommended":False},
        ]
        CRIME = {"Low":1.0,"Medium":0.5,"High":0.0}
        LIGHT = {"Excellent":1.0,"Good":0.7,"Poor":0.2}
        TRAFFIC={"Light":1.0,"Moderate":0.6,"Heavy":0.2}
        durs=[int(r["duration"].split()[0]) for r in routes]
        dists=[r["distance"] for r in routes]
        max_dur=max(durs) or 1
        max_dist=max(dists) or 1
        WEIGHTS={
            "Safest":  dict(safety=0.50, crime=0.20, light=0.15, traffic=0.15, time=0.00, distance=0.00),
            "Fastest": dict(safety=0.10, crime=0.05, light=0.05, traffic=0.05, time=0.50, distance=0.25),
            "Balanced":dict(safety=0.30, crime=0.15, light=0.15, traffic=0.10, time=0.20, distance=0.10),
        }
        w=WEIGHTS.get(preference, WEIGHTS["Balanced"])
        for r in routes:
            dur = int(r["duration"].split()[0])
            score=( w["safety"]*(r["safety_score"]/10.0) + w["crime"]*CRIME[r["crime_level"]]
                   + w["light"]*LIGHT[r["lighting"]] + w["traffic"]*TRAFFIC[r["traffic"]]
                   - w["time"]*(dur/max_dur) - w["distance"]*(r["distance"]/max_dist) )
            r["composite_score"]=round(score,3)
        routes.sort(key=lambda x: x["composite_score"], reverse=True)
        for i,r in enumerate(routes): r["recommended"]=(i==0)
        return routes

    def create_route_card(self, parent, route, index):
        shadow = tk.Frame(parent, bg="#000000"); shadow.pack(fill=tk.X, pady=10)
        card_bg = self.card_elevated if route.get("recommended") else self.card_dark
        border_color = self.accent_cyan if route.get("recommended") else "#000000"
        border = tk.Frame(shadow, bg=border_color); border.pack(fill=tk.X, padx=2, pady=2)
        card = tk.Frame(border, bg=card_bg); card.pack(fill=tk.X, padx=3 if route.get("recommended") else 0,
                                                      pady=3 if route.get("recommended") else 0)
        if route.get("recommended"):
            badge_frame = tk.Frame(card, bg=card_bg); badge_frame.pack(fill=tk.X, padx=20, pady=(15,5))
            tk.Label(badge_frame, text="⭐ RECOMMENDED", font=("Arial",11,"bold"),
                     bg=self.accent_cyan, fg="white", padx=12, pady=5).pack(side=tk.LEFT)

        header = tk.Frame(card, bg=card_bg); header.pack(fill=tk.X, padx=20, pady=(15 if not route.get("recommended") else 10, 5))
        tk.Label(header, text=f"#{index} {route['name']}", font=self.font_subheader, bg=card_bg, fg=self.text_bright
                 ).pack(side=tk.LEFT)
        score = route["safety_score"]
        score_color = self.accent_green if score >= 8 else self.accent_orange if score >= 6 else self.accent_pink
        tk.Label(header, text=f"⭐ {score}", font=("Arial",14,"bold"),
                 bg=score_color, fg="white", padx=10, pady=3).pack(side=tk.RIGHT)

        info_frame = tk.Frame(card, bg=card_bg); info_frame.pack(fill=tk.X, padx=20, pady=10)
        infos=[("📏", f"{route['distance']} km"),("⏱️",route['duration']),
               ("🚨", f"Crime: {route['crime_level']}"),("💡",f"Light: {route['lighting']}"),
               ("🚗", f"Traffic: {route['traffic']}")]
        for icon,text in infos:
            row = tk.Frame(info_frame, bg=card_bg); row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=f"{icon} {text}", font=self.font_body, bg=card_bg,
                     fg=self.text_dim, anchor=tk.W).pack(side=tk.LEFT)

        btn_shadow = tk.Frame(card, bg="#000000"); btn_shadow.pack(fill=tk.X, padx=20, pady=(5, 15))
        tk.Button(btn_shadow, text="📍 Start Navigation", font=("Arial",14,"bold"),
                  bg=self.accent_cyan if route.get("recommended") else self.accent_blue,
                  fg="white", activebackground="#00b8d4", bd=0, cursor="hand2",
                  command=lambda r=route: self.start_navigation(r), height=2
                  ).pack(fill=tk.X, padx=2, pady=2)

    def start_navigation(self, route):
        messagebox.showinfo("Navigation Started",
                            f"Starting navigation on:\n\n"
                            f"Route: {route['name']}\n"
                            f"Distance: {route['distance']} km\n"
                            f"Duration: {route['duration']}\n"
                            f"Safety Score: {route['safety_score']}/10\n\n"
                            f"Stay safe!")
