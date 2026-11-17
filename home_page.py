import tkinter as tk

class HomePage:
    def __init__(self, app):
        self.app = app

    def __getattr__(self, name):
        return getattr(self.app, name)

    def show_home_screen(self):
        self.clear_content()
        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=15).pack()
        self.create_shake_detection_banner()
        self.create_premium_safety_score()
        self.create_recent_activity()
        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=20).pack()

    def create_shake_detection_banner(self):
        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=15)
        banner = tk.Frame(shadow, bg=self.card_dark)
        banner.pack(fill=tk.X, padx=2, pady=2)
        content = tk.Frame(banner, bg=self.card_dark)
        content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            content, text="📳", font=("Arial", 35),
            bg=self.card_dark, fg=self.accent_cyan
        ).pack(side=tk.LEFT, padx=(0, 15))

        text_frame = tk.Frame(content, bg=self.card_dark)
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            text_frame, text="Shake Detection Active",
            font=self.font_subheader, bg=self.card_dark, fg=self.accent_cyan, anchor=tk.W
        ).pack(fill=tk.X)

        tk.Label(
            text_frame, text="Press SPACE 3 times quickly for emergency SOS",
            font=self.font_small, bg=self.card_dark, fg=self.text_dim, anchor=tk.W
        ).pack(fill=tk.X, pady=(3, 0))

        tk.Label(
            text_frame, text="(Simulates phone shake gesture)",
            font=("Arial", 9, "italic"), bg=self.card_dark, fg=self.text_muted, anchor=tk.W
        ).pack(fill=tk.X, pady=(2, 0))

    def create_premium_safety_score(self):
        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=15)
        card = tk.Frame(shadow, bg=self.accent_cyan)
        card.pack(fill=tk.X, padx=2, pady=2)

        header = tk.Frame(card, bg=self.accent_cyan)
        header.pack(fill=tk.X, padx=25, pady=(20, 10))

        tk.Label(
            header, text=f"📍{self.user_location}",
            font=self.font_subheader, bg=self.accent_cyan, fg="white"
        ).pack(side=tk.LEFT)

        tk.Label(
            header, text="🟢 LIVE", font=("Arial", 11, "bold"),
            bg="white", fg=self.accent_green, padx=10, pady=5
        ).pack(side=tk.RIGHT)

        canvas_size = 280
        canvas_frame = tk.Frame(card, bg=self.accent_cyan)
        canvas_frame.pack(pady=20)
        score_canvas = tk.Canvas(
            canvas_frame, width=canvas_size, height=canvas_size,
            bg=self.accent_cyan, highlightthickness=0
        )
        score_canvas.pack()

        safety_score = self.crime_stats.get('overall_risk')
        center_x = canvas_size / 2
        center_y = canvas_size / 2
        radius = 110
        line_width = 12

        score_canvas.create_arc(
            center_x - radius, center_y - radius, center_x + radius, center_y + radius,
            start=0, extent=359.99, outline="#2d3561", width=line_width, style=tk.ARC
        )

        progress_extent = (safety_score / 10.0) * 359.99
        score_canvas.create_arc(
            center_x - radius, center_y - radius, center_x + radius, center_y + radius,
            start=90, extent=-progress_extent, outline=self.accent_green,
            width=line_width, style=tk.ARC
        )

        score_canvas.create_text(
            center_x, center_y - 15, text=str(safety_score),
            font=("Arial", 72, "bold"), fill=self.text_bright
        )
        score_canvas.create_text(
            center_x, center_y + 40, text="RISKY",
            font=("Arial", 16, "bold"), fill=self.text_muted
        )

    def create_recent_activity(self):
        tk.Label(
            self.scrollable_frame, text=" Recent Activity",
            font=self.font_header, bg=self.bg_gradient_mid, fg=self.text_bright
        ).pack(anchor=tk.W, padx=25, pady=(25, 15))

        for report in self.safety_reports[:2]:
            self.create_activity_card(report)

    def create_activity_card(self, report):
        risk_colors = {
            "High": self.accent_pink,
            "Medium": self.accent_orange,
            "Low": self.accent_green
        }

        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=8)

        card = tk.Frame(shadow, bg=self.card_dark, cursor="hand2")
        card.pack(fill=tk.X, padx=2, pady=2)

        tk.Frame(card, bg=risk_colors.get(report["risk"]), width=6).pack(side=tk.LEFT, fill=tk.Y)

        content = tk.Frame(card, bg=self.card_dark)
        content.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=18)

        tk.Label(
            content, text=report["type"],
            font=self.font_subheader, bg=self.card_dark, fg=self.text_bright, anchor=tk.W
        ).pack(fill=tk.X)

        tk.Label(
            content, text=f"📍 {report['distance']} km away  •  🕐 {report['time']}",
            font=self.font_body, bg=self.card_dark, fg=self.text_dim
        ).pack(fill=tk.X, pady=(8, 0))

        badge = tk.Label(
            card, text=report["risk"].upper(), font=("Arial", 11, "bold"),
            bg=risk_colors.get(report["risk"]), fg="white", padx=18, pady=10
        )
        badge.pack(side=tk.RIGHT, padx=20)

        def on_click(event):
            self.pages["reports"].show_incident_detail(report)

        card.bind("<Button-1>", on_click)
        for child in card.winfo_children():
            child.bind("<Button-1>", on_click)
            for grandchild in child.winfo_children():
                grandchild.bind("<Button-1>", on_click)

        def on_enter(event):
            card.config(bg=self.card_elevated)
            content.config(bg=self.card_elevated)
            for ch in content.winfo_children():
                if isinstance(ch, tk.Label):
                    ch.config(bg=self.card_elevated)

        def on_leave(event):
            card.config(bg=self.card_dark)
            content.config(bg=self.card_dark)
            for ch in content.winfo_children():
                if isinstance(ch, tk.Label):
                    ch.config(bg=self.card_dark)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
