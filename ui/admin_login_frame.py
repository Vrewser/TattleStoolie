import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from models.user import Admin


class AdminLoginFrame(ctk.CTkFrame):
    """Admin-only login frame."""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # =========================================================
        # BACKGROUND IMAGE
        # =========================================================
        bg_path = "assets/bg_login.png"
        try:
            bg_img = Image.open(bg_path)
            self.bg = ctk.CTkImage(light_image=bg_img, size=(1920, 1080))
            bg_label = ctk.CTkLabel(self, image=self.bg, text="")
            bg_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            print("Background image failed to load. Using solid background.")
            self.configure(fg_color="white")

        # =========================================================
        # LOGIN BOX (center)
        # =========================================================
        login_box = ctk.CTkFrame(self, fg_color="#2B2B2B")
        login_box.place(relx=0.5, rely=0.5, anchor="center")
        login_box.configure(width=600, height=250)
        login_box.pack_propagate(False)

        # Title text placed above the login box.
        label = ctk.CTkLabel(
            self,
            text="TattleStoolie - Admin",
            font=("HelveticaNeue Heavy", 70),
            text_color="#E0E0E0",
            bg_color="#2B2B2B",
        )
        label.place(relx=0.5, rely=0.33, anchor="center")
        label.configure(width=500, height=75)

        # Inner panel for credentials
        inputs = ctk.CTkFrame(login_box, fg_color="#565656", corner_radius=1)
        inputs.pack(pady=15, padx=10)
        inputs.configure(width=565, height=165)
        inputs.pack_propagate(False)

        # ICONS for username and password
        try:
            user_icon_img = ctk.CTkImage(light_image=Image.open("assets/user_icon.png"), size=(25, 25))
            password_icon_img = ctk.CTkImage(light_image=Image.open("assets/password_icon.png"), size=(25, 25))
        except Exception:
            user_icon_img = None
            password_icon_img = None

        # Username input row with icon
        box_user = ctk.CTkFrame(inputs, fg_color="#565656", corner_radius=1)
        box_user.pack(padx=10, pady=(25, 5), anchor="center")
        box_user.pack_propagate(False)
        box_user.configure(width=515, height=50)

        if user_icon_img:
            user_icon_label = ctk.CTkLabel(
                box_user,
                image=user_icon_img,
                text="",
                fg_color="#D9D9D9",
                corner_radius=1,
                width=50, height=50
            )
            user_icon_label.place(relx=0.010, rely=0.5, anchor="w")

        # Username entry widget
        self.username = ctk.CTkEntry(
            box_user,
            font=("Helvetica", 25),
            placeholder_text="Username",
            fg_color="#D9D9D9",
            text_color="black",
            border_width=0,
            corner_radius=1,
            width=465, height=50
        )
        self.username.place(relx=0.10, rely=0.5, anchor="w")

        # Password input row with icon
        box_pass = ctk.CTkFrame(inputs, fg_color="#565656", corner_radius=1)
        box_pass.pack(padx=10, pady=(5, 25), anchor="center")
        box_pass.pack_propagate(False)
        box_pass.configure(width=515, height=50)

        if password_icon_img:
            password_icon_label = ctk.CTkLabel(
                box_pass,
                image=password_icon_img,
                text="",
                fg_color="#D9D9D9",
                corner_radius=1,
                width=50, height=50
            )
            password_icon_label.place(relx=0.010, rely=0.5, anchor="w")

        # Password entry widget
        self.password = ctk.CTkEntry(
            box_pass,
            font=("Helvetica", 25),
            placeholder_text="Password",
            show="*",
            fg_color="#D9D9D9",
            text_color="black",
            border_width=0,
            corner_radius=1,
            width=465, height=50
        )
        self.password.place(relx=0.10, rely=0.5, anchor="w")

        shadow_offset_y = 8

        # Subtle shadow frame beneath the main Enter button
        ctk.CTkFrame(
            self,
            fg_color="#565656",
            width=250,
            height=60,
            corner_radius=1
        ).place(relx=0.5, rely=0.70, anchor="center", y=shadow_offset_y)

        # Main Enter button that triggers authentication
        ctk.CTkButton(
            self,
            text="Enter",
            font=("HelveticaNeue Heavy", 40),
            width=250,
            height=60,
            fg_color="#dbdbdb",
            text_color="black",
            hover_color="#c8c8c8",
            corner_radius=1,
            command=self.login
        ).place(relx=0.5, rely=0.70, anchor="center")

    # =============================================================
    # LOGIN LOGIC
    # =============================================================
    def login(self):
        """Authenticate admin user."""
        u = self.username.get().strip()
        p = self.password.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Enter credentials.")
            return

        row = self.app.db.get_user_by_credentials(u, p)
        if not row:
            messagebox.showerror("Error", "Invalid username/password.")
            return

        # Verify user is admin
        if row.get('role', '').lower() != 'admin':
            messagebox.showerror("Error", "Admin credentials required.")
            return

        try:
            user = Admin(row)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Store current_user and navigate to admin dashboard
        self.app.current_user = user
        self.app.show_frame("DashboardFrame")
