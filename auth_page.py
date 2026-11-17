import tkinter as tk
from tkinter import messagebox
import csv
import os

class AuthPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.users_csv = "users.csv"

        self.bg_gradient_start = "#0d0f2a"
        self.bg_gradient_mid = "#16203e"
        self.card_dark = "#0d0f2a"
        self.card_elevated = "#3d4876"
        self.accent_cyan = "#DAA520"
        self.accent_green = "#00f5a0"
        self.accent_pink = "#ff2e63"
        self.text_bright = "#ffffff"
        self.text_dim = "#b8c5d6"
        self.text_muted = "#7c8db0"

        self.root.title("SAFE ROUTE - Login")
        self.width = 620
        self.height = 900
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.bg_gradient_mid)

        self.init_csv()

        self.show_login_page()
    
    def init_csv(self):
        if not os.path.exists(self.users_csv):
            with open(self.users_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'email', 'name', 'password', 'guardians'])
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def get_next_user_id(self):
        try:
            if not os.path.exists(self.users_csv):
                return 1
            
            with open(self.users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if not rows:
                    return 1
                # Get the highest ID and add 1
                max_id = max(int(row['id']) for row in rows if row['id'].isdigit())
                max_id += 1
                return max_id
        except Exception as e:
            print(f"Error getting next ID: {e}")
            return 1
    
    def email_exists(self, email):
        try:
            if not os.path.exists(self.users_csv):
                return False
            
            with open(self.users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['email'].strip().lower() == email.strip().lower():
                        return True
            return False
        except Exception as e:
            print(f"Error checking email: {e}")
            return False
    
    def name_exists(self, name):
        try:
            if not os.path.exists(self.users_csv):
                return False
            
            with open(self.users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['name'].strip().lower() == name.strip().lower():
                        return True
            return False
        except Exception as e:
            print(f"Error checking name: {e}")
            return False
    
    def validate_credentials(self, email, password):
        try:
            if not os.path.exists(self.users_csv):
                return None
            
            with open(self.users_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['email'].strip().lower() == email.strip().lower():
                        if row['password'] == password:
                            return row
                        else:
                            return None  # Password mismatch
            return None  # Email not found
        except Exception as e:
            print(f"Error validating credentials: {e}")
            return None
    
    def add_user(self, email, name, password="", guardians=""):
        try:
            user_id = self.get_next_user_id()
            
            with open(self.users_csv, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([user_id, email.strip(), name.strip(), password, guardians])
            
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def show_login_page(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg=self.bg_gradient_mid)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Frame(main_frame, bg=self.bg_gradient_mid, height=100).pack()

        title_frame = tk.Frame(main_frame, bg=self.bg_gradient_mid)
        title_frame.pack(pady=30)
        
        tk.Label(
            title_frame, text="SAFE ROUTE", font=("Arial", 32, "bold"),
            bg=self.bg_gradient_mid, fg=self.text_bright
        ).pack(pady=(10, 5))

        card_shadow = tk.Frame(main_frame, bg="#000000")
        card_shadow.pack(padx=40, pady=40)
        
        card = tk.Frame(card_shadow, bg=self.card_dark)
        card.pack(padx=2, pady=2)
        
        content = tk.Frame(card, bg=self.card_dark)
        content.pack(padx=40, pady=40)
        
        tk.Label(
            content, text="Welcome Back", font=("Arial", 24, "bold"),
            bg=self.card_dark, fg=self.text_bright
        ).pack(pady=(0, 30))

        tk.Label(
            content, text="Email", font=("Arial", 12, "bold"),
            bg=self.card_dark, fg=self.text_dim, anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        email_entry = tk.Entry(
            content, font=("Arial", 14), bg=self.card_elevated,
            fg=self.text_bright, insertbackground=self.text_bright,
            relief=tk.FLAT, bd=0
        )
        email_entry.pack(fill=tk.X, ipady=12, pady=(0, 20))
        email_entry.focus()

        tk.Label(
            content, text="Password", font=("Arial", 12, "bold"),
            bg=self.card_dark, fg=self.text_dim, anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        password_entry = tk.Entry(
            content, font=("Arial", 14), bg=self.card_elevated,
            fg=self.text_bright, insertbackground=self.text_bright,
            relief=tk.FLAT, bd=0, show="•"
        )
        password_entry.pack(fill=tk.X, ipady=12, pady=(0, 30))

        def on_login():
            email = email_entry.get().strip()
            password = password_entry.get()
            
            if not email or not password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            user_data = self.validate_credentials(email, password)
            
            if user_data:
                messagebox.showinfo("Success", f"Welcome back, {user_data['name']}!")
                self.on_login_success(user_data)
            else:
                messagebox.showerror("Error", "Invalid email or password")
        
        login_btn = tk.Button(
            content, text="Login", font=("Arial", 14, "bold"),
            bg=self.accent_cyan, fg="white", activebackground=self.accent_green,
            activeforeground="white", bd=0, cursor="hand2", relief=tk.FLAT,
            command=on_login
        )
        login_btn.pack(fill=tk.X, ipady=15)

        email_entry.bind('<Return>', lambda e: password_entry.focus())
        password_entry.bind('<Return>', lambda e: on_login())

        signup_frame = tk.Frame(content, bg=self.card_dark)
        signup_frame.pack(pady=(20, 0))
        
        tk.Label(
            signup_frame, text="Don't have an account? ",
            font=("Arial", 11), bg=self.card_dark, fg=self.text_dim
        ).pack(side=tk.LEFT)
        
        signup_link = tk.Label(
            signup_frame, text="Sign Up", font=("Arial", 11, "bold"),
            bg=self.card_dark, fg=self.accent_cyan, cursor="hand2"
        )
        signup_link.pack(side=tk.LEFT)
        signup_link.bind("<Button-1>", lambda e: self.show_signup_page())

        def on_enter(e):
            signup_link.config(fg=self.accent_green)
        
        def on_leave(e):
            signup_link.config(fg=self.accent_cyan)
        
        signup_link.bind("<Enter>", on_enter)
        signup_link.bind("<Leave>", on_leave)
    
    def show_signup_page(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg=self.bg_gradient_mid)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg=self.bg_gradient_mid, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_gradient_mid)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW, width=self.width)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        tk.Frame(scrollable_frame, bg=self.bg_gradient_mid, height=50).pack()

        title_frame = tk.Frame(scrollable_frame, bg=self.bg_gradient_mid)
        title_frame.pack(pady=20)
        
        tk.Label(
            title_frame, text="Create Account", font=("Arial", 28, "bold"),
            bg=self.bg_gradient_mid, fg=self.text_bright
        ).pack(pady=(10, 5))

        card_shadow = tk.Frame(scrollable_frame, bg="#000000")
        card_shadow.pack(padx=40, pady=30)
        
        card = tk.Frame(card_shadow, bg=self.card_dark)
        card.pack(padx=2, pady=2)
        
        content = tk.Frame(card, bg=self.card_dark)
        content.pack(padx=40, pady=40)

        tk.Label(
            content, text="Full Name", font=("Arial", 12, "bold"),
            bg=self.card_dark, fg=self.text_dim, anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        name_entry = tk.Entry(
            content, font=("Arial", 14), bg=self.card_elevated,
            fg=self.text_bright, insertbackground=self.text_bright,
            relief=tk.FLAT, bd=0
        )
        name_entry.pack(fill=tk.X, ipady=12, pady=(0, 20))
        name_entry.focus()

        tk.Label(
            content, text="Email", font=("Arial", 12, "bold"),
            bg=self.card_dark, fg=self.text_dim, anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        email_entry = tk.Entry(
            content, font=("Arial", 14), bg=self.card_elevated,
            fg=self.text_bright, insertbackground=self.text_bright,
            relief=tk.FLAT, bd=0
        )
        email_entry.pack(fill=tk.X, ipady=12, pady=(0, 20))

        tk.Label(
            content, text="Password", font=("Arial", 12, "bold"),
            bg=self.card_dark, fg=self.text_dim, anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        password_entry = tk.Entry(
            content, font=("Arial", 14), bg=self.card_elevated,
            fg=self.text_bright, insertbackground=self.text_bright,
            relief=tk.FLAT, bd=0, show="•"
        )
        password_entry.pack(fill=tk.X, ipady=12, pady=(0, 5))

        def on_signup():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()

            if not name or not email:
                messagebox.showerror("Error", "Please enter both name and email")
                return

            if not password:
                messagebox.showerror("Error", "Please enter password")
                return
            
            if '@' not in email or '.' not in email:
                messagebox.showerror("Error", "Please enter a valid email address")
                return
            
            if self.email_exists(email):
                messagebox.showerror("Error", "This email is already registered")
                return
            
            if self.name_exists(name):
                messagebox.showerror("Error", "This name is already taken. Please choose another name")
                return

            if self.add_user(email, name, password):
                messagebox.showinfo(
                    "Success",
                    f"Account created successfully!\nWelcome, {name}!"
                )
                user_data = {
                    'id': self.get_next_user_id() - 1,
                    'email': email,
                    'name': name,
                    'password': password,
                    'guardians': ''
                }
                self.on_login_success(user_data)
            else:
                messagebox.showerror("Error", "Failed to create account. Please try again.")
        
        signup_btn = tk.Button(
            content, text="Create Account", font=("Arial", 14, "bold"),
            bg=self.accent_cyan, fg="white", activebackground=self.accent_green,
            activeforeground="white", bd=0, cursor="hand2", relief=tk.FLAT,
            command=on_signup
        )
        signup_btn.pack(fill=tk.X, ipady=15)

        login_frame = tk.Frame(content, bg=self.card_dark)
        login_frame.pack(pady=(20, 0))
        
        tk.Label(
            login_frame, text="Already have an account? ",
            font=("Arial", 11), bg=self.card_dark, fg=self.text_dim
        ).pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame, text="Login", font=("Arial", 11, "bold"),
            bg=self.card_dark, fg=self.accent_cyan, cursor="hand2"
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind("<Button-1>", lambda e: self.show_login_page())

        def on_enter(e):
            login_link.config(fg=self.accent_green)
        
        def on_leave(e):
            login_link.config(fg=self.accent_cyan)
        
        login_link.bind("<Enter>", on_enter)
        login_link.bind("<Leave>", on_leave)

        tk.Frame(scrollable_frame, bg=self.bg_gradient_mid, height=50).pack()

if __name__ == "__main__":
    def on_success(user_data):
        print(f"Login successful! User: {user_data}")
        root.quit()
    
    root = tk.Tk()
    auth = AuthPage(root, on_success)
    root.mainloop()
