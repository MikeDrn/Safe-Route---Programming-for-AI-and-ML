import tkinter as tk

from auth_page import AuthPage

from home_page import HomePage
from route_page import RoutePage
from reports_page import ReportsPage
from guardians_page import GuardiansPage
from stats_page import StatsPage
from predict_page import PredictPage

from tkinter import messagebox, font as tkfont
from datetime import datetime
import random
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('TkAgg')
import numpy as np
import csv
import os


class SafeRouteApp:

    def __init__(self, root, user_data):
        self.root = root
        self.root.title("SafeGuard Pro")

        self.user_data = user_data
        self.current_user_name = user_data['name']
        self.current_user_email = user_data['email']

        self.width = 620
        self.height = 900
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        self.bg_gradient_start = "#0d0f2a"
        self.bg_gradient_mid = "#16203e"
        self.bg_gradient_end = "#16203e"
        self.bg_dark = "#16203e"
        self.bg_medium = "#16203e"

        self.card_glass = "#ffffff"
        self.card_dark = "#0d0f2a"
        self.card_elevated = "#3d4876"

        self.accent_cyan = "#DAA520"
        self.accent_pink = "#ff2e63"
        self.accent_purple = "#a855f7"
        self.accent_orange = "#ff6b35"
        self.accent_green = "#00f5a0"
        self.accent_gold = "#ffd700"
        self.accent_blue = "#4facfe"

        self.text_bright = "#ffffff"
        self.text_dim = "#b8c5d6"
        self.text_muted = "#7c8db0"

        self.root.configure(bg=self.bg_gradient_start)

        self.reports_csv = "lebanon_crime_sample.csv"
        self.user_location = random.choice([
            "Tyre", "Sidon", "Zahle", "Jounieh", "Bcharre", "Bourj Hammoud",
            "Jeita", "Beit Meri", "Tripoli", "Ghazir", "Aley", "Dekwaneh",
            "Zgharta", "Ghazir", "Batroun", "Nabatieh", "Byblos", "Choueifat", "Beirut"
        ])

        self.safety_reports = self.load_reports_from_csv()
        self.crime_stats = self.calculate_crime_statistics()

        self.location_sharing = False
        self.current_screen = "home"

        self.shake_count = 0
        self.shake_threshold = 3
        self.shake_timeout = None
        self.warning_notification_active = False
        self.setup_fonts()
        self.create_mobile_interface()

        self.root.after(20000, self.check_and_show_warning)

        self.pages = {
            "home": HomePage(self),
            "route": RoutePage(self),
            "reports": ReportsPage(self),
            "guards": GuardiansPage(self),
            "stats": StatsPage(self),
            "predict": PredictPage(self),
        }
        self.navigate_to("home")

    def setup_fonts(self):
        try:
            self.font_title = tkfont.Font(family="Helvetica", size=28, weight="bold")
            self.font_header = tkfont.Font(family="Helvetica", size=20, weight="bold")
            self.font_subheader = tkfont.Font(family="Helvetica", size=16, weight="bold")
            self.font_body = tkfont.Font(family="Helvetica", size=12)
            self.font_small = tkfont.Font(family="Helvetica", size=10)
        except:
            self.font_title = ("Arial", 28, "bold")
            self.font_header = ("Arial", 20, "bold")
            self.font_subheader = ("Arial", 16, "bold")
            self.font_body = ("Arial", 12)
            self.font_small = ("Arial", 10)

    def load_reports_from_csv(self):
        reports = []

        # Crime type to emoji and risk mapping
        crime_mapping = {
            "Assault": {"emoji": "👊", "type": "Assault", "risk": "High"},
            "Robbery": {"emoji": "💰", "type": "Robbery", "risk": "High"},
            "Theft": {"emoji": "🎒", "type": "Theft", "risk": "Medium"},
            "Burglary": {"emoji": "🏠", "type": "Burglary", "risk": "High"},
            "Vandalism": {"emoji": "🔨", "type": "Vandalism", "risk": "Low"},
            "Vehicle Theft": {"emoji": "🚗", "type": "Vehicle Theft", "risk": "Medium"},
            "Pickpocketing": {"emoji": "👜", "type": "Pickpocketing", "risk": "Medium"},
            "Fraud": {"emoji": "💳", "type": "Fraud", "risk": "Medium"},
            "Drug Possession": {"emoji": "💊", "type": "Drug Possession", "risk": "Medium"},
            "Arson": {"emoji": "🔥", "type": "Arson", "risk": "High"},
            "Domestic Disturbance": {"emoji": "🏡", "type": "Domestic Disturbance", "risk": "High"}
        }

        try:
            if not os.path.exists(self.reports_csv):
                return []

            with open(self.reports_csv, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if self.user_location in row.get('city', ''):
                        crime_type = row.get('crime_type', 'Unknown')
                        crime_info = crime_mapping.get(crime_type,
                                                       {"emoji": "⚠️", "type": "Suspicious Activity", "risk": "Medium"})

                        # Calculate time ago
                        try:
                            # First, try to get the date from the row
                            date_str = row.get('date', '')
                            incident_time = row.get('time', '00:00')

                            # Try multiple date formats
                            incident_datetime = None
                            date_formats = [
                                '%Y-%m-%d',
                                '%m/%d/%Y',
                                '%d/%m/%Y',
                                '%Y/%m/%d'
                            ]

                            for date_format in date_formats:
                                try:
                                    incident_datetime = datetime.strptime(f"{date_str} {incident_time}",
                                                                          f"{date_format} %H:%M")
                                    break
                                except ValueError:
                                    continue

                            if incident_datetime:
                                time_diff = datetime.now() - incident_datetime
                                if time_diff.days > 0:
                                    time_ago = f"{time_diff.days} days ago"
                                elif time_diff.seconds // 3600 > 0:
                                    time_ago = f"{time_diff.seconds // 3600} hrs ago"
                                else:
                                    time_ago = f"{time_diff.seconds // 60} min ago"
                            else:
                                time_ago = "recently"
                        except Exception as e:
                            time_ago = "recently"

                        distance = round(random.uniform(0.1, 3.0), 1)

                        reports.append({
                            "type": f"{crime_info['emoji']} {crime_info['type']}",
                            "time": time_ago,
                            "distance": distance,
                            "risk": crime_info['risk'],
                            # Full details for detail view
                            "id": row.get('id', 'N/A'),
                            "crime_type": crime_type,
                            "date": row.get('date', 'N/A'),
                            "time_raw": row.get('time', 'N/A'),
                            "location": row.get('location_description', 'N/A'),
                            "city": row.get('city', 'N/A'),
                            "state": row.get('state', 'N/A'),
                            "victim_age": row.get('victim_age', 'N/A'),
                            "victim_gender": row.get('victim_gender', 'N/A'),
                            "victim_race": row.get('victim_race', 'N/A')
                        })

            reports.sort(key=lambda x: x['distance'])
            return reports[:50]
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return []

    def calculate_crime_statistics(self):
        try:
            property_crimes = ['Theft', 'Burglary', 'Vehicle Theft', 'Vandalism', 'Fraud', 'Pickpocketing',
                               'Drug Possession']
            violent_crimes = ['Assault', 'Robbery', 'Arson', 'Domestic Disturbance']

            total_count = property_count = violent_count = 0
            property_score = violent_score = overall_risk = 10.0
            with open(self.reports_csv, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if self.user_location in row.get('city', ''):
                        total_count += 1
                        crime_type = row.get('crime_type', '')
                        if crime_type in property_crimes:
                            property_count += 1
                        elif crime_type in violent_crimes:
                            violent_count += 1
            if total_count > 0:
                property_score = min((property_count / total_count) * 10, 10.0)
                violent_score = min((violent_count / total_count) * 10, 10.0)
                crime_rate = ((property_score * 0.6) + violent_score)
                overall_risk = max(crime_rate, 0.0)
            else:
                property_score = violent_score = 0.0
                overall_risk = 10.0
            return {
                "property_crime": round(property_score, 1),
                "violent_crime": round(violent_score, 1),
                "overall_risk": round(overall_risk, 1)
            }
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return {"property_crime": 0.0, "violent_crime": 0.0, "overall_risk": 10.0}

    def _mock_success_alert(self):
        messagebox.showinfo("Test Submitted", "Your prediction request was registered (Mock Data).")

    def get_next_report_id(self):
        try:
            if not os.path.exists(self.reports_csv):
                return 1

            with open(self.reports_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if not rows:
                    return 1

                max_id = max(int(row['id']) for row in rows if row['id'].isdigit())
                max_id += 1
                return max_id
        except Exception as e:
            print(f"Error getting next report ID: {e}")
            return 1

    def add_report_to_csv(self, crime_type, location, date_str, time_str, victim_age, victim_gender, victim_race):
        try:
            try:
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = datetime.now().strftime('%Y-%m-%d')

            new_id = self.get_next_report_id()

            new_row = {
                'id': str(new_id),
                'crime_type': crime_type,
                'date': formatted_date,
                'time': time_str,
                'location_description': location,
                'city': self.user_location,
                'state': 'Lebanon',
                'victim_age': victim_age,
                'victim_gender': victim_gender,
                'victim_race': victim_race
            }

            rows = []
            fieldnames = ['id', 'crime_type', 'date', 'time', 'location_description', 'city', 'state',
                          'victim_age', 'victim_gender', 'victim_race']

            if os.path.exists(self.reports_csv):
                with open(self.reports_csv, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    fieldnames = csv_reader.fieldnames or fieldnames
                    rows = list(csv_reader)

            rows.append(new_row)

            with open(self.reports_csv, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            self.safety_reports = self.load_reports_from_csv()
            self.crime_stats = self.calculate_crime_statistics()

            return True

        except Exception as e:
            print(f"Error adding report to CSV: {e}")
            return False

    def create_mobile_interface(self):
        self.create_premium_status_bar()
        self.create_content_area()
        self.create_premium_bottom_nav()
        self.root.bind('<space>', self.on_shake)

    def create_premium_status_bar(self):
        status_frame = tk.Frame(self.root, bg=self.bg_gradient_start, height=50)
        status_frame.pack(fill=tk.X);
        status_frame.pack_propagate(False)

        tk.Label(status_frame, text=datetime.now().strftime('%H:%M'),
                 font=("Arial", 14, "bold"), bg=self.bg_gradient_start, fg=self.text_bright
                 ).pack(side=tk.LEFT, padx=20, pady=12)

        user_label = tk.Label(status_frame, text=f"👤 {self.current_user_name}",
                              font=("Arial", 12), bg=self.bg_gradient_start, fg=self.text_dim,
                              cursor="hand2")
        user_label.pack(side=tk.RIGHT, padx=20, pady=12)

        user_label.bind("<Button-1>", lambda e: self.confirm_logout())

        def on_enter(e):
            user_label.config(fg=self.accent_cyan)

        def on_leave(e):
            user_label.config(fg=self.text_dim)

        user_label.bind("<Enter>", on_enter)
        user_label.bind("<Leave>", on_leave)

    def create_content_area(self):
        self.content_container = tk.Frame(self.root, bg=self.bg_gradient_mid)
        self.content_container.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.content_container, bg=self.bg_gradient_mid, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.content_container, orient=tk.VERTICAL,
                                      command=self.canvas.yview, width=8, bg=self.bg_medium,
                                      troughcolor=self.bg_dark, activebackground=self.accent_cyan)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_gradient_mid)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW, width=self.width)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bind_main_canvas_scroll()

    def bind_main_canvas_scroll(self):
        self.canvas.unbind('<Enter>')
        self.canvas.unbind('<Leave>')
        self.canvas.unbind_all("<MouseWheel>")

        def on_mousewheel(event): self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def on_enter(event): self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        def on_leave(event): self.canvas.unbind_all("<MouseWheel>")

        self.canvas.bind('<Enter>', on_enter)
        self.canvas.bind('<Leave>', on_leave)

    def rebind_main_canvas_scroll(self):
        self.bind_main_canvas_scroll()

    def update_scroll_region(self):
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear_content(self):
        for w in self.scrollable_frame.winfo_children(): w.destroy()
        self.canvas.yview_moveto(0)
        self.update_scroll_region()
        self.bind_main_canvas_scroll()

    def confirm_logout(self):
        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to log out?",
            icon='question'
        )

        if result:
            self.root.destroy()

            login_root = tk.Tk()

            def on_login(user_data):
                login_root.destroy()
                main_root = tk.Tk()
                SafeRouteApp(main_root, user_data)
                main_root.mainloop()

            AuthPage(login_root, on_login)
            login_root.mainloop()

    def create_premium_bottom_nav(self):
        nav_frame = tk.Frame(self.root, bg=self.card_dark, height=85)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X);
        nav_frame.pack_propagate(False)
        nav_items = [
            ("🏠", "Home", "home", self.accent_cyan),
            ("🗺️", "Route", "route", self.accent_blue),
            ("📊", "Reports", "reports", self.accent_purple),
            ("🔮", "Predict", "predict", self.accent_gold),
            ("👥", "Guards", "guards", self.accent_green),
            ("📈", "Stats", "stats", self.accent_orange),
        ]
        self.nav_buttons = {}
        for icon, label, screen_id, color in nav_items:
            btn_frame = tk.Frame(nav_frame, bg=self.card_dark)
            btn_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            btn = tk.Button(btn_frame, text=f"{icon}\n{label}", font=("Arial", 14),
                            bg=self.card_dark, fg=color if screen_id == self.current_screen else self.text_dim,
                            activebackground=self.card_dark, bd=0, cursor="hand2",
                            command=lambda s=screen_id: self.navigate_to(s))
            btn.pack(expand=True, fill=tk.BOTH, pady=10)
            self.nav_buttons[screen_id] = (btn, icon, label, color)

            def on_enter(e, b=btn):
                if b.cget("fg") != self.text_bright: b.config(fg=self.text_bright)

            def on_leave(e, b=btn, c=color, s=screen_id):
                if s != self.current_screen: b.config(fg=self.text_dim)

            btn.bind("<Enter>", on_enter);
            btn.bind("<Leave>", on_leave)

    def navigate_to(self, screen_id):
        old_screen = self.current_screen
        self.current_screen = screen_id
        for sid, (btn, icon, label, color) in self.nav_buttons.items():
            btn.config(fg=(color if sid == screen_id else self.text_dim), text=f"{icon}\n{label}")
        # Delegate to page handlers
        if screen_id == "home":
            self.pages["home"].show_home_screen()
        elif screen_id == "route":
            self.pages["route"].show_route_screen()
        elif screen_id == "reports":
            self.pages["reports"].show_reports_screen()
        elif screen_id == "guards":
            self.pages["guards"].show_guardians_screen()
        elif screen_id == "stats":
            self.pages["stats"].show_stats_screen()
        elif screen_id == "predict":
            self.pages["predict"].show_predict_screen()
        self.root.after(100, self.update_scroll_region)

    def on_shake(self, event):
        self.shake_count += 1
        if self.shake_timeout:
            self.root.after_cancel(self.shake_timeout)
        self.shake_timeout = self.root.after(2000, self.reset_shake_count)
        if self.shake_count >= self.shake_threshold:
            self.reset_shake_count()
            self.show_sos_countdown()

    def reset_shake_count(self):
        self.shake_count = 0
        self.shake_timeout = None

    def show_sos_countdown(self):
        overlay = tk.Toplevel(self.root)
        overlay.title("Emergency SOS")
        overlay.geometry(f"{self.width}x{self.height}")
        overlay.transient(self.root)
        overlay.grab_set()
        overlay.resizable(False, False)

        overlay.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y()}")

        overlay.configure(bg=self.accent_pink)

        content = tk.Frame(overlay, bg=self.accent_pink)
        content.pack(expand=True, fill=tk.BOTH)

        tk.Label(
            content, text="🚨", font=("Arial", 80),
            bg=self.accent_pink, fg="white"
        ).pack(pady=(80, 20))

        tk.Label(
            content, text="EMERGENCY SOS",
            font=("Arial", 32, "bold"),
            bg=self.accent_pink, fg="white"
        ).pack(pady=10)

        countdown_label = tk.Label(
            content, text="5",
            font=("Arial", 120, "bold"),
            bg=self.accent_pink, fg="white"
        )
        countdown_label.pack(pady=30)

        tk.Label(
            content, text="Alerting emergency contacts...",
            font=("Arial", 16),
            bg=self.accent_pink, fg="white"
        ).pack(pady=10)

        cancel_btn = tk.Button(
            content, text="CANCEL",
            font=("Arial", 16, "bold"),
            bg="white", fg=self.accent_pink,
            activebackground="#f0f0f0",
            cursor="hand2",
            padx=40, pady=15,
            command=overlay.destroy
        )
        cancel_btn.pack(pady=40)

        countdown = [5]

        def update_countdown():
            countdown[0] -= 1
            if countdown[0] > 0:
                countdown_label.config(text=str(countdown[0]))
                overlay.after(1000, update_countdown)
            else:
                overlay.destroy()
                self.send_sos_alert()

        overlay.after(1000, update_countdown)

    def send_sos_alert(self):
        messagebox.showinfo(
            "SOS Alert Sent",
            f"Emergency alert has been sent to your guardians!\n\n"
            f"Location: {self.user_location}\n"
            f"Time: {datetime.now().strftime('%H:%M:%S')}\n\n"
            f"Your emergency contacts have been notified."
        )

    def check_and_show_warning(self):
        pass


def main():
    root = tk.Tk()

    def on_login_success(user_data):
        for widget in root.winfo_children():
            widget.destroy()

        app = SafeRouteApp(root, user_data)

    auth = AuthPage(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
