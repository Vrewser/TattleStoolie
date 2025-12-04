import customtkinter as ctk
from PIL import Image, ImageTk

# Module: dashboard_frame.py
# Purpose: Present an overview dashboard for users.
# This frame shows urgency buckets, a global list of incidents and provides
# navigation via the left sidebar. It fetches incidents from the app's DB
# and populates the urgency boxes and a simple global list.
# Comments below explain the role of major methods and areas.

URGENCY_ORDER = ["High", "Medium", "Low"]
URGENCY_BG = {
    "High": "#1E1E1E",
    "Medium": "#4A4A4A",
    "Low": "#6A6A6A"
}


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        # Standard frame initialization and configuration.
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#BDBDBD")

        # ------------------ SIDEBAR (left) ------------------
        # Reused sidebar: logo + navigation buttons; consistent across UI pages.
        self.sidebar = ctk.CTkFrame(self, fg_color="#2E2E2E", width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Attempt to display a logo image, with fallback to simple text.
        try:
            main_logo = ctk.CTkImage(light_image=Image.open("assets/main_logo.png"), size=(60, 60))
            ctk.CTkLabel(self.sidebar, image=main_logo, text="",
                         width=60, height=60, corner_radius=0, fg_color="#2B2B2B").pack(pady=(25, 10))
        except Exception:
            ctk.CTkLabel(self.sidebar, text="TS", font=("Helvetica", 42, "bold"),
                         text_color="white").pack(pady=(25, 10))

        # Sidebar title
        ctk.CTkLabel(self.sidebar, text="Dashboard",
                     font=("Helvetica", 28, "bold"), text_color="white").pack(pady=(0, 30))

        # Navigation buttons: Home, Submit, Manage, Sign out (manage shown only for admins)
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
            command=lambda: self.app.show_frame("AdminSubmitTipFrame")  # navigates to admin submit
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

        # ------------------ CENTER PANEL ------------------
        # Main content area showing title and urgency boxes stacked vertically.
        self.center_panel = ctk.CTkFrame(self, fg_color="#D3D3D3", corner_radius=0)
        self.center_panel.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(self.center_panel, text="TattleStoolie",
                     font=("HelveticaNeue Heavy", 70),
                     text_color="black").pack(pady=(15, 4))

        # urgency_stack holds the three urgency boxes (High / Medium / Low)
        self.urgency_stack = ctk.CTkFrame(self.center_panel, fg_color="transparent")
        self.urgency_stack.pack(pady=10, fill="x")

        self.urgency_boxes = {}
        INNER_PADDING_X = 12

        # Create one urgency box per urgency level. Each box contains a header and a scroll area.
        for urgency in URGENCY_ORDER:
            # Wrapper allows the box to occupy full width within the center panel.
            wrapper = ctk.CTkFrame(self.urgency_stack, fg_color="transparent", width=1200)
            wrapper.pack(pady=12)

            # Main colored frame for the urgency bucket
            main = ctk.CTkFrame(wrapper, fg_color=URGENCY_BG[urgency], corner_radius=10)
            main.pack(fill="x", expand=True)

            # Header area: title and count
            header = ctk.CTkFrame(main, fg_color="#2B2B2B", corner_radius=6)
            header.pack(padx=INNER_PADDING_X, pady=(8, 4))

            title_lbl = ctk.CTkLabel(header, text=f"{urgency.upper()} URGENCY",
                                     font=("Helvetica", 16, "bold"), text_color="#E0E0E0")
            title_lbl.pack(side="left", padx=10)

            count_lbl = ctk.CTkLabel(header, text="(0)",
                                     font=("Helvetica", 15), text_color="#E0E0E0")
            count_lbl.pack(side="right", padx=10)

            # Scrollable frame contains simple rows for incidents of this urgency.
            scroll = ctk.CTkScrollableFrame(main, fg_color="#3C3C3C", corner_radius=6, width=1150, height=120)
            scroll.pack(padx=INNER_PADDING_X, pady=(0, 10))

            self.urgency_boxes[urgency] = {
                "count": count_lbl,
                "scroll": scroll
            }

        # ------------------ RIGHT PANEL (global list) ------------------
        # Shows a global list of incident names and types.
        self.right_panel = ctk.CTkFrame(self, fg_color="#C0C0C0", corner_radius=15, width=320)
        self.right_panel.pack(side="right", fill="y", padx=20, pady=20)
        self.right_panel.pack_propagate(False)

        all_incidents = ctk.CTkLabel(
            self.right_panel,
            text="  Name\t|\tIncident Type ",
            font=("Helvetica", 18, "bold"),
            text_color="white",
            fg_color="#212121"
        )
        all_incidents.pack(pady=(20, 6))
        all_incidents.configure(width=300, height=50)

        # A scrollable area that lists incidents in compact rows.
        self.global_scroll = ctk.CTkScrollableFrame(
            self.right_panel,
            fg_color="#858585",
            corner_radius=10,
            width=300,
            height=520)
        self.global_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.global_rows_container = ctk.CTkFrame(self.global_scroll, fg_color="transparent")
        self.global_rows_container.pack(fill="x")

    # ---------- Lifecycle ----------
    def on_show(self):
        # Called by the app when this frame is shown. Refreshes visibility and data.
        print("[Dashboard] on_show invoked")
        self._apply_role_visibility()
        self._load_urgency_boxes()
        self._load_global_list()

    # ---------- Role visibility ----------
    def _apply_role_visibility(self):
        # Show or hide admin-only controls depending on current_user role.
        user = getattr(self.app, "current_user", None)
        is_admin = bool(user and getattr(user, "is_admin", lambda: False)())
        manage_btn = getattr(self, "manage_btn", None)
        if not manage_btn:
            return
        if not is_admin:
            # Remove manage button for non-admins.
            if manage_btn.winfo_manager():
                manage_btn.pack_forget()
        else:
            # Restore manage button for admins.
            if not manage_btn.winfo_manager():
                manage_btn.pack(pady=10)

    # ---------- Data fetch ----------
    def _get_incidents(self):
        # Fetch incidents via the DB API. Supports multiple DB method names for compatibility.
        db = getattr(self.app, "db", None)
        if not db:
            print("[Dashboard] No DB instance.")
            return []
        if hasattr(db, "get_all_incidents"):
            rows = db.get_all_incidents()
            print(f"[Dashboard] get_all_incidents -> {len(rows)} rows")
            return rows
        elif hasattr(db, "read_tips"):
            rows = db.read_tips()
            print(f"[Dashboard] read_tips -> {len(rows)} rows")
            return rows
        print("[Dashboard] No suitable DB method.")
        return []

    # ---------- Urgency box loader ----------
    def _load_urgency_boxes(self):
        # Populate each urgency bucket with incidents and update counts.
        incidents = self._get_incidents()
        buckets = {u: [] for u in URGENCY_ORDER}
        for inc in incidents:
            u = (inc.get("urgency") or "").strip().capitalize()
            if u in buckets:
                buckets[u].append(inc)
        for u in URGENCY_ORDER:
            box = self.urgency_boxes[u]
            scroll = box["scroll"]
            # Some CTkScrollableFrame implementations provide scrollable_frame attr.
            scroll_parent = getattr(scroll, "scrollable_frame", scroll)
            for child in scroll_parent.winfo_children():
                child.destroy()
            data = buckets[u]
            box["count"].configure(text=f"({len(data)})")
            print(f"[Dashboard] Loading {u}: {len(data)} items")
            if not data:
                # Show placeholder when no incidents present.
                ctk.CTkLabel(scroll_parent, text="No incidents.",
                             font=("Helvetica", 14), text_color="#E0E0E0").pack(pady=6)
                continue
            for inc in data:
                self._create_simple_name_row(scroll_parent, inc)

    def _create_simple_name_row(self, parent, inc):
        # Render a compact row with the incident's tip name.
        try:
            tip_name = inc.get("tip_name", "Unknown")
            print(f"[Dashboard] Creating row for tip_name='{tip_name}'")
            row = ctk.CTkFrame(parent, fg_color="#4F4F4F", corner_radius=4)
            row.pack(fill="x", padx=6, pady=3)
            text_tip = ctk.CTkLabel(
                row, text=tip_name,
                font=("Helvetica", 14, "bold"),
                text_color="white", anchor="w"
            )
            text_tip.pack(side="left", padx=10, pady=6)
        except Exception as e:
            # Defensive logging so a single bad row does not break the dashboard.
            print("[Dashboard] Row creation error:", e)

    # ---------- Global list ----------
    def _load_global_list(self):
        # Populate the right-hand global list with all incidents sorted by name.
        container = self.global_rows_container
        for child in container.winfo_children():
            child.destroy()
        incidents = self._get_incidents()
        if not incidents:
            ctk.CTkLabel(container, text="No incidents.",
                         font=("Helvetica", 14), text_color="black").pack(pady=6)
            return
        incidents_sorted = sorted(incidents, key=lambda i: (i.get("tip_name") or "").lower())
        for inc in incidents_sorted:
            tip_name = inc.get("tip_name", "Unknown")
            itype = inc.get("incident_type", "N/A")
            row = ctk.CTkFrame(container, fg_color="#B7B7B7", corner_radius=4)
            row.pack(fill="x", padx=4, pady=3)
            ctk.CTkLabel(row, text=tip_name, font=("Helvetica", 13, "bold"),
                         text_color="black", anchor="w").pack(side="left", padx=8, pady=4)
            ctk.CTkLabel(row, text=itype, font=("Helvetica", 13),
                         text_color="black", anchor="w").pack(side="right", padx=8, pady=4)

    # ---------- Logout ----------
    def logout(self):
        # Clear session and navigate to login.
        self.app.current_user = None
        self.app.show_frame("LoginFrame")