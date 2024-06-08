import tkinter as tk
from PIL import Image, ImageTk
import random

class VirtualPet:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes("-topmost", True)  # Keep window on top
        self.root.geometry("+100+100")  # Initial position

        self.pet_image = Image.open("pet.gif")  # Path to your GIF
        self.pet_frames = []
        self.resize_factor = 0.5  # Factor to resize the image

        try:
            for frame in range(self.pet_image.n_frames):
                self.pet_image.seek(frame)
                frame_image = self.pet_image.copy()
                frame_image = frame_image.resize(
                    (int(frame_image.width * self.resize_factor), int(frame_image.height * self.resize_factor)),
                    Image.LANCZOS
                )
                self.pet_frames.append(ImageTk.PhotoImage(frame_image))
        except EOFError:
            pass
        
        self.frame_index = 0
        self.label = tk.Label(root, bd=0, bg='white')
        self.label.pack()
        self.update_frame()

        self.messages = [
            "Te amo.",
            "Buen día.",
            "¡Eres genial!",
            "¡Me alegra verte!",
            "Espero que tengas un buen día."
        ]
        self.display_message()

        # Bind the drag events to the label
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

    def update_frame(self):
        self.label.configure(image=self.pet_frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.pet_frames)
        self.root.after(100, self.update_frame)

    def display_message(self):
        message = random.choice(self.messages)
        self.label.configure(text=message, compound=tk.BOTTOM)
        delay = random.randint(10000, 40000)
        self.root.after(delay, self.display_message)

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.start_x
        y = self.root.winfo_y() + event.y - self.start_y
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    pet = VirtualPet(root)
    root.mainloop()
