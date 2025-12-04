import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# Module: register_frame.py
# Purpose: Provide a registration UI for new users.
# Renders a centered registration box with inputs for username, email and password,
# includes basic client-side validation and calls the app.db.create_user method.
# Comments added to clarify layout and validation steps.

class RegisterFrame(ctk.CTkFrame):
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
            # If background asset missing, use a plain background color.
            print("Background image failed to load. Using solid background.")
            self.configure(fg_color="white")

        # =========================================================
        # REGISTER BOX (center)
        # =========================================================
        # Main centered container for the registration form.
        register_box = ctk.CTkFrame(self, fg_color="#2B2B2B")
        register_box.place(relx=0.5, rely=0.5, anchor="center")
        register_box.configure(width=600, height=310)
        register_box.pack_propagate(False)

        # Title at the top, consistent style with LoginFrame
        label = ctk.CTkLabel(
            self,
            text="Register",
            font=("HelveticaNeue Heavy", 70),
            text_color="#E0E0E0",
            bg_color="#2B2B2B",
        )
        label.place(relx=0.5, rely=0.30, anchor="center")
        label.configure(width=350, height=75)

        # =========================================================
        # Inner panel for inputs
        # =========================================================
        inputs = ctk.CTkFrame(register_box, fg_color="#565656", corner_radius=1)
        inputs.pack(pady=15, padx=10)
        inputs.configure(width=565, height=235)
        inputs.pack_propagate(False)

        # Centering inner block for consistent layout
        inputs_inner = ctk.CTkFrame(inputs, fg_color="transparent")
        inputs_inner.place(relx=0.5, rely=0.5, anchor="center")  # centers the rows block

        # ICONS for the input rows
        user_icon_img = ctk.CTkImage(light_image=Image.open("assets/user_icon.png"), size=(30, 30))
        email_icon_img = ctk.CTkImage(light_image=Image.open("assets/email_icon.png"), size=(30, 30))
        password_icon_img = ctk.CTkImage(light_image=Image.open("assets/password_icon.png"), size=(30, 30))

        # Username input row
        box_user = ctk.CTkFrame(inputs_inner, fg_color="#565656", corner_radius=1)
        box_user.pack(padx=10, pady=(6, 6), anchor="center")
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

        # Email input row
        box_email = ctk.CTkFrame(inputs_inner, fg_color="#565656", corner_radius=1)
        box_email.pack(padx=10, pady=(6, 6), anchor="center")
        box_email.pack_propagate(False)
        box_email.configure(width=515, height=50)

        email_icon_label = ctk.CTkLabel(
            box_email,
            image=email_icon_img,
            text="",
            fg_color="#D9D9D9",
            corner_radius=1,
            width=50, height=50
        )
        email_icon_label.place(relx=0.010, rely=0.5, anchor="w")

        self.email = ctk.CTkEntry(
            box_email,
            font=("Helvetica", 25),
            placeholder_text="Email",
            fg_color="#D9D9D9",
            text_color="black",
            border_width=0,
            corner_radius=1,
            width=465, height=50
        )
        self.email.place(relx=0.10, rely=0.5, anchor="w")

        # Password input row
        box_pass = ctk.CTkFrame(inputs_inner, fg_color="#565656", corner_radius=1)
        box_pass.pack(padx=10, pady=(6, 6), anchor="center")
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
            width=465, height=50
        )
        self.password.place(relx=0.10, rely=0.5, anchor="w")

        # =========================================================
        # Prompt + navigation to login
        # =========================================================
        nav_prompt_frame = ctk.CTkFrame(
            register_box,
            fg_color="transparent",
            width=300,
            height=40
        )
        nav_prompt_frame.place(relx=0.95, rely=0.95, anchor="se")

        prompt_label = ctk.CTkLabel(
            nav_prompt_frame,
            text="Already have an account?",
            font=("Helvetica", 20),
            text_color="#E0E0E0",
            fg_color="transparent"
        )
        prompt_label.pack(side="left", padx=(10, 5))

        back_to_login_btn = ctk.CTkButton(
            nav_prompt_frame,
            text="Login",
            font=("Helvetica", 20),
            fg_color="#515151",
            text_color="#5DADE2",
            hover_color="#A8A8A8",
            width=100, height=36,
            corner_radius=6,
            command=lambda: app.show_frame("LoginFrame")
        )
        back_to_login_btn.pack(side="left", padx=(5, 5))

        # =========================================================
        # CREATE ACCOUNT BUTTON
        # =========================================================
        # Visual shadow beneath the primary action button
        shadow_offset_y = 8
        ctk.CTkFrame(
            self,
            fg_color="#565656",
            width=250,
            height=60,
            corner_radius=1
        ).place(relx=0.5, rely=0.70, anchor="center", y=shadow_offset_y)

        # Main Create Account button triggers register()
        ctk.CTkButton(
            self,
            text="Create Account",
            font=("HelveticaNeue Heavy", 34),
            width=260,
            height=60,
            fg_color="#dbdbdb",
            text_color="black",
            hover_color="#c8c8c8",
            corner_radius=1,
            command=self.register
        ).place(relx=0.5, rely=0.70, anchor="center")

    # =============================================================
    # REGISTER LOGIC
    # =============================================================
    def register(self):
        # Basic validation then call DB.create_user
        u = self.username.get().strip()
        e = self.email.get().strip()
        p = self.password.get().strip()

        if not u or not p or not e:
            messagebox.showerror("Error", "All fields required.")
            return

        # Basic email sanity check
        if "@" not in e or "." not in e.split("@")[-1]:
            messagebox.showerror("Error", "Enter a valid email address.")
            return

        ok = self.app.db.create_user(u, e, p)
        if not ok:
            messagebox.showerror("Error", "Username already taken.")
            return

        messagebox.showinfo("Success", "Account created. Please log in.")
        self.app.show_frame("LoginFrame")