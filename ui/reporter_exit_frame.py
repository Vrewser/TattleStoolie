import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

class ReporterExitFrame(ctk.CTkFrame):
    """Exit confirmation screen styled to match the reference image."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Background color similar to screenshot
        self.configure(fg_color="#B3B3B3")

        # Top bar (unchanged scaffold)
        top_bar = ctk.CTkFrame(self, fg_color="#2b2b2b", height=50, corner_radius=0)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        # Top bar Logo and text
        main_logo = ctk.CTkImage(light_image=Image.open("assets/main_logo.png"), size=(35, 35))

        main_logo = ctk.CTkLabel(
            top_bar,
            image=main_logo,
            text="",
            fg_color="#2B2B2B",
            corner_radius=1,
            width=50, height=50
        )
        main_logo.pack(side="right", padx=(0,0))

        logo = ctk.CTkLabel(
            top_bar,
            text="TattleStoolie",
            font=("Helevitica", 25, "italic", "bold"),
            text_color="#d9d9d9"
        )
        logo.pack(side="right", padx=(35,0))

        # --- CENTER CONTENT --------------------------------------------------
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        msg = (
            "By accepting, you acknowledge that your confidentiality is fully protected.\n"
            "Are you sure you want to exit?"
        )

        ctk.CTkLabel(
            center,
            text=msg,
            wraplength=650,
            justify="center",
            font=("Inter", 18, "italic", "bold"),
            text_color="#2b2b2b"
        ).pack(padx=20, pady=(0, 30))

        # --- BUTTON ROW ---
        btn_row = ctk.CTkFrame(center, fg_color="transparent")
        btn_row.pack(pady=5)
        btn_row.configure(width=330, height=60)
        btn_row.pack_propagate(False)


        # ======================================================
        # EXIT BUTTON + SHADOW  (pattern matched to your sample)
        # ======================================================

        shadow_exit = ctk.CTkLabel(
            btn_row,
            width=130,
            height=36,
            fg_color="#515151",
            text="",
            corner_radius=0
        )
        shadow_exit.place(x=15, y=10 + 3)

        exit_btn = ctk.CTkButton(
            btn_row,
            text="Exit",
            font=("Helvetica", 20),
            width=130, height=36,
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#C9C9C9",
            corner_radius=0,
            command=self._exit_confirm
        )
        exit_btn.place(x=15, y=10)


        # ======================================================
        # RETURN BUTTON + SHADOW (same pattern)
        # ======================================================

        shadow_return = ctk.CTkLabel(
            btn_row,
            width=130,
            height=36,
            fg_color="#515151",
            text="",
            corner_radius=0
        )
        shadow_return.place(x=15 + 130 + 30, y=10 + 3)

        return_btn = ctk.CTkButton(
            btn_row,
            text="Return",
            font=("Helvetica", 20),
            width=130, height=36,
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#C9C9C9",
            corner_radius=0,
            command=self.app.go_back
        )
        return_btn.place(x=15 + 130 + 30, y=10)

    # ----------------------------------------------------------------------
    def _exit_confirm(self):
        if messagebox.askyesno("Confirm Exit", "Sign out and return to login?"):
            self.app.logout()

