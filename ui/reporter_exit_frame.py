import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# Module: reporter_exit_frame.py
# Purpose: Show a confirmation / exit screen after submission.
# Renders a centered message about confidentiality and two action buttons:
# Exit (sign out / back to login) and Return (go back to previous screen).
# Comments describe layout and button behaviors.

class ReporterExitFrame(ctk.CTkFrame):
    """Exit confirmation screen styled to match the reference image."""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Background color chosen to match the app theme
        self.configure(fg_color="#B3B3B3")

        # Top bar (unchanged scaffold) containing the logo and app name.
        top_bar = ctk.CTkFrame(self, fg_color="#2b2b2b", height=50, corner_radius=0)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        # Top bar logo image (small) and app title on the right
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

        # --- CENTER CONTENT ---
        # Center frame holds the confirmation message and buttons.
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        msg = (
            "By accepting, you acknowledge that your confidentiality is fully protected.\n"
            "Are you sure you want to exit?"
        )

        # Message label with wrap and centered justification
        ctk.CTkLabel(
            center,
            text=msg,
            wraplength=650,
            justify="center",
            font=("Inter", 18, "italic", "bold"),
            text_color="#2b2b2b"
        ).pack(padx=20, pady=(0, 30))

        # --- BUTTON ROW ---
        # Row container for Exit and Return buttons; uses absolute placement for button shadows.
        btn_row = ctk.CTkFrame(center, fg_color="transparent")
        btn_row.pack(pady=5)
        btn_row.configure(width=330, height=60)
        btn_row.pack_propagate(False)


        # ======================================================
        # EXIT BUTTON + SHADOW  (pattern matched to your sample)
        # ======================================================
        # The shadow label is placed slightly offset to create a drop-shadow effect.
        shadow_exit = ctk.CTkLabel(
            btn_row,
            width=130,
            height=36,
            fg_color="#515151",
            text="",
            corner_radius=0
        )
        shadow_exit.place(x=15, y=10 + 3)

        # Exit button triggers sign-out (confirmation prompt)
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
        # Return button cancels exit and returns to the previous frame.
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
        # When the user confirms, call the app.logout method to clear session and go to login.
        if messagebox.askyesno("Confirm Exit", "Sign out and return to login?"):
            self.app.logout()