import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict, Any
from PIL import Image


class EditTipFrame(ctk.CTkFrame):
    """Edit tip screen: loads row, allows manual edits, only saves on button click."""

    MAX_DESC_LEN = 500

    def __init__(self, parent, app, tip_row: Optional[Dict[str, Any]] = None, tip_id: Optional[int] = None):
        super().__init__(parent)
        self.app = app

        # Resolve tip row: prefer tip_id, else tip_row, else empty
        self.tip_row = {}
        rid = tip_id or (tip_row.get("id") if tip_row else None)
        if rid:
            try:
                fresh = self.app.db.read_tip(rid)
                if fresh:
                    self.tip_row = fresh
                else:
                    self.tip_row = tip_row or {}
            except Exception:
                self.tip_row = tip_row or {}
        else:
            self.tip_row = tip_row or {}

        # ------------------ SIDEBAR ------------------
        self.sidebar = ctk.CTkFrame(self, fg_color="#2E2E2E", width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Keep logo exactly
        try:
            main_logo = ctk.CTkImage(light_image=Image.open("assets/main_logo.png"), size=(60, 60))
            ctk.CTkLabel(self.sidebar, image=main_logo, text="",
                         width=60, height=60, corner_radius=0, fg_color="#2B2B2B").pack(pady=(25, 10))
        except Exception:
            ctk.CTkLabel(self.sidebar, text="TS", font=("Helvetica", 42, "bold"),
                         text_color="white").pack(pady=(25, 10))

        ctk.CTkLabel(self.sidebar, text="Dashboard",
                     font=("Helvetica", 28, "bold"), text_color="white").pack(pady=(0, 30))

        self.home_btn = ctk.CTkButton(
            self.sidebar, text="Home", font=("Helvetica", 24, "bold"),
            fg_color="#E0E0E0", text_color="black",
            hover_color="#C9C9C9", corner_radius=0,
            width=180, height=45,
            command=lambda: self.app.show_frame("DashboardFrame")
        )
        self.home_btn.pack(pady=10)

        self.submit_btn = ctk.CTkButton(
            self.sidebar, text="Submit", font=("Helvetica", 24, "bold"),
            fg_color="#E0E0E0", text_color="black",
            hover_color="#C9C9C9", corner_radius=0,
            width=180, height=45,
            command=lambda: self.app.show_frame("AdminSubmitTipFrame")
        )
        self.submit_btn.pack(pady=10)

        self.manage_btn = ctk.CTkButton(
            self.sidebar, text="Manage Incidents", font=("Helvetica", 24, "bold"),
            fg_color="#E0E0E0", text_color="black",
            hover_color="#C9C9C9", corner_radius=0,
            width=180, height=45,
            command=lambda: self.app.show_frame("ManageTipsFrame")
        )
        self.manage_btn.pack(pady=10)

        self.signout_btn = ctk.CTkButton(
            self.sidebar, text="Sign out", font=("Helvetica", 18, "bold"),
            fg_color="#E0E0E0", text_color="black",
            hover_color="#C9C9C9", width=100, height=32,
            corner_radius=0, command=self.logout
        )
        self.signout_btn.pack(side="bottom", pady=20)

        # ------------------ MAIN CONTENT ------------------
        main = ctk.CTkFrame(self, fg_color="#BEBEBE")
        main.pack(side="left", expand=True, fill="both")

        header = ctk.CTkFrame(
            main,
            fg_color="#D9D9D9",
            width=200, height=60,
            corner_radius=0
        )
        header.pack(anchor="center", side="top", pady=(125, 20))

        ctk.CTkLabel(
            header,
            text="Enter Your Anonymous Tip Confidentially",
            font=("HelveticaNeue Heavy", 55),
            text_color="#3E3E3E"
        ).pack(pady=10)

        # ------------------ FORM ------------------
        self._build_form(main)

    # ------------------ UI BUILDERS ------------------
    def _build_form(self, parent):
        form_container = ctk.CTkFrame(
            parent,
            fg_color="#E8E8E8",
            width=1166, height=760,
            corner_radius=0
        )
        form_container.pack(pady=0)

        bordered = ctk.CTkFrame(
            form_container,
            fg_color="#565656",
            border_width=3,
            border_color="#1296FF",
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

        # Top row: Tip Name + Incident Type
        self.tip_name = ctk.CTkEntry(
            inner,
            width=480, height=44,
            font=("Helvetica", 16),
            fg_color="#D9D9D9",
            text_color="black",
            placeholder_text_color="#7B7B7B",
            border_width=0,
            placeholder_text="Enter Tip Name"
        )
        self.tip_name.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="we")
        self.tip_name.insert(0, self.tip_row.get("tip_name", ""))

        self.incident_type = ctk.CTkEntry(
            inner,
            width=480, height=44,
            font=("Helvetica", 16),
            fg_color="#D9D9D9",
            text_color="black",
            placeholder_text_color="#7B7B7B",
            border_width=0,
            placeholder_text="Enter Incident Type"
        )
        self.incident_type.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="we")
        self.incident_type.insert(0, self.tip_row.get("incident_type", ""))

        # Second row: Location + Urgency (radiobutton group)
        self.location = ctk.CTkEntry(
            inner,
            width=480, height=44,
            font=("Helvetica", 16),
            fg_color="#D9D9D9",
            text_color="black",
            placeholder_text_color="#7B7B7B",
            border_width=0,
            placeholder_text="Enter Location of incident"
        )
        self.location.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="we")
        self.location.insert(0, self.tip_row.get("location", ""))

        urgency_panel = ctk.CTkFrame(inner, fg_color="#D9D9D9", corner_radius=0)
        urgency_panel.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="we")
        urgency_panel.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(urgency_panel, text="URGENCY", font=("HelveticaNeue Heavy", 25), text_color="black",
                     fg_color="transparent").grid(row=0, column=0, columnspan=4, pady=(6, 2))

        self.urgency_var = ctk.StringVar(value=(self.tip_row.get("urgency") or "Medium").title())
        ctk.CTkRadioButton(urgency_panel, text="Low", value="Low", variable=self.urgency_var,
                           fg_color="#3B8ED0", hover_color="#2476B9", font=("Helvetica", 15), text_color="black").grid(row=1, column=0, padx=(100, 8), pady=(4, 10), sticky="w")
        ctk.CTkRadioButton(urgency_panel, text="Medium", value="Medium", variable=self.urgency_var,
                           fg_color="#3B8ED0", hover_color="#2476B9", font=("Helvetica", 15), text_color="black").grid(row=1, column=1, padx=(8, 8), pady=(4, 10), sticky="w")
        ctk.CTkRadioButton(urgency_panel, text="High", value="High", variable=self.urgency_var,
                           fg_color="#3B8ED0", hover_color="#2476B9", font=("Helvetica", 15), text_color="black").grid(row=1, column=2, padx=(8, 50), pady=(4, 10), sticky="w")

        # Third row: Description with counter
        desc_container = ctk.CTkFrame(inner, fg_color="#D9D9D9", corner_radius=0)
        desc_container.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 6), sticky="nsew")
        inner.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            desc_container, text="Describe your tip here", font=("Inter", 20, "italic"),
            text_color="black", fg_color="transparent"
        ).pack(anchor="w", padx=10, pady=(8, 2))

        self.description = ctk.CTkTextbox(desc_container, width=980, height=220, fg_color="#EFEFEF", text_color="black", font=("Helvetica", 15))
        self.description.pack(padx=10, pady=(0, 6), fill="both", expand=True)
        self.description.insert("1.0", self.tip_row.get("description", ""))

        self._desc_count = ctk.CTkLabel(desc_container, text="0/500", text_color="black", fg_color="#EFEFEF")
        self._desc_count.place(relx=0.99, rely=1.0, anchor="se", x=-10, y=-6)

        def _update_desc_count(event=None):
            txt = self.description.get("1.0", "end-1c")
            if len(txt) > 500:
                self.description.delete("1.0+500c", "end-1c")
                txt = self.description.get("1.0", "end-1c")
            self._desc_count.configure(text=f"{len(txt)}/500")

        self.description.bind("<KeyRelease>", _update_desc_count)
        self.description.bind("<FocusIn>", _update_desc_count)
        _update_desc_count()

        # Bottom buttons styled like Submit/Clear, but wired to save/reset
        button_bar = ctk.CTkFrame(form_container, fg_color="transparent", height=96)
        button_bar.pack(side="bottom", fill="x", pady=(4, 10))
        button_bar.pack_propagate(False)

        center_buttons = ctk.CTkFrame(button_bar, fg_color="transparent")
        center_buttons.pack(side="top")

        # Save Changes
        save_wrap = ctk.CTkFrame(center_buttons, fg_color="transparent", width=220, height=60)
        save_wrap.pack(side="left", padx=25)
        save_wrap.pack_propagate(False)

        save_shadow = ctk.CTkLabel(save_wrap, width=200, height=50, fg_color="#9E9E9E", text="")
        save_shadow.place(relx=0.5, rely=1.0, anchor="center", y=6)

        save_btn = ctk.CTkButton(
            save_wrap,
            fg_color="#E0E0E0",
            hover_color="#D3D3D3",
            text_color="black",
            text="Save Changes",
            font=("HelveticaNeue Heavy", 28),
            width=200, height=50,
            corner_radius=0,
            command=self.save_tip  # FIX: was self.submit_tip (missing)
        )
        save_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Resolve & Delete
        resolve_wrap = ctk.CTkFrame(center_buttons, fg_color="transparent", width=220, height=60)
        resolve_wrap.pack(side="left", padx=25)
        resolve_wrap.pack_propagate(False)

        resolve_shadow = ctk.CTkLabel(resolve_wrap, width=200, height=50, fg_color="#3C0202", text="")
        resolve_shadow.place(relx=0.5, rely=1.0, anchor="center", y=6)

        resolve_btn = ctk.CTkButton(
            resolve_wrap,
            fg_color="#FF4B4B",
            hover_color="#FFB2B2",
            text_color="black",
            text="Resolve",
            font=("HelveticaNeue Heavy", 28),
            width=200, height=50,
            corner_radius=0,
            command=self._resolve_and_delete
        )
        resolve_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Back
        back_wrap = ctk.CTkFrame(center_buttons, fg_color="transparent", width=220, height=60)
        back_wrap.pack(side="left", padx=25)
        back_wrap.pack_propagate(False)

        back_shadow = ctk.CTkLabel(back_wrap, width=200, height=50, fg_color="#9E9E9E", text="")
        back_shadow.place(relx=0.5, rely=1.0, anchor="center", y=6)

        back_btn = ctk.CTkButton(
            back_wrap,
            fg_color="#E0E0E0",
            hover_color="#C9C9C9",
            text_color="black",
            text="Back",
            font=("HelveticaNeue Heavy", 28),
            width=200, height=50,
            corner_radius=0,
            command=self._back
        )
        back_btn.place(relx=0.5, rely=0.5, anchor="center") 

    # ================= BACKEND FUNCTIONS =================
    def _resolve_and_delete(self):
        tip_id = self.tip_row.get("id")
        if not tip_id:
            messagebox.showerror("Error", "No tip selected.")
            return

        if not messagebox.askyesno("Confirm", "Resolve this tip and delete it? This cannot be undone."):
            return

        # Try to mark resolved first (non-fatal if it fails)
        try:
            self.app.db.update_tip(tip_id, {"status": "Resolved"})
        except Exception as e:
            # You can show a warning but still attempt deletion
            print("[EditTipFrame] resolve update failed:", e)

        # Then delete
        try:
            ok = self.app.db.delete_tip(tip_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete tip:\n{e}")
            return

        if ok:
            messagebox.showinfo("Done", "Tip marked as Resolved and deleted.")
            self._back()
        else:
            messagebox.showwarning("Not deleted", "Tip could not be deleted.")

    def _back(self):
        try:
            self.app.go_back()
        except Exception:
            # Fallback to manage list if history is empty
            try:
                self.app.show_frame("ManageTipsFrame")
            except Exception:
                pass

    def _limit_description(self, event=None):
        txt = self.description.get("1.0", "end-1c")
        if len(txt) > self.MAX_DESC_LEN:
            self.description.delete("1.0", "end")
            self.description.insert("1.0", txt[:self.MAX_DESC_LEN])

    def _collect_updates(self) -> Dict[str, Any]:
        # Collect current field values
        updates = {
            "tip_name": self.tip_name.get().strip(),
            "incident_type": self.incident_type.get().strip(),
            "location": self.location.get().strip(),
            "urgency": self.urgency_var.get().strip(),  # FIX: use radiobutton variable
            "description": self.description.get("1.0", "end-1c").strip(),
        }
        if len(updates["description"]) > self.MAX_DESC_LEN:
            updates["description"] = updates["description"][:self.MAX_DESC_LEN]
        return updates

    def _clear(self):
        """Reset fields to the originally loaded values (not blank)."""
        self.tip_name.delete(0, "end")
        self.tip_name.insert(0, self.tip_row.get("tip_name", ""))

        self.incident_type.delete(0, "end")
        self.incident_type.insert(0, self.tip_row.get("incident_type", ""))

        self.location.delete(0, "end")
        self.location.insert(0, self.tip_row.get("location", ""))

        self.urgency_var.set((self.tip_row.get("urgency") or "Medium").title())

        self.description.delete("1.0", "end")
        desc = (self.tip_row.get("description") or "")[:self.MAX_DESC_LEN]
        self.description.insert("1.0", desc)

        # update counter
        if hasattr(self, "_desc_count"):
            self._desc_count.configure(text=f"{len(desc)}/500")

    def save_tip(self):
        tip_id = self.tip_row.get("id")
        if not tip_id:
            messagebox.showerror("Error", "No tip selected to edit.")
            return

        updates = self._collect_updates()
        # Minimal validation
        missing = [k for k in ("tip_name", "incident_type", "location") if not updates[k]]
        if missing:
            messagebox.showerror("Error", "Missing required fields: " + ", ".join(missing))
            return

        try:
            ok = self.app.db.update_tip(tip_id, updates)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes:\n{e}")
            return

        if ok:
            messagebox.showinfo("Saved", "Changes updated.")
            try:
                self.app.go_back()
            except Exception:
                pass
        else:
            messagebox.showwarning("No changes", "Nothing was updated.")

    def mark_resolved(self):
        tip_id = self.tip_row.get("id")
        if not tip_id:
            messagebox.showerror("Error", "No tip selected to update.")
            return
        if not messagebox.askyesno("Confirm", "Mark this tip as Resolved?"):
            return
        try:
            ok = self.app.db.update_tip(tip_id, {"status": "Resolved"})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status:\n{e}")
            return
        if ok:
            messagebox.showinfo("Status Updated", "Marked as Resolved.")

    def logout(self):
        self.app.current_user = None
        self.app.show_frame("LoginFrame")