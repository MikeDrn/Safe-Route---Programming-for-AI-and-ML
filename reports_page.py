from datetime import datetime
import random
import tkinter as tk
from tkinter import messagebox
import csv
import os


class ReportsPage:
    def __init__(self, app):
        self.app = app

    def __getattr__(self, name):
        return getattr(self.app, name)

    def show_reports_screen(self):
        self.clear_content()

        self.safety_reports = self.load_reports_from_csv()

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()

        tk.Label(
            self.scrollable_frame,
            text="Community Reports",
            font=self.font_title,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(padx=25, pady=15, anchor=tk.W)

        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=10)

        tk.Button(
            shadow,
            text="➕ Report New Incident",
            font=("Arial", 14, "bold"),
            bg=self.accent_cyan,
            fg="white",
            activebackground="#00b8d4",
            bd=0,
            cursor="hand2",
            command=self.show_report_dialog,
            height=2
        ).pack(fill=tk.X, padx=2, pady=2)

        tk.Label(
            self.scrollable_frame,
            text=f"📍 Recent Reports - {self.user_location}",
            font=self.font_subheader,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(anchor=tk.W, padx=25, pady=(20, 15))

        if self.safety_reports:
            for report in self.safety_reports:
                self.create_detailed_report_card(report)
        else:
            shadow = tk.Frame(self.scrollable_frame, bg="#000000")
            shadow.pack(fill=tk.X, padx=25, pady=10)

            tk.Label(
                shadow,
                text="✅ No reports in your area\nBe the first to contribute!",
                font=("Arial", 14),
                bg=self.card_dark,
                fg=self.accent_green,
                padx=20,
                pady=30,
                justify=tk.CENTER
            ).pack(fill=tk.X, padx=2, pady=2)

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=20).pack()

    def create_detailed_report_card(self, report):
        risk_colors = {
            "High": self.accent_pink,
            "Medium": self.accent_orange,
            "Low": self.accent_green
        }

        color = risk_colors.get(report["risk"], self.accent_orange)

        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=10)

        card = tk.Frame(shadow, bg=self.card_dark)
        card.pack(fill=tk.X, padx=2, pady=2)

        tk.Frame(card, bg=color, width=8).pack(side=tk.LEFT, fill=tk.Y)

        content = tk.Frame(card, bg=self.card_dark)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        header = tk.Frame(content, bg=self.card_dark)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text=report["type"],
            font=("Arial", 16, "bold"),
            bg=self.card_dark,
            fg=self.text_bright,
            anchor=tk.W
        ).pack(side=tk.LEFT)

        risk_badge = tk.Frame(header, bg=color)
        risk_badge.pack(side=tk.RIGHT)

        tk.Label(
            risk_badge,
            text=f" {report['risk']} ",
            font=("Arial", 10, "bold"),
            bg=color,
            fg="white"
        ).pack(padx=8, pady=4)

        details_text = f"📅 {report['date']} at {report['time_raw']}\n"
        details_text += f"📍 {report['location']}\n"
        details_text += f"🎯 Distance: {report['distance']} km away\n"
        details_text += f"⏱️ {report['time']}"

        tk.Label(
            content,
            text=details_text,
            font=self.font_body,
            bg=self.card_dark,
            fg=self.text_dim,
            anchor=tk.W,
            justify=tk.LEFT
        ).pack(fill=tk.X, pady=(10, 0))

    def show_incident_detail(self, report):
        self.clear_content()

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()

        back_frame = tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid)
        back_frame.pack(fill=tk.X, padx=25, pady=(10, 5))

        back_btn = tk.Button(
            back_frame,
            text="Back",
            font=("Arial", 14, "bold"),
            bg=self.bg_gradient_mid,
            fg=self.accent_cyan,
            bd=0,
            cursor="hand2",
            command=lambda: self.navigate_to("reports"),
            activebackground=self.bg_gradient_mid,
            activeforeground=self.accent_cyan
        )
        back_btn.pack(side=tk.LEFT)

        tk.Label(
            self.scrollable_frame,
            text="Incident Details",
            font=self.font_title,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(padx=25, pady=(10, 5), anchor=tk.W)

        risk_colors = {
            "High": self.accent_pink,
            "Medium": self.accent_orange,
            "Low": self.accent_green
        }

        risk_badge_frame = tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid)
        risk_badge_frame.pack(padx=25, pady=(5, 20), anchor=tk.W)

        tk.Label(
            risk_badge_frame,
            text=f"{report['risk'].upper()} RISK",
            font=("Arial", 12, "bold"),
            bg=risk_colors.get(report["risk"]),
            fg="white",
            padx=15,
            pady=8
        ).pack(side=tk.LEFT)

        detail_shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        detail_shadow.pack(fill=tk.X, padx=25, pady=10)

        detail_card = tk.Frame(detail_shadow, bg=self.card_dark)
        detail_card.pack(fill=tk.X, padx=2, pady=2)

        detail_content = tk.Frame(detail_card, bg=self.card_dark)
        detail_content.pack(fill=tk.BOTH, padx=25, pady=20)

        tk.Label(
            detail_content,
            text=report["type"],
            font=("Arial", 24, "bold"),
            bg=self.card_dark,
            fg=self.text_bright,
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 20))

        details = [
            ("Report ID", report.get("id", "N/A")),
            ("Date", report.get("date", "N/A")),
            ("Time", report.get("time_raw", "N/A")),
            ("Location", report.get("location", "N/A")),
            ("City", report.get("city", "N/A")),
            ("State", report.get("state", "N/A")),
            ("Crime Type", report.get("crime_type", "N/A")),
            ("Distance", f"{report['distance']} km away"),
            ("Reported", report["time"])
        ]

        for label, value in details:
            row = tk.Frame(detail_content, bg=self.card_dark)
            row.pack(fill=tk.X, pady=8)

            tk.Label(
                row,
                text=label,
                font=("Arial", 13, "bold"),
                bg=self.card_dark,
                fg=self.text_dim,
                anchor=tk.W,
                width=15
            ).pack(side=tk.LEFT)

            tk.Label(
                row,
                text=value,
                font=("Arial", 13),
                bg=self.card_dark,
                fg=self.text_bright,
                anchor=tk.W
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            detail_content,
            text="Victim Information",
            font=("Arial", 18, "bold"),
            bg=self.card_dark,
            fg=self.text_bright,
            anchor=tk.W
        ).pack(fill=tk.X, pady=(25, 15))

        victim_details = [
            ("Age", report.get("victim_age", "N/A") if report.get("victim_age") else "N/A"),
            ("Gender", report.get("victim_gender", "N/A")),
            ("Race", report.get("victim_race", "N/A"))
        ]

        for label, value in victim_details:
            vrow = tk.Frame(detail_content, bg=self.card_dark)
            vrow.pack(fill=tk.X, pady=8)
            tk.Label(
                vrow,
                text=label,
                font=("Arial", 13, "bold"),
                bg=self.card_dark,
                fg=self.text_dim,
                anchor=tk.W,
                width=15
            ).pack(side=tk.LEFT)
            tk.Label(
                vrow,
                text=value,
                font=("Arial", 13),
                bg=self.card_dark,
                fg=self.text_bright,
                anchor=tk.W
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=20).pack()

    def show_report_dialog(self):
        self.clear_content()

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()

        tk.Label(
            self.scrollable_frame,
            text="Report Incident",
            font=self.font_title,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(padx=25, pady=15, anchor=tk.W)

        form = tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid)
        form.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        tk.Label(
            form,
            text="Incident Type",
            font=self.font_subheader,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(anchor=tk.W, pady=(10, 8))

        self.incident_type_var = tk.StringVar(value="")
        incident_types = [
            "Suspicious Activity",
            "Poor Lighting",
            "Harassment",
            "Reckless Driving",
            "Noise Disturbance",
            "Vandalism",
            "Stalking",
            "Other"
        ]

        for incident_type in incident_types:
            tk.Radiobutton(
                form,
                text=incident_type,
                variable=self.incident_type_var,
                value=incident_type,
                font=self.font_body,
                bg=self.bg_gradient_mid,
                fg=self.text_bright,
                selectcolor=self.card_dark,
                activebackground=self.bg_gradient_mid
            ).pack(anchor=tk.W, padx=12, pady=3)

        tk.Label(
            form,
            text="Location",
            font=self.font_subheader,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(anchor=tk.W, pady=(20, 8))

        self.incident_location_var = tk.StringVar(value=self.user_location)
        location_entry = tk.Entry(
            form,
            textvariable=self.incident_location_var,
            font=("Arial", 14),
            bg=self.card_dark,
            fg=self.text_bright,
            insertbackground="white",
            bd=0,
            state=tk.DISABLED
        )
        location_entry.pack(fill=tk.X, pady=5, ipady=10)

        tk.Label(
            form,
            text="Date & Time",
            font=self.font_subheader,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(anchor=tk.W, pady=(20, 8))

        tk.Label(
            form,
            text="Date (MM/DD/YYYY)",
            font=self.font_body,
            bg=self.bg_gradient_mid,
            fg=self.text_dim
        ).pack(anchor=tk.W, padx=12, pady=(5, 3))

        self.incident_date_var = tk.StringVar(value=datetime.now().strftime('%m/%d/%Y'))
        date_entry = tk.Entry(
            form,
            textvariable=self.incident_date_var,
            font=("Arial", 14),
            bg=self.card_dark,
            fg=self.text_bright,
            insertbackground="white",
            bd=0,
            state=tk.DISABLED
        )
        date_entry.pack(fill=tk.X, padx=12, pady=5, ipady=8)

        tk.Label(
            form,
            text="Time (HH:MM)",
            font=self.font_body,
            bg=self.bg_gradient_mid,
            fg=self.text_dim,
            state=tk.DISABLED
        ).pack(anchor=tk.W, padx=12, pady=(10, 3))

        self.incident_time_var = tk.StringVar(value=datetime.now().strftime('%H:%M'))
        time_entry = tk.Entry(
            form,
            textvariable=self.incident_time_var,
            font=("Arial", 14),
            bg=self.card_dark,
            fg=self.text_bright,
            insertbackground="white",
            bd=0,
            state=tk.DISABLED
        )
        time_entry.pack(fill=tk.X, padx=12, pady=5, ipady=8)

        tk.Label(
            form,
            text="Victim Information",
            font=self.font_subheader,
            bg=self.bg_gradient_mid,
            fg=self.text_bright
        ).pack(anchor=tk.W, pady=(20, 8))

        tk.Label(
            form,
            text="Age",
            font=self.font_body,
            bg=self.bg_gradient_mid,
            fg=self.text_dim
        ).pack(anchor=tk.W, padx=12, pady=(5, 3))

        self.victim_age_var = tk.StringVar(value="")
        age_entry = tk.Entry(
            form,
            textvariable=self.victim_age_var,
            font=("Arial", 14),
            bg=self.card_dark,
            fg=self.text_bright,
            insertbackground="white",
            bd=0
        )
        age_entry.pack(fill=tk.X, padx=12, pady=5, ipady=8)

        tk.Label(
            form,
            text="Gender",
            font=self.font_body,
            bg=self.bg_gradient_mid,
            fg=self.text_dim
        ).pack(anchor=tk.W, padx=12, pady=(10, 3))

        self.victim_gender_var = tk.StringVar(value="")
        genders = ["Male", "Female", "Other", "Prefer not to say"]

        gender_frame = tk.Frame(form, bg=self.bg_gradient_mid)
        gender_frame.pack(fill=tk.X, padx=12, pady=5)

        for gender in genders:
            tk.Radiobutton(
                gender_frame,
                text=gender,
                variable=self.victim_gender_var,
                value=gender,
                font=self.font_body,
                bg=self.bg_gradient_mid,
                fg=self.text_bright,
                selectcolor=self.card_dark,
                activebackground=self.bg_gradient_mid
            ).pack(anchor=tk.W, pady=2)

        tk.Label(
            form,
            text="Race",
            font=self.font_body,
            bg=self.bg_gradient_mid,
            fg=self.text_dim
        ).pack(anchor=tk.W, padx=12, pady=(10, 3))

        self.victim_race_var = tk.StringVar(value="Unknown")
        race_options = ["White", "Black", "Asian", "Hispanic", "Other", "Unknown"]

        race_frame = tk.Frame(form, bg=self.bg_gradient_mid)
        race_frame.pack(anchor=tk.W, padx=12, pady=5)

        for race in race_options:
            tk.Radiobutton(
                race_frame,
                text=race,
                variable=self.victim_race_var,
                value=race,
                font=self.font_body,
                bg=self.bg_gradient_mid,
                fg=self.text_bright,
                selectcolor=self.card_dark,
                activebackground=self.bg_gradient_mid
            ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Frame(form, bg=self.bg_gradient_mid, height=20).pack()

        shadow = tk.Frame(form, bg="#000000")
        shadow.pack(fill=tk.X, pady=10)

        tk.Button(
            shadow,
            text="Submit Report",
            font=("Arial", 16, "bold"),
            bg=self.accent_cyan,
            fg="white",
            activebackground="#00b8d4",
            bd=0,
            cursor="hand2",
            command=self.submit_report,
            height=3
        ).pack(fill=tk.X, padx=2, pady=2)

        shadow = tk.Frame(form, bg="#000000")
        shadow.pack(fill=tk.X, pady=(5, 20))

        tk.Button(
            shadow,
            text="Cancel",
            font=("Arial", 14),
            bg=self.card_dark,
            fg=self.text_dim,
            activebackground=self.card_elevated,
            bd=0,
            cursor="hand2",
            command=lambda: self.navigate_to("reports"),
            height=2
        ).pack(fill=tk.X, padx=2, pady=2)

    def submit_report(self):
        incident_type = self.incident_type_var.get()
        location = self.incident_location_var.get()
        risk_level = "Medium"
        incident_date = self.incident_date_var.get()
        incident_time = self.incident_time_var.get()
        victim_age = self.victim_age_var.get()
        victim_gender = self.victim_gender_var.get()
        victim_race = self.victim_race_var.get() or "Not specified"

        if not incident_type:
            messagebox.showerror("Error", "Please select an incident type")
            return

        if not victim_age or not victim_gender:
            messagebox.showerror("Error", "Please provide victim age and gender")
            return

        if int(victim_age) > 100 or int(victim_age) <= 0:
            messagebox.showerror("Error", "Please provide a victim age greater than 0 and less than 100")
            return

        result = messagebox.askyesno(
            "Confirm Report",
            f"📋 Report Summary:\n\n"
            f"Type: {incident_type}\n"
            f"Location: {location}\n"
            f"Date: {incident_date}\n"
            f"Time: {incident_time}\n"
            f"Victim Age: {victim_age}\n"
            f"Victim Gender: {victim_gender}\n"
            f"Victim Race: {victim_race}\n\n"
            f"This will be shared with local authorities and community members."
        )

        if result:
            incident_to_crime = {
                "Suspicious Activity": "Robbery",
                "Poor Lighting": "Vandalism",
                "Harassment": "Assault",
                "Reckless Driving": "Vehicle Theft",
                "Noise Disturbance": "Domestic Disturbance",
                "Vandalism": "Vandalism",
                "Stalking": "Assault",
                "Other": "Theft"
            }

            crime_type = incident_to_crime.get(incident_type, "Theft")

            success = self.add_report_to_csv(crime_type, location, incident_date, incident_time,
                                             victim_age, victim_gender, victim_race)

            if success:
                messagebox.showinfo(
                    "Report Submitted",
                    f"✅ Thank you for your report!\n\n"
                    f"Your incident report has been submitted successfully.\n\n"
                    f"Status: Under Review\n\n"
                    f"You'll be notified of any updates."
                )
            else:
                messagebox.showerror(
                    "Error",
                    "❌ Failed to submit report. Please try again."
                )

            self.navigate_to("reports")
