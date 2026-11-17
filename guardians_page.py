import tkinter as tk
from tkinter import messagebox
import csv
import os


class GuardiansPage:
    def __init__(self, app):
        self.app = app

    def __getattr__(self, name):
        return getattr(self.app, name)

    def show_guardians_screen(self):
        self.clear_content()

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()

        tk.Label(
            self.scrollable_frame, text="My Guardians",
            font=self.font_title, bg=self.bg_gradient_mid, fg=self.text_bright
        ).pack(padx=25, pady=15, anchor=tk.W)

        self.create_location_sharing_card()

        tk.Label(
            self.scrollable_frame, text="Active Guardians",
            font=self.font_header, bg=self.bg_gradient_mid, fg=self.text_bright
        ).pack(anchor=tk.W, padx=25, pady=(25, 15))

        guardians_list = self.load_guardians_from_csv()

        if guardians_list:
            for guardian_name in guardians_list:
                is_active = True
                last_seen = "Recently"
                self.create_premium_guardian_card(
                    guardian_name,
                    ("Active" if is_active else "Offline", last_seen, is_active)
                )
        else:
            shadow = tk.Frame(self.scrollable_frame, bg="#000000")
            shadow.pack(fill=tk.X, padx=25, pady=20)

            empty_frame = tk.Frame(shadow, bg=self.card_dark)
            empty_frame.pack(fill=tk.X, padx=2, pady=2)

            empty_content = tk.Frame(empty_frame, bg=self.card_dark)
            empty_content.pack(fill=tk.X, padx=20, pady=30)

            tk.Label(
                empty_content,
                text="No guardians yet",
                font=self.font_subheader,
                bg=self.card_dark,
                fg=self.text_dim
            ).pack()

            tk.Label(
                empty_content,
                text="Add trusted contacts to share your safety status",
                font=self.font_body,
                bg=self.card_dark,
                fg=self.text_muted
            ).pack(pady=(10, 0))

        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=25)

        add_btn = tk.Button(
            shadow, text="➕  Add New Guardian", font=("Arial", 15, "bold"),
            bg=self.accent_purple, fg="white", activebackground="#8e44ad",
            bd=0, cursor="hand2", command=self.show_add_guardian_dialog, height=3
        )
        add_btn.pack(fill=tk.X, padx=2, pady=2)

        self.root.after(100, self.update_scroll_region)

    def load_guardians_from_csv(self):
        users_csv = "users.csv"
        current_user = self.current_user_name

        try:
            if not os.path.exists(users_csv):
                return []

            with open(users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['name'].strip().lower() == current_user.strip().lower():
                        guardians_str = row.get('guardians', '').strip()
                        if guardians_str:
                            guardians_list = [g.strip() for g in guardians_str.split(',') if g.strip()]
                            return guardians_list
                        else:
                            return []

            return []

        except Exception as e:
            print(f"Error loading guardians from CSV: {e}")
            import traceback
            traceback.print_exc()
            return []

    def create_location_sharing_card(self):
        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=15)

        card = tk.Frame(shadow, bg=self.card_dark)
        card.pack(fill=tk.X, padx=2, pady=2)

        inner = tk.Frame(card, bg=self.card_dark)
        inner.pack(fill=tk.X, padx=25, pady=20)

        tk.Label(
            inner, text="📍 Location Sharing",
            font=self.font_header, bg=self.card_dark, fg=self.text_bright
        ).pack(anchor=tk.W)

        status_text = "🟢 Broadcasting to all guardians" if self.location_sharing else "🔴 Currently disabled"
        tk.Label(
            inner, text=status_text, font=self.font_body,
            bg=self.card_dark, fg=self.accent_green if self.location_sharing else self.accent_pink
        ).pack(anchor=tk.W, pady=(8, 15))

        toggle_btn = tk.Button(
            inner,
            text="⏸️ Pause Sharing" if self.location_sharing else "▶️ Start Sharing",
            font=("Arial", 14, "bold"),
            bg=self.accent_pink if self.location_sharing else self.accent_green,
            fg="white", activebackground="#c0392b" if self.location_sharing else "#27ae60",
            bd=0, cursor="hand2", command=self.toggle_location_sharing, height=2
        )
        toggle_btn.pack(fill=tk.X)

    def create_premium_guardian_card(self, name, info):
        status, last_seen, is_active = info

        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=8)

        card = tk.Frame(shadow, bg=self.card_dark)
        card.pack(fill=tk.X, padx=2, pady=2)

        inner = tk.Frame(card, bg=self.card_dark)
        inner.pack(fill=tk.X, padx=20, pady=18)

        container = tk.Frame(inner, bg=self.card_dark)
        container.pack(fill=tk.X)

        avatar_color = self.accent_cyan if is_active else self.text_muted
        # Get first letter of name for avatar
        first_letter = name[0].upper() if name else "?"
        avatar = tk.Label(
            container, text=first_letter,
            font=("Arial", 22, "bold"), bg=avatar_color, fg="white",
            width=3, height=1
        )
        avatar.pack(side=tk.LEFT, padx=(0, 18))

        info_frame = tk.Frame(container, bg=self.card_dark)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            info_frame, text=name, font=("Arial", 17, "bold"),
            bg=self.card_dark, fg=self.text_bright, anchor=tk.W
        ).pack(fill=tk.X)

        status_frame = tk.Frame(info_frame, bg=self.card_dark)
        status_frame.pack(fill=tk.X, pady=(5, 0))

        status_color = self.accent_green if is_active else self.text_muted
        tk.Label(status_frame, text="⬤", font=("Arial", 16), bg=self.card_dark, fg=status_color).pack(side=tk.LEFT)
        tk.Label(
            status_frame, text=f"{status}  •  {last_seen}",
            font=self.font_body, bg=self.card_dark, fg=self.text_dim
        ).pack(side=tk.LEFT, padx=(8, 0))

    def toggle_location_sharing(self):
        self.location_sharing = not self.location_sharing
        self.navigate_to("guards")

    def show_add_guardian_dialog(self):
        self.clear_content()

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()

        tk.Label(
            self.scrollable_frame, text="➕ Add New Guardian",
            font=self.font_title, bg=self.bg_gradient_mid, fg=self.text_bright
        ).pack(padx=25, pady=(12, 6), anchor=tk.W)

        form = tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid)
        form.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        tk.Label(form, text="Full Name", font=self.font_subheader,
                 bg=self.bg_gradient_mid, fg=self.text_bright).pack(anchor=tk.W, pady=(6, 6))
        self.guard_name_var = tk.StringVar()
        tk.Entry(form, textvariable=self.guard_name_var, font=("Arial", 14),
                 bg=self.card_dark, fg=self.text_bright, insertbackground="white", bd=0
                 ).pack(fill=tk.X, pady=4, ipady=10)

        toggle = tk.Frame(form, bg=self.bg_gradient_mid)
        toggle.pack(fill=tk.X, pady=(16, 6))
        self.guard_active_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            toggle, text="Mark as Active", variable=self.guard_active_var,
            font=self.font_body, bg=self.bg_gradient_mid, fg=self.text_bright,
            activebackground=self.bg_gradient_mid, selectcolor=self.card_dark
        ).pack(anchor=tk.W)

        actions_shadow = tk.Frame(form, bg="#000000")
        actions_shadow.pack(fill=tk.X, pady=(22, 8))
        tk.Button(
            actions_shadow, text="Save Guardian", font=("Arial", 16, "bold"),
            bg=self.accent_green, fg="white", activebackground="#27ae60",
            bd=0, cursor="hand2", command=self.submit_new_guardian, height=3
        ).pack(fill=tk.X, padx=2, pady=2)

        back_shadow = tk.Frame(form, bg="#000000")
        back_shadow.pack(fill=tk.X, pady=8)
        tk.Button(
            back_shadow, text="Cancel", font=("Arial", 14, "bold"),
            bg=self.card_dark, fg=self.text_dim, activebackground=self.card_elevated,
            bd=0, cursor="hand2", command=lambda: self.navigate_to("guards"), height=2
        ).pack(fill=tk.X, padx=2, pady=2)

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=40).pack()
        self.root.after(100, self.update_scroll_region)

    def check_guardian_exists_in_system(self, guardian_name):
        users_csv = "users.csv"
        try:
            if not os.path.exists(users_csv):
                return False

            with open(users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['name'].strip().lower() == guardian_name.strip().lower():
                        return True
            return False
        except Exception as e:
            print(f"Error checking guardian existence: {e}")
            return False

    def check_guardian_not_duplicate(self, guardian_name):
        users_csv = "users.csv"
        current_user = self.current_user_name

        try:
            if not os.path.exists(users_csv):
                return True

            with open(users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['name'].strip().lower() == current_user.strip().lower():
                        guardians_str = row.get('guardians', '').strip()
                        if guardians_str:
                            guardians_list = [g.strip() for g in guardians_str.split(',')]
                            for guardian in guardians_list:
                                if guardian.lower() == guardian_name.strip().lower():
                                    return False  # Duplicate found
                        return True  # Not in list
            return True
        except Exception as e:
            print(f"Error checking duplicate guardian: {e}")
            return True

    def check_guardian_not_self(self, guardian_name):
        return guardian_name.strip().lower() != self.current_user_name.strip().lower()

    def update_guardian_in_csv(self, guardian_name):
        users_csv = "users.csv"
        current_user = self.current_user_name

        try:
            if not os.path.exists(users_csv):
                return False

            rows = []
            with open(users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames

                for row in reader:
                    if row['name'].strip().lower() == current_user.strip().lower():
                        existing = row.get('guardians', '').strip()
                        if existing:
                            row['guardians'] = f"{existing}, {guardian_name.strip()}"
                        else:
                            row['guardians'] = guardian_name.strip()
                    rows.append(row)

            with open(users_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            return True
        except Exception as e:
            print(f"Error updating guardian in CSV: {e}")
            return False

    def submit_new_guardian(self):
        name = (self.guard_name_var.get() or "").strip()
        active = bool(self.guard_active_var.get())

        # Validation 1: Check if name is empty
        if not name:
            messagebox.showwarning(
                "Missing Information",
                "⚠️ Please enter the guardian's full name."
            )
            return

        # Validation 2: Check if trying to add yourself
        if not self.check_guardian_not_self(name):
            messagebox.showerror(
                "Invalid Guardian",
                "You cannot add yourself as a guardian!\n\nPlease enter a different name."
            )
            return

        # Validation 3: Check if guardian exists in system
        if not self.check_guardian_exists_in_system(name):
            messagebox.showerror(
                "User Not Found",
                f"The user '{name}' does not exist in the system.\n\n"
                f"Please make sure they have created an account first."
            )
            return

        # Validation 4: Check if guardian is already added
        if not self.check_guardian_not_duplicate(name):
            messagebox.showwarning(
                "Already Added",
                f"'{name}' is already in your guardians list!\n\n"
                f"You cannot add the same guardian twice."
            )
            return

        # All validations passed so we can add the new guardian
        if self.update_guardian_in_csv(name):
            messagebox.showinfo(
                "Guardian Added",
                f"✅ {name} has been added to your guardians!\n\n"
                f"They can now receive your safety alerts."
            )
            self.navigate_to("guards")
        else:
            messagebox.showerror(
                "Save Error",
                "Failed to save guardian to database.\n\nPlease try again."
            )