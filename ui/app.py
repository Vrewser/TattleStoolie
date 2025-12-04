import customtkinter as ctk
from tkinter import messagebox

# Module: app.py
# Purpose: Main application class and frame navigation manager.
# TattleApp is a thin wrapper around CTk that:
# - Holds application-wide objects (db, incident_factory, current_user)
# - Lazily resolves and instantiates UI frames on demand to avoid circular imports
# - Manages navigation history and admin-only access controls
# Only comments are added to document behaviors and responsibilities.

class TattleApp(ctk.CTk):
    def __init__(self, db, incident_factory):
        super().__init__()
        # Application-level services and state
        self.db = db
        self.incident_factory = incident_factory
        self.current_user = None

        # Window setup
        self.title("TattleStoolie")
        self.after(10, lambda: self.state("zoomed"))

        # Container frame used to host page frames (one at a time)
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Registry mapping frame keys to module/class for lazy import
        # This lets show_frame import only as required, avoiding import-time cycles.
        self.frame_registry = {
            "LoginFrame": ("ui.login_frame", "LoginFrame"),
            "RegisterFrame": ("ui.register_frame", "RegisterFrame"),
            "DashboardFrame": ("ui.dashboard_frame", "DashboardFrame"),
            "SubmitTipFrame": ("ui.reporter_submit_tip_frame", "SubmitTipFrame"),
            "AdminSubmitTipFrame": ("ui.admin_submit_tip_frame", "AdminSubmitTipFrame"),
            "ManageTipsFrame": ("ui.manage_tips_frame", "ManageTipsFrame"),
            "EditTipFrame": ("ui.edit_tip_frame", "EditTipFrame"),
            "ReporterExitFrame": ("ui.reporter_exit_frame", "ReporterExitFrame"),
        }

        # Frames requiring admin privileges
        self.admin_only_frames = {"DashboardFrame", "ManageTipsFrame", "AdminSubmitTipFrame"}

        # Frames that should always be re-instantiated when shown (dynamic)
        self.dynamic_frame = {"EditTipFrame"}

        # Cache of persistent (static) frame instances
        self.frame_instances: dict[str, ctk.CTkFrame] = {}

        # Navigation history for back navigation support
        self.history: list[str] = []

        # Currently displayed frame
        self._frame: ctk.CTkFrame | None = None

        # Start the app at the login screen
        self.show_frame("LoginFrame", push_history=False)

    def _is_admin(self) -> bool:
        # Helper: check if current user has admin privileges (callable or attribute)
        user = getattr(self, "current_user", None)
        return bool(user and getattr(user, "is_admin", lambda: False)())

    def _resolve_frame_class(self, key: str):
        """
        Lazily import and resolve the frame class for the given key.
        Raises a clear ImportError/KeyError when resolution fails.
        """
        entry = self.frame_registry.get(key)
        if entry is None:
            raise KeyError(f"Frame '{key}' not registered")

        module_name, class_name = entry
        # Import module on demand to avoid import cycles
        try:
            module = __import__(module_name, fromlist=[class_name])
        except Exception as e:
            raise ImportError(f"Failed to import module {module_name} for frame '{key}': {e}") from e

        # Retrieve the class object from the imported module
        try:
            frame_class = getattr(module, class_name)
        except AttributeError as e:
            raise ImportError(
                f"Module {module_name} does not define class '{class_name}' for frame '{key}'."
            ) from e
        return frame_class

    def show_frame(self, frame_class_or_key, push_history: bool = True, **kwargs):
        # Normalize input: accept either a registered key or a frame class
        if isinstance(frame_class_or_key, str):
            key = frame_class_or_key
            frame_class = self._resolve_frame_class(key)
        else:
            frame_class = frame_class_or_key
            key = frame_class.__name__

        original_key = key  # track requested key for history logic

        # Enforce admin-only access: redirect to SubmitTipFrame on denial
        if key in self.admin_only_frames and not self._is_admin():
            messagebox.showerror("Forbidden", "You do not have permission to view that screen.")
            key = "SubmitTipFrame"
            frame_class = self._resolve_frame_class(key)
            # Do not push history for a failed attempt; it's a redirect
            push_history = False

        # Push current frame onto history stack when appropriate
        if push_history and self._frame:
            prev_key = self._frame.__class__.__name__
            self.history.append(prev_key)

        # Decide whether to instantiate a new frame or reuse a cached one
        needs_new_instance = (key in self.dynamic_frame) or (key not in self.frame_instances) or bool(kwargs)

        if needs_new_instance:
            # For dynamic frames we replace the existing instance, for static frames we may cache
            if key in self.dynamic_frame and self._frame and self._frame.__class__.__name__ == key:
                # Replace the currently shown dynamic frame
                self._frame.destroy()
            # For static frames: if kwargs provided, destroy old instance so new args apply
            if key not in self.dynamic_frame and key in self.frame_instances and kwargs:
                self.frame_instances[key].destroy()

            # Instantiate the frame and cache if static
            frame_instance = frame_class(self.container, self, **kwargs)
            if key not in self.dynamic_frame and not kwargs:
                self.frame_instances[key] = frame_instance
        else:
            # Reuse the cached instance
            frame_instance = self.frame_instances[key]
            # If the frame supports accept_kwargs, attempt to update it instead of re-creating
            if kwargs and hasattr(frame_instance, "accept_kwargs"):
                try:
                    frame_instance.accept_kwargs(**kwargs)
                except Exception as e:
                    print(f"[App] accept_kwargs failed for {key}: {e}")

        # Replace the visible frame in the container
        if self._frame and frame_instance is not self._frame:
            self._frame.pack_forget()

        self._frame = frame_instance
        self._frame.pack(fill="both", expand=True)

        # Call optional on_show lifecycle hook to allow frames to refresh when displayed
        if hasattr(frame_instance, "on_show"):
            try:
                frame_instance.on_show()
            except Exception as e:
                print(f"[App] on_show failed for {key}: {e}")

    def go_back(self):
        """Pop from history and navigate to previous frame. Falls back to LoginFrame if empty."""
        while self.history:
            key = self.history.pop()
            # Skip unknown keys for safety
            if key in self.frame_registry:
                self.show_frame(key, push_history=False)
                return
        # If history is empty, go to login
        self.show_frame("LoginFrame", push_history=False)

    def logout(self):
        # Clear session state and navigate to login; also reset history.
        self.current_user = None
        self.history.clear()
        self.show_frame("LoginFrame", push_history=False)