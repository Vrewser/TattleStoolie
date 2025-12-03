import customtkinter as ctk
from tkinter import messagebox
from typing import List, Dict, Any
from PIL import Image


class ManageTipsFrame(ctk.CTkFrame):

    COLORS = {
        "sidebar_bg": "#1F1F1F",
        "sidebar_btn": "#E0E0E0",
        "sidebar_btn_hover": "#C9C9C9",
        "sidebar_text_dark": "black",
        "sidebar_text_light": "white",

        "main_bg": "#BDBDBD",
        "table_outer_bg": "#BDBDBD",
        "table_border": "#1296FF",
        "header_bg": "#1F1F1F",
        "header_text": "#FFFFFF",
        "subheader_bg": "#1F1F1F",
        "row_bg": "#E8E8E8",
        "row_alt_bg": "#EDEDED",
        "row_text": "#000000",
        "no_rows_text": "#4F4F4F",
        "search_entry_bg": "#2A2A2A",
    }

    # Column weights (first three wider). Last column is the Edit button area.
    COL_WEIGHTS = [2, 2, 2, 1, 1, 0]

    # Uniform cell padding to keep perfect alignment
    CELL_PADX = (12, 8)
    CELL_PADY = (4, 4)

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color=self.COLORS["main_bg"])

        self.sort_key = "tip_name"
        self.sort_ascending = True

        # Header buttons registry for easy label updates
        self._header_buttons: dict[str, tuple[ctk.CTkButton, str]] = {}

        # ------------------ SIDEBAR ------------------
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color="#2E2E2E", width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

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
            self.sidebar, text="Manage Incidents", font=("HelveticaNeue Heavy", 24),
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

        # ---------- Main Content ----------
        content_wrapper = ctk.CTkFrame(self, fg_color=self.COLORS["main_bg"])
        content_wrapper.pack(side="left", fill="both", expand=True)

        title_lbl = ctk.CTkLabel(
            content_wrapper,
            text="Manage Incidents",
            font=("HelveticaNeue Heavy", 46),
            text_color="#111111"
        )
        title_lbl.pack(anchor="nw", pady=(26, 6), padx=30)

        # Outer bordered table container
        self.table_outer = ctk.CTkFrame(
            content_wrapper,
            fg_color=self.COLORS["table_outer_bg"],
            corner_radius=0,
            border_width=2,
            border_color=self.COLORS["table_border"],
            width=2000, height=900
        )
        self.table_outer.pack(padx=30, pady=(10, 30), fill="both", expand=False)
        self.table_outer.pack_propagate(False)

        # Header row -------------------------------------------------------
        self.header_frame = ctk.CTkFrame(self.table_outer, fg_color=self.COLORS["header_bg"], corner_radius=0)
        self.header_frame.pack(fill="x")

        # Configure columns (last column minsize for Edit button)
        for col, weight in enumerate(self.COL_WEIGHTS):
            if col == 5:
                self.header_frame.grid_columnconfigure(col, weight=weight, uniform="cols", minsize=100)
            else:
                self.header_frame.grid_columnconfigure(col, weight=weight, uniform="cols")

        # Name header (static)
        name_hdr = ctk.CTkLabel(
            self.header_frame, text="Name", font=("Helvetica", 15, "bold"),
            text_color=self.COLORS["header_text"], anchor="w"
        )
        name_hdr.grid(row=0, column=0, sticky="nsew", padx=self.CELL_PADX, pady=self.CELL_PADY)

        # Sortable headers
        self._make_sort_header("Incident Type", 1, "incident_type")
        self._make_sort_header("Location", 2, "location")
        self._make_sort_header("Urgency", 3, "urgency")
        # Add status header with a refresh button next to it
        self._make_sort_header("STATUS", 4, "status", add_refresh=True)

        # Non-sortable "Edit" header spacer
        ctk.CTkLabel(
            self.header_frame, text="", fg_color="transparent"
        ).grid(row=0, column=5, sticky="nsew", padx=self.CELL_PADX, pady=self.CELL_PADY)

        # Sub‑header row (search under Name only) --------------------------
        self.sub_header = ctk.CTkFrame(self.table_outer, fg_color=self.COLORS["subheader_bg"], corner_radius=0)
        self.sub_header.pack(fill="x")

        for col, weight in enumerate(self.COL_WEIGHTS):
            if col == 5:
                self.sub_header.grid_columnconfigure(col, weight=weight, uniform="cols", minsize=100)
            else:
                self.sub_header.grid_columnconfigure(col, weight=weight, uniform="cols")

        search_cell = ctk.CTkFrame(self.sub_header, fg_color="transparent", corner_radius=0)
        search_cell.grid(row=1, column=0, sticky="nsew", padx=self.CELL_PADX, pady=(0, 6))

        ctk.CTkLabel(
            search_cell,
            text="Search:",
            font=("Helvetica", 14, "bold"),
            text_color=self.COLORS["header_text"],
            anchor="w"
        ).pack(side="left", padx=(0, 6))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_cell,
            textvariable=self.search_var,
            width=240,
            fg_color=self.COLORS["search_entry_bg"],
            text_color=self.COLORS["header_text"],
            corner_radius=2,
            placeholder_text=""
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda e: self.render_rows())

        # Empty spacers to keep grid height/alignment for other columns
        for col in range(1, 6):
            ctk.CTkLabel(self.sub_header, text="", fg_color="transparent").grid(
                row=1, column=col, sticky="nsew", padx=self.CELL_PADX, pady=(0, 6)
            )

        # Scrollable body ---------------------------------------------------
        self.body_scroll = ctk.CTkScrollableFrame(self.table_outer, fg_color="#EDEDED", corner_radius=0)
        self.body_scroll.pack(fill="both", expand=True)

        for col, weight in enumerate(self.COL_WEIGHTS):
            if col == 5:
                self.body_scroll.grid_columnconfigure(col, weight=weight, uniform="cols", minsize=100)
            else:
                self.body_scroll.grid_columnconfigure(col, weight=weight, uniform="cols")

        self.render_rows()

    # ---------- Header helpers ----------
    def _make_sort_header(self, title: str, column_index: int, sort_key: str, add_refresh: bool = False):
        """
        Create a sort header in header_frame. If add_refresh is True, place a
        small refresh button to the right of the sort button (keeps UI intact).
        """
        # Place a container into the header cell so we can put both the sort button and a refresh button.
        container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        container.grid(row=0, column=column_index, sticky="nsew", padx=self.CELL_PADX, pady=self.CELL_PADY)

        btn = ctk.CTkButton(
            container,
            text=f"{title} [▼]",
            font=("Helvetica", 15, "bold"),
            fg_color="transparent",
            hover_color="#333333",
            text_color=self.COLORS["header_text"],
            corner_radius=0,
            width=10,
            command=lambda k=sort_key: self._toggle_sort(k)
        )
        # Pack the sort button left so refresh can sit to the right
        btn.pack(side="left", fill="x", expand=True)

        if add_refresh:
            # Small refresh button to the right of the status header
            refresh_btn = ctk.CTkButton(
                container,
                text="⟳",
                width=36,
                height=28,
                fg_color="transparent",
                hover_color="#2a2a2a",
                text_color=self.COLORS["header_text"],
                font=("Helvetica", 12, "bold"),
                corner_radius=4,
                command=self._on_refresh_clicked
            )
            refresh_btn.pack(side="right", padx=(8, 0))

        self._header_buttons[sort_key] = (btn, title)
        return btn

    def _toggle_sort(self, key: str):
        if self.sort_key == key:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_key = key
            self.sort_ascending = True
        for k, (btn, title) in self._header_buttons.items():
            if k == self.sort_key:
                arrow = "[▲]" if self.sort_ascending else "[▼]"
                btn.configure(text=f"{title} {arrow}")
            else:
                btn.configure(text=f"{title} [▼]")
        self.render_rows()

    # ---------- Data helpers ----------
    def _fetch(self) -> List[Dict[str, Any]]:
        db = getattr(self.app, "db", None)
        if not db:
            return []
        try:
            return db.read_tips()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tips: {e}")
            return []

    def _apply_search(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        q = self.search_var.get().strip().lower()
        if not q:
            return rows
        return [r for r in rows if q in (r.get("tip_name") or "").lower()]

    def _urgency_rank(self, u: str) -> int:
        order = {"low": 0, "medium": 1, "high": 2}
        return order.get((u or "").lower(), 99)

    def _status_rank(self, s: str) -> int:
        order = {"pending": 0, "investigating": 1, "resolved": 2}
        return order.get((s or "").lower(), 99)

    def _sort(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        key = self.sort_key

        def k(r):
            if key == "tip_name":
                return (r.get("tip_name") or "").lower()
            if key == "incident_type":
                return (r.get("incident_type") or "").lower()
            if key == "location":
                return (r.get("location") or "").lower()
            if key == "urgency":
                return self._urgency_rank(r.get("urgency"))
            if key == "status":
                return self._status_rank(r.get("status"))
            return (r.get("tip_name") or "").lower()

        return sorted(rows, key=k, reverse=not self.sort_ascending)

    # ---------- Rendering ----------
    def render_rows(self):
        for child in self.body_scroll.winfo_children():
            child.destroy()

        rows = self._sort(self._apply_search(self._fetch()))
        if not rows:
            ctk.CTkLabel(
                self.body_scroll,
                text="No incidents found.",
                font=("Helvetica", 16, "italic"),
                text_color=self.COLORS["no_rows_text"],
                fg_color="transparent"
            ).grid(row=0, column=0, columnspan=6, padx=20, pady=40, sticky="w")
            return

        for idx, r in enumerate(rows):
            bg = self.COLORS["row_bg"] if idx % 2 == 0 else self.COLORS["row_alt_bg"]

            # Name
            self._cell(self.body_scroll, idx, 0, r.get("tip_name") or "", bold=True, bg=bg)

            # Incident Type
            self._cell(self.body_scroll, idx, 1, r.get("incident_type") or "", bg=bg)

            # Location
            self._cell(self.body_scroll, idx, 2, r.get("location") or "", bg=bg)

            # Urgency
            self._cell(self.body_scroll, idx, 3, r.get("urgency") or "", bg=bg)

            # Status
            self._cell(self.body_scroll, idx, 4, r.get("status") or "Pending", bg=bg)

            # Edit button (per row, last column)
            edit_btn = ctk.CTkButton(
                self.body_scroll,
                text="Edit",
                width=80,
                fg_color="#99D1FF",
                hover_color="#1296FF",
                text_color="#000000",
                corner_radius=4,
                command=lambda row=r: self._edit_row(row)
            )
            edit_btn.grid(row=idx, column=5, sticky="e", padx=self.CELL_PADX, pady=self.CELL_PADY)

    def _cell(self, parent, row, col, text, bold=False, bg=None):
        font = ("Helvetica", 15, "bold") if bold else ("Helvetica", 15)
        lbl = ctk.CTkLabel(
            parent,
            text=text,
            font=font,
            text_color=self.COLORS["row_text"],
            fg_color=bg,
            anchor="w"
        )
        lbl.grid(row=row, column=col, sticky="nsew", padx=self.CELL_PADX, pady=self.CELL_PADY)

    # ---------- Actions ----------
    def _edit_row(self, row: Dict[str, Any]):
        # Navigate to your edit frame; pass the whole row for convenience
        try:
            self.app.show_frame("EditTipFrame", tip_row=row)
        except Exception:
            # Fallback: if edit frame expects tip_id
            try:
                self.app.show_frame("EditTipFrame", tip_id=row.get("id"))
            except Exception:
                messagebox.showerror("Error", "Edit screen is not available.")

    def logout(self):
        self.app.current_user = None
        self.app.show_frame("LoginFrame")

    # ---------- Refresh handler ----------
    def _on_refresh_clicked(self):
        """
        Called when user clicks the small refresh control next to STATUS.
        Refreshes rows from the database and re-renders the table.
        """
        # Optionally disable the button briefly or show a busy cursor if desired.
        try:
            self.render_rows()
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to refresh incidents: {ex}")