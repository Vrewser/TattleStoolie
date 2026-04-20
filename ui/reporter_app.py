import customtkinter as ctk
from tkinter import messagebox


class ReporterApp(ctk.CTk):
    """Reporter application: separate secured interface for reporters only."""
    
    def __init__(self, db, incident_factory):
        super().__init__()
        self.db = db
        self.incident_factory = incident_factory
        self.current_user = None

        self.title("TattleStoolie - Reporter Portal")
        self.after(10, lambda: self.state("zoomed"))

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Frame registry: only reporter frames
        self.frame_registry = {
            "ReporterLoginFrame": ("ui.reporter_login_frame", "ReporterLoginFrame"),
            "ReporterRegisterFrame": ("ui.reporter_register_frame", "ReporterRegisterFrame"),
            "SubmitTipFrame": ("ui.reporter_submit_tip_frame", "SubmitTipFrame"),
            "ReporterExitFrame": ("ui.reporter_exit_frame", "ReporterExitFrame"),
        }

        self.dynamic_frame = set()
        self.frame_instances: dict[str, ctk.CTkFrame] = {}
        self.history: list[str] = []
        self._frame: ctk.CTkFrame | None = None

        self.show_frame("ReporterLoginFrame", push_history=False)

    def _is_reporter(self) -> bool:
        """Check if current user has reporter privileges."""
        user = getattr(self, "current_user", None)
        return bool(user and getattr(user, "is_reporter", lambda: False)())

    def _resolve_frame_class(self, key: str):
        """Lazily import and resolve frame class by registry key."""
        entry = self.frame_registry.get(key)
        if entry is None:
            raise KeyError(f"Frame '{key}' not registered")

        module_name, class_name = entry
        try:
            module = __import__(module_name, fromlist=[class_name])
        except Exception as e:
            raise ImportError(f"Failed to import {module_name} for frame '{key}': {e}") from e

        try:
            frame_class = getattr(module, class_name)
        except AttributeError as e:
            raise ImportError(
                f"Module {module_name} does not define class '{class_name}'."
            ) from e
        return frame_class

    def show_frame(self, frame_class_or_key, push_history: bool = True, **kwargs):
        """Navigate to a frame by key or class. Manages caching, history, and permissions."""
        if isinstance(frame_class_or_key, str):
            key = frame_class_or_key
            frame_class = self._resolve_frame_class(key)
        else:
            frame_class = frame_class_or_key
            key = frame_class.__name__

        # Enforce reporter authentication for protected frames
        protected_frames = {"SubmitTipFrame", "ReporterExitFrame"}
        if key in protected_frames and not self._is_reporter():
            messagebox.showerror("Forbidden", "Reporter access required.")
            key = "ReporterLoginFrame"
            frame_class = self._resolve_frame_class(key)
            push_history = False

        if push_history and self._frame:
            self.history.append(self._frame.__class__.__name__)

        needs_new_instance = (key in self.dynamic_frame) or (key not in self.frame_instances) or bool(kwargs)

        if needs_new_instance:
            if key in self.dynamic_frame and self._frame and self._frame.__class__.__name__ == key:
                self._frame.destroy()
            if key not in self.dynamic_frame and key in self.frame_instances and kwargs:
                self.frame_instances[key].destroy()

            frame_instance = frame_class(self.container, self, **kwargs)
            if key not in self.dynamic_frame and not kwargs:
                self.frame_instances[key] = frame_instance
        else:
            frame_instance = self.frame_instances[key]
            if kwargs and hasattr(frame_instance, "accept_kwargs"):
                try:
                    frame_instance.accept_kwargs(**kwargs)
                except Exception:
                    pass

        if self._frame:
            self._frame.grid_remove()

        frame_instance.grid(row=0, column=0, sticky="nsew")
        self._frame = frame_instance

    def go_back(self):
        """Navigate to previous frame in history; default to ReporterLoginFrame if empty."""
        while self.history:
            key = self.history.pop()
            if key in self.frame_registry:
                self.show_frame(key, push_history=False)
                return
        self.show_frame("ReporterLoginFrame", push_history=False)

    def logout(self):
        """Clear session and return to login."""
        self.current_user = None
        self.history.clear()
        self.show_frame("ReporterLoginFrame", push_history=False)
