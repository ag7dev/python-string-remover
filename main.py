import customtkinter
import tkinter
import pymem
import gc
import requests
from plyer import notification
from CTkMessagebox import CTkMessagebox
import threading

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

class ColorManager:
    _instance = None
    _current_color = "#2CC985"
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get(cls):
        return cls._current_color
    
    @classmethod
    def set(cls, color):
        cls._current_color = color
        if hasattr(cls, '_callback'):
            cls._callback(color)
    
    @classmethod
    def register_callback(cls, callback):
        cls._callback = callback

class StringDeleterApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.color_manager = ColorManager()
        self.color_manager.register_callback(self.update_colors)
        
        self.title("ag7-dev.de String Deleter")
        self.geometry("450x550")
        self.minsize(450, 550)
        
        self.is_loading = False
        self.progress = 0
        self.process = None
        
        self.create_widgets()
        self.create_progress_bar()
        self.create_theme_switch()
        self.create_color_picker()
        
    def create_widgets(self):
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.title_label = customtkinter.CTkLabel(
            self.main_frame,
            text="STRING DELETER",
            font=("Roboto Bold", 24),
            text_color=self.color_manager.get()
        )
        self.title_label.pack(pady=(20, 30))

        input_fields = [
            ("Process name", "exe-filename.exe"),
            ("Address (Hex)", "0x..."),
            ("Length", "123")
        ]
        
        self.entries = []
        for i, (label_text, placeholder) in enumerate(input_fields):
            frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
            frame.pack(pady=5, fill="x", padx=20)
            
            label = customtkinter.CTkLabel(frame, text=label_text, width=100, anchor="w")
            label.pack(side="left", padx=(0, 10))
            
            entry = customtkinter.CTkEntry(
                frame,
                placeholder_text=placeholder,
                width=200,
                height=35,
                corner_radius=10
            )
            entry.pack(side="right", fill="x", expand=True)
            self.entries.append(entry)

        self.delete_btn = customtkinter.CTkButton(
            self.main_frame,
            text="Remove String",
            command=self.start_delete_thread,
            height=40,
            font=("Roboto Medium", 16),
            fg_color=self.color_manager.get(),
            hover_color=self.adjust_color(self.color_manager.get(), -20),
            corner_radius=10
        )
        self.delete_btn.pack(pady=30, fill="x", padx=20)

    def create_color_picker(self):
        color_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        color_frame.pack(pady=10, padx=20, fill="x")
        
        self.color_option = customtkinter.CTkOptionMenu(
            color_frame,
            values=["Green", "Blue", "Purple", "Red", "Orange"],
            command=self.change_accent_color,
            fg_color=self.color_manager.get(),
            button_color=self.color_manager.get(),
            button_hover_color=self.adjust_color(self.color_manager.get(), -20)
        )
        self.color_option.pack(side="right")
        
        label = customtkinter.CTkLabel(color_frame, text="Accent Color:")
        label.pack(side="right", padx=10)

    def adjust_color(self, hex_color, amount):
        rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
        new_rgb = [min(255, max(0, c + amount)) for c in rgb]
        return "#{:02x}{:02x}{:02x}".format(*new_rgb)

    def change_accent_color(self, choice):
        color_map = {
            "Green": "#2CC985",
            "Blue": "#2196F3",
            "Purple": "#9C27B0",
            "Red": "#F44336",
            "Orange": "#FF9800"
        }
        new_color = color_map.get(choice, "#2CC985")
        self.color_manager.set(new_color)

    def update_colors(self, color):
        self.title_label.configure(text_color=color)
        self.delete_btn.configure(
            fg_color=color,
            hover_color=self.adjust_color(color, -20)
        )
        self.progress_bar.configure(progress_color=color)
        self.theme_switch.configure(progress_color=color)
        self.color_option.configure(
            fg_color=color,
            button_color=color,
            button_hover_color=self.adjust_color(color, -20)
        )

    def create_progress_bar(self):
        self.progress_bar = customtkinter.CTkProgressBar(
            self,
            height=15,
            progress_color=self.color_manager.get(),
            mode="indeterminate"
        )
        self.progress_bar.pack(side="bottom", fill="x", padx=20, pady=20)
        self.progress_bar.stop()
        self.progress_bar.set(0)

    def create_theme_switch(self):
        self.theme_switch = customtkinter.CTkSwitch(
            self,
            text="Dark Mode",
            command=self.toggle_theme,
            progress_color=self.color_manager.get()
        )
        self.theme_switch.pack(side="top", anchor="ne", padx=20, pady=10)
        if customtkinter.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def toggle_theme(self):
        current = customtkinter.get_appearance_mode()
        new_mode = "Dark" if current == "Light" else "Light"
        customtkinter.set_appearance_mode(new_mode)
        self.theme_switch.configure(text=f"{new_mode} Mode")

    def start_delete_thread(self):
        if not self.is_loading:
            thread = threading.Thread(target=self.delete_string)
            thread.start()

    def validate_inputs(self):
        try:
            proc_name = self.entries[0].get()
            address = int(self.entries[1].get(), 0)
            length = int(self.entries[2].get())
            
            if not proc_name:
                raise ValueError("Process name cannot be empty")
            if length <= 0:
                raise ValueError("Length must be positive")
            
            return proc_name, address, length
        except ValueError as e:
            CTkMessagebox(title="Input Error", message=f"Invalid input: {e}", icon="cancel")
            raise

    def toggle_loading(self, state):
        self.is_loading = state
        self.delete_btn.configure(state="disabled" if state else "normal")
        if state:
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.set(0)

    def delete_string(self):
        try:
            self.toggle_loading(True)
            proc_name, address, length = self.validate_inputs()
            
            try:
                pm = pymem.Pymem(proc_name)
                original = pm.read_string(address, length)
                
                pm.write_string(address, "." * length)
                gc.collect()
                
                notification.notify(
                    title="Operation Successful",
                    message="String successfully overwritten!",
                    timeout=5
                )
                
                CTkMessagebox(
                    title="Success",
                    message=f"Original string: {original}\nReplaced with: {'.'*length}",
                    icon="check"
                )
                
            except pymem.exception.ProcessNotFound:
                CTkMessagebox(title="Error", message="Process not found!", icon="cancel")
            except pymem.exception.MemoryReadError:
                CTkMessagebox(title="Error", message="Invalid memory address", icon="cancel")
            except Exception as e:
                CTkMessagebox(title="Error", message=str(e), icon="cancel")

        finally:
            self.toggle_loading(False)

if __name__ == "__main__":
    app = StringDeleterApp()
    app.mainloop()
