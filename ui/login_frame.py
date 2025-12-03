import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

from models.user import Admin, Reporter, Viewer


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # =========================================================
        # BACKGROUND IMAGE
        # =========================================================
        bg_path = "assets/bg_login.png"   # <-- change this to your file
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

        # Title
        label = ctk.CTkLabel(
        self,
        text="TattleStoolie",
        font=("HelveticaNeue Heavy", 70),
        text_color="#E0E0E0",
        bg_color="#2B2B2B",
        )
        label.place(relx=0.5, rely=0.33, anchor="center")
        label.configure(width=500, height=75)

        # Inner white panel for inputs
        inputs = ctk.CTkFrame(login_box, fg_color="#565656", corner_radius=1)
        inputs.pack(pady=15, padx=10)
        inputs.configure(width=565,height=165)
        inputs.pack_propagate(False)

        # ICONS
        user_icon_img = ctk.CTkImage(light_image=Image.open("assets/user_icon.png"), size=(25, 25))
        password_icon_img = ctk.CTkImage(light_image=Image.open("assets/password_icon.png"), size=(25, 25))

        # Username box
        box_user = ctk.CTkFrame(inputs, fg_color="#565656", corner_radius=1)
        box_user.pack(padx=10, pady=(25, 5), anchor="center")
        box_user.pack_propagate(False)
        box_user.configure(width=515, height=50)

        user_icon_label = ctk.CTkLabel(
            box_user,
            image=user_icon_img,
            text="",
            fg_color="#D9D9D9",
            corner_radius=1,
            width=50, height=50
        )
        user_icon_label.place(relx=0.010, rely=0.5, anchor="w")

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


        # Password box
        box_pass = ctk.CTkFrame(inputs, fg_color="#565656", corner_radius=1)
        box_pass.pack(padx=10, pady=(5, 25), anchor="center")
        box_pass.pack_propagate(False)
        box_pass.configure(width=515, height=50)

        password_icon_label = ctk.CTkLabel(
            box_pass,
            image=password_icon_img,
            text="",
            fg_color="#D9D9D9",
            corner_radius=1,
            width=50, height=50
        )
        password_icon_label.place(relx=0.010, rely=0.5, anchor="w")

        self.password = ctk.CTkEntry(
            box_pass,
            font=("Helvetica", 25),
            placeholder_text="Password",
            show="*",
            fg_color="#D9D9D9",
            text_color="black",
            border_width=0,
            corner_radius=1,
            width=465, height=50       # Leave some space for icon
        )
        self.password.place(relx=0.10, rely=0.5, anchor="w")

        shadow_offset_y = 8

        # --- Frame to contain prompt and button ---
        register_prompt_frame = ctk.CTkFrame(
            login_box,
            fg_color="transparent",  # doesn't show, just for layout
            width=270,
            height=40
        )
        register_prompt_frame.place(relx=0.95, rely=0.95, anchor="se")

        # --- "Don't have an account?" label ---
        prompt_label = ctk.CTkLabel(
            register_prompt_frame,
            text="Don't have an account?",
            font=("Helvetica", 20),
            text_color="#E0E0E0",
            fg_color="transparent"
        )
        prompt_label.pack(side="left", padx=(10, 5))

        # --- "Register now" clickable button ---
        register_btn = ctk.CTkButton(
            register_prompt_frame,
            text="Register now",
            font=("Helvetica", 20),  # underline makes it look like a link
            fg_color="#515151",
            text_color="#5DADE2",   # light blue for action
            hover_color="#A8A8A8",
            width=120, height=36,
            corner_radius=6,
            command=lambda: app.show_frame("RegisterFrame")
        )
        register_btn.pack(side="left", padx=(5, 5))

        # =========================================================
        # ENTER BUTTON (big, centered below)
        # =========================================================

        shadow_offset_y = 8

        ctk.CTkFrame(
            self,
            fg_color="#565656",
            width=250,
            height=60,
            corner_radius=1
        ).place(relx=0.5, rely=0.70, anchor="center", y=shadow_offset_y)

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
        u = self.username.get().strip()
        p = self.password.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Enter credentials.")
            return

        row = self.app.db.get_user_by_credentials(u, p)
        if not row:
            messagebox.showerror("Error", "Invalid username/password.")
            return

        # Create user object
        role = row.get('role', 'reporter').lower()
        if role == 'admin':
            user = Admin(row)
        elif role == 'viewer':
            user = Viewer(row)
        else:
            user = Reporter(row)

        self.app.current_user = user

        # Navigation
        if user.is_admin():
            self.app.show_frame("DashboardFrame")
        else:
            self.app.show_frame("SubmitTipFrame")
