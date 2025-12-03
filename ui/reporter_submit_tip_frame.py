import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


class SubmitTipFrame(ctk.CTkFrame):
    """
    Reporter/Viewer submit tip frame (non-admin).
    Title and Exit button are left exactly as-is.
    """
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#BEBEBE")

        # Top bar
        top_bar = ctk.CTkFrame(self, fg_color="#2b2b2b", height=50, corner_radius=0)
        top_bar.pack(fill="x", side="top")

        # Top Bar Logo and Title
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

        # ------------------ TITLE (LEAVE ALONE) ------------------
        ctk.CTkLabel(
            self,
            text="Enter Your Anonymous Tip Confidentially",
            text_color="black",
            font=("HelveticaNeue Heavy", 50),
            fg_color="#D9D9D9",
            width=1085, height=110
        ).pack(pady=15)

        # ------------------ FORM ------------------
        self._build_form(self)

    # ------------------ UI BUILDERS ------------------
    def _build_form(self, parent):
        # Outer white card matching the mock (fixed size to match layout)
        form_container = ctk.CTkFrame(
            parent,
            fg_color="#E8E8E8",
            width=1166, height=760,  # slightly taller to reserve room for shadows/buttons
            corner_radius=0
        )
        form_container.pack(pady=25)
        form_container.pack_propagate(False)

        # Inner bordered panel (blue border) + dark content area
        bordered = ctk.CTkFrame(
            form_container,
            fg_color="#565656",
            border_width=3,
            border_color="#1296FF",  # blue accent like mock
            corner_radius=0,
            width=1085, height=560
        )
        bordered.pack(padx=24, pady=(24, 12))
        bordered.pack_propagate(False)

        inner = ctk.CTkFrame(bordered, fg_color="#4F4F4F", corner_radius=0)
        inner.pack(fill="both", expand=True, padx=18, pady=18)

        # Two columns inside the dark panel
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=1)

        # ------------------------------------------------------------------
        # Top row: Tip Name (left) + Incident Type (right)
        # Light gray boxes with placeholder text to match the mock
        # ------------------------------------------------------------------
        name_box = ctk.CTkEntry(
            inner,
            width=480, height=44,
            font=("Helvetica", 16),
            fg_color="#D9D9D9",
            text_color="black",
            placeholder_text_color="#7B7B7B",
            border_width=0,
            placeholder_text="Enter Tip Name"
        )
        name_box.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="we")
        self.tip_name = name_box

        incident_box = ctk.CTkEntry(
            inner,
            width=480, height=44,
            font=("Helvetica", 16),
            fg_color="#D9D9D9",
            text_color="black",
            placeholder_text_color="#7B7B7B",
            border_width=0,
            placeholder_text="Enter Incident Type"
        )
        incident_box.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="we")
        self.incident_type = incident_box

        # ------------------------------------------------------------------
        # Second row: Location (left) + Urgency selector (right)
        # ------------------------------------------------------------------
        location_box = ctk.CTkEntry(
            inner,
            width=480, height=44,
            font=("Helvetica", 16),
            fg_color="#D9D9D9",
            text_color="black",
            placeholder_text_color="#7B7B7B",
            border_width=0,
            placeholder_text="Enter Location of incident"
        )
        location_box.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="we")
        self.location = location_box

        # Urgency panel (light box with label + three radio options)
        urgency_panel = ctk.CTkFrame(inner, fg_color="#D9D9D9", corner_radius=0)
        urgency_panel.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="we")
        urgency_panel.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(urgency_panel, text="URGENCY", font=("HelveticaNeue Heavy", 25), text_color="black",
                     fg_color="transparent").grid(row=0, column=0, columnspan=4, pady=(6, 2))

        self.urgency_var = ctk.StringVar(value="Medium")
        low_rb = ctk.CTkRadioButton(urgency_panel, text="Low", value="Low", variable=self.urgency_var,
                                    fg_color="#3B8ED0", hover_color="#2476B9", font=("Helvetica", 15), text_color="black")
        med_rb = ctk.CTkRadioButton(urgency_panel, text="Medium", value="Medium", variable=self.urgency_var,
                                    fg_color="#3B8ED0", hover_color="#2476B9", font=("Helvetica", 15), text_color="black")
        high_rb = ctk.CTkRadioButton(urgency_panel, text="High", value="High", variable=self.urgency_var,
                                    fg_color="#3B8ED0", hover_color="#2476B9", font=("Helvetica", 15), text_color="black")

        low_rb.grid(row=1, column=0, padx=(100, 8), pady=(4, 10), sticky="w")
        med_rb.grid(row=1, column=1, padx=(8, 8), pady=(4, 10), sticky="w")
        high_rb.grid(row=1, column=2, padx=(8, 50), pady=(4, 10), sticky="w")

        # ------------------------------------------------------------------
        # Third row: Description spanning both columns with count bottom-right
        # ------------------------------------------------------------------
        desc_container = ctk.CTkFrame(inner, fg_color="#D9D9D9", corner_radius=0)
        desc_container.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 6), sticky="nsew")
        inner.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            desc_container, text="Describe your tip here", font=("Inter", 20, "italic"),
            text_color="black", fg_color="transparent"
        ).pack(anchor="w", padx=10, pady=(8, 2))

        self.description = ctk.CTkTextbox(desc_container, width=980, height=220, fg_color="#EFEFEF", text_color="black", font=("Helvetica", 15))
        self.description.pack(padx=10, pady=(0, 6), fill="both", expand=True)

        # Character counter bottom-right (0/500)
        self._desc_count = ctk.CTkLabel(desc_container, text="0/500", text_color="black", fg_color="#EFEFEF")
        self._desc_count.place(relx=0.99, rely=1.0, anchor="se", x=-10, y=-6)

        def _update_desc_count(event=None):
            txt = self.description.get("1.0", "end-1c")
            if len(txt) > 500:
                # Trim to 500 without breaking cursor excessively
                self.description.delete("1.0+500c", "end-1c")
                txt = self.description.get("1.0", "end-1c")
            self._desc_count.configure(text=f"{len(txt)}/500")

        self.description.bind("<KeyRelease>", _update_desc_count)
        self.description.bind("<FocusIn>", _update_desc_count)
        _update_desc_count()

        # ------------------ Submit/Clear buttons (centered at bottom of white card) ------------------
        # Dedicated bottom area so shadows never get clipped
        button_bar = ctk.CTkFrame(form_container, fg_color="transparent", height=96)
        button_bar.pack(side="bottom", fill="x", pady=(4, 10))
        button_bar.pack_propagate(False)

        center_buttons = ctk.CTkFrame(button_bar, fg_color="transparent")
        center_buttons.pack(side="top")

        # Submit (with shallow drop shadow)
        submit_wrap = ctk.CTkFrame(center_buttons, fg_color="transparent", width=220, height=60)
        submit_wrap.pack(side="left", padx=25)
        submit_wrap.pack_propagate(False)

        submit_shadow = ctk.CTkLabel(submit_wrap, width=200, height=50, fg_color="#9E9E9E", text="")
        submit_shadow.place(relx=0.5, rely=1.0, anchor="center", y=6)

        submit_btn = ctk.CTkButton(
            submit_wrap,
            fg_color="#E0E0E0",
            hover_color="#D3D3D3",
            text_color="black",
            text="Submit",
            font=("HelveticaNeue Heavy", 28),
            width=200, height=50,
            corner_radius=0,
            command=self.submit_tip
        )
        submit_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Clear (with shallow drop shadow)
        clear_wrap = ctk.CTkFrame(center_buttons, fg_color="transparent", width=220, height=60)
        clear_wrap.pack(side="left", padx=25)
        clear_wrap.pack_propagate(False)

        clear_shadow = ctk.CTkLabel(clear_wrap, width=200, height=50, fg_color="#9E9E9E", text="")
        clear_shadow.place(relx=0.5, rely=1.0, anchor="center", y=6)

        clear_btn = ctk.CTkButton(
            clear_wrap,
            fg_color="#E0E0E0",
            hover_color="#C9C9C9",
            text_color="black",
            text="Clear",
            font=("HelveticaNeue Heavy", 28),
            width=200, height=50,
            corner_radius=0,
            command=self._clear
        )
        clear_btn.place(relx=0.5, rely=0.5, anchor="center")

        # ------------------ EXIT ------------------
        shadow_exit = ctk.CTkLabel(
            self,
            width=200,
            height=50,
            fg_color="#515151",   # unchanged
            text="",
            corner_radius=0
        )
        shadow_exit.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)

        exit_btn = ctk.CTkButton(
            self,
            text="Exit",
            font=("HelveticaNeue Heavy", 45),
            width=200, height=50,
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#C9C9C9",
            corner_radius=0,
            command=self._exit
        )
        exit_btn.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    # ------------------ HELPERS ------------------
    def _collect_payload(self):
        desc = self.description.get("1.0", "end-1c").strip()
        payload = {
            "tip_name": self.tip_name.get().strip(),
            "incident_type": self.incident_type.get().strip(),
            "location": self.location.get().strip(),
            "urgency": self.urgency_var.get(),  # use radio selection
            "description": desc,
        }
        user = getattr(self.app, "current_user", None)
        if user:
            payload["submitted_by"] = getattr(user, "username", None)
            payload["role"] = getattr(user, "role", None)
        return payload

    def _validate(self, payload):
        if not payload["tip_name"]:
            messagebox.showerror("Error", "Tip Name is required.")
            return False
        if not payload["incident_type"]:
            messagebox.showerror("Error", "Incident Type is required.")
            return False
        if not payload["location"]:
            messagebox.showerror("Error", "Location is required.")
            return False
        if not payload["description"]:
            messagebox.showerror("Error", "Description is required.")
            return False
        if payload["urgency"] not in {"Low", "Medium", "High"}:
            messagebox.showerror("Error", "Urgency must be Low, Medium, or High.")
            return False
        return True

    def _save_tip(self, payload):
        db = getattr(self.app, "db", None)
        if not db:
            return False, None
        for m in ("create_tip", "add_tip", "insert_tip", "save_tip"):
            fn = getattr(db, m, None)
            if callable(fn):
                try:
                    result = fn(payload)
                    if result is True or result is None:
                        return True, None
                    if isinstance(result, dict) and ("id" in result or "tip_id" in result):
                        return True, result.get("id", result.get("tip_id"))
                    return True, result
                except Exception as e:
                    print(f"[Reporter SubmitTip] Save via {m} failed:", e)
                    return False, None
        return False, None

    def _clear(self):
        self.tip_name.delete(0, "end")
        self.incident_type.delete(0, "end")
        self.location.delete(0, "end")
        self.description.delete("1.0", "end")
        self.urgency_var.set("Medium")
        # update counter
        if hasattr(self, "_desc_count"):
            self._desc_count.configure(text="0/500")

    # ------------------ ACTIONS ------------------
    def _exit(self):
        # LEAVE ALONE (unchanged behavior)
        if hasattr(self.app, "show_frame"):
            try:
                self.app.show_frame("ReporterExitFrame")
                return
            except Exception:
                pass
        self._clear()
        messagebox.showinfo("Info", "You can close the window.")

    def submit_tip(self):
        payload = self._collect_payload()
        if not self._validate(payload):
            return
        ok, tip_id = self._save_tip(payload)
        if not ok:
            messagebox.showerror("Error", "There was a problem submitting your tip.")
            return
        msg = f"Your anonymous tip has been submitted."
        if tip_id is not None:
            msg += f" Thank you."
        messagebox.showinfo("Success", msg)
        self._clear()