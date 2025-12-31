import tkinter as tk
from tkinter import simpledialog
import random
import os

# ---------------- SAFE OPENAI SETUP ----------------
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

# ---------------- SAFE SOUND SETUP ----------------
try:
    import pygame
    pygame.mixer.init()
    try:
        STEP_SOUND = pygame.mixer.Sound("step.wav")
        SOUND_AVAILABLE = True
    except:
        STEP_SOUND = None
        SOUND_AVAILABLE = False
except:
    STEP_SOUND = None
    SOUND_AVAILABLE = False

# ---------------- SETTINGS ----------------
PET_SIZE = 120
GRAVITY = 2
WALK_SPEED = 3
PET_COUNT = 2

pets = []
screen_width = None
screen_height = None

help_window = None
settings_window = None
help_lock = False
ai_enabled = True
sound_enabled = SOUND_AVAILABLE

# ---------------- AI ----------------
def ai_reply(user_message, impostor=False):
    if not OPENAI_AVAILABLE or not ai_enabled:
        return random.choice(["Hi!", "Hmm...", "Okay!", "Beep!"])
    try:
        system_prompt = "You are a cute, friendly Among Us desktop pet. Replies must be short, kid-friendly, safe."
        if impostor:
            system_prompt += " You are mischievous but harmless."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=40
        )
        return response.choices[0].message.content.strip()
    except:
        return random.choice(["...", "Hmm?", "Walking 🚶"])

# ---------------- HELP MENU ----------------
def unlock_help():
    global help_lock
    help_lock = False

def toggle_help():
    global help_window, help_lock
    if help_lock:
        return
    help_lock = True

    if help_window and help_window.winfo_exists():
        help_window.destroy()
        help_window = None
    else:
        help_window = tk.Toplevel()
        help_window.title("Controls")
        help_window.geometry("360x330")
        help_window.attributes("-topmost", True)
        text = (
            "🧑‍🚀 AMONG US DESKTOP PET\n\n"
            "🖱 Mouse:\n"
            "• Left Click → Jump\n"
            "• Drag → Move pet\n"
            "• Double Click → Follow mouse\n\n"
            "⌨ Keyboard:\n"
            "• Space → Jump\n"
            "• F → Feed\n"
            "• N → Rename (not impostor)\n"
            "• H → Help menu\n"
            "• O → Settings\n\n"
            "💬 Chat:\n"
            "• Type + Enter → Talk\n\n"
            "👹 Impostor:\n"
            "• Red\n"
            "• Knife animation\n"
            "• Mischievous replies\n"
        )
        tk.Label(help_window, text=text, justify="left", font=("Arial", 10)).pack(padx=10, pady=10)

    if help_window:
        help_window.after(300, unlock_help)

# ---------------- SETTINGS MENU ----------------
def toggle_settings():
    global settings_window, ai_enabled, sound_enabled
    if settings_window and settings_window.winfo_exists():
        settings_window.destroy()
        settings_window = None
        return

    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    settings_window.geometry("220x160")
    settings_window.attributes("-topmost", True)

    def toggle_ai():
        global ai_enabled
        ai_enabled = not ai_enabled
        ai_btn.config(text=f"AI: {'ON' if ai_enabled else 'OFF'}")

    def toggle_sound():
        global sound_enabled
        sound_enabled = not sound_enabled
        sound_btn.config(text=f"Sound: {'ON' if sound_enabled else 'OFF'}")

    ai_btn = tk.Button(settings_window, text=f"AI: {'ON' if ai_enabled else 'OFF'}", command=toggle_ai)
    ai_btn.pack(pady=10)
    sound_btn = tk.Button(settings_window, text=f"Sound: {'ON' if sound_enabled else 'OFF'}", command=toggle_sound)
    sound_btn.pack(pady=10)

# ---------------- PET CLASS ----------------
class AmongUsPet:
    def __init__(self, x):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="black")
        self.root.wm_attributes("-transparentcolor", "black")

        self.canvas = tk.Canvas(self.root, width=PET_SIZE, height=PET_SIZE, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.name = "Crewmate"
        self.color = random.choice(["blue", "green", "pink", "yellow"])
        self.impostor = False

        self.x = x
        self.y = 50
        self.vx = random.choice([-WALK_SPEED, WALK_SPEED])
        self.vy = 0

        self.walk_frame = 0
        self.knife_angle = 0
        self.knife_dir = 1

        self.dragging = False
        self.follow_mouse = False
        self.speech_id = None

        self.root.geometry(f"{PET_SIZE}x{PET_SIZE}+{self.x}+{self.y}")

        self.canvas.bind("<Button-1>", self.jump)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Double-Button-1>", self.toggle_follow)

        self.root.bind("f", self.feed)
        self.root.bind("n", self.rename)
        self.root.bind("h", lambda e: toggle_help())
        self.root.bind("o", lambda e: toggle_settings())

        self.update()

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(PET_SIZE//2, 10, text=self.name, fill="white", font=("Arial", 9, "bold"))
        leg = 6 if self.walk_frame % 2 == 0 else -6
        self.canvas.create_oval(16, 40, 34, 86, fill=self.color, outline="black")
        self.canvas.create_oval(30, 20, 90, 100, fill=self.color, outline="black", width=3)
        self.canvas.create_rectangle(42, 96, 56, 112 + leg, fill=self.color)
        self.canvas.create_rectangle(64, 96, 78, 112 - leg, fill=self.color)
        self.canvas.create_oval(54, 36, 96, 66, fill="#6fdfff", outline="black")

        if self.impostor:
            self.animate_knife()
        if self.speech_id:
            self.canvas.tag_raise(self.speech_id)

    def animate_knife(self):
        self.knife_angle += self.knife_dir * 3
        if abs(self.knife_angle) > 15:
            self.knife_dir *= -1
        o = self.knife_angle // 2
        self.canvas.create_rectangle(86, 60 + o, 96, 70 + o, fill="#5a3b1e", outline="black")
        self.canvas.create_polygon(96, 60 + o, 120, 65 + o, 96, 70 + o, fill="#d9d9d9", outline="black")

    def jump(self, e=None):
        self.vy = -25

    def drag(self, e):
        self.dragging = True
        self.x = e.x_root - PET_SIZE // 2
        self.y = e.y_root - PET_SIZE // 2

    def stop_drag(self, e):
        self.dragging = False

    def toggle_follow(self, e):
        self.follow_mouse = not self.follow_mouse

    def feed(self, e=None):
        self.say("Yum!")

    def rename(self, e=None):
        if self.impostor:
            self.say("😈")
            return
        name = simpledialog.askstring("Rename", "New name?")
        if name:
            self.name = name

    def receive_message(self, msg):
        if "jump" in msg.lower():
            self.jump()
        self.say(ai_reply(msg, self.impostor))

    def say(self, text):
        if self.speech_id:
            self.canvas.delete(self.speech_id)
        self.speech_id = self.canvas.create_text(PET_SIZE//2, 0, text=text, fill="white")
        self.root.after(2500, lambda: self.canvas.delete(self.speech_id))

    def update(self):
        global screen_width, screen_height
        if screen_width is None:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

        if not self.dragging:
            self.vy += GRAVITY
            self.y += self.vy

        floor = screen_height - PET_SIZE - 40
        if self.y > floor:
            self.y = floor
            self.vy = 0

        self.x += self.vx
        if self.x <= 0 or self.x >= screen_width - PET_SIZE:
            self.vx *= -1

        if STEP_SOUND and sound_enabled and self.walk_frame % 7 == 0:
            try:
                STEP_SOUND.play()
            except:
                pass

        self.walk_frame += 1
        self.draw()
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self.root.after(50, self.update)

# ---------------- MAIN ----------------
try:
    root = tk.Tk()
    root.withdraw()
    root.bind_all("<h>", lambda e: toggle_help())
    root.bind_all("<o>", lambda e: toggle_settings())

    for i in range(PET_COUNT):
        pet = AmongUsPet(100 + i * (PET_SIZE + 60))
        if i == 0:
            pet.impostor = True
            pet.color = "red"
            pet.name = "Impostor"
        pets.append(pet)

    chat = tk.Toplevel()
    chat.title("Chat")
    chat.geometry("400x50")
    entry = tk.Entry(chat)
    entry.pack(fill="both", expand=True)

    def send(e=None):
        msg = entry.get()
        for p in pets:
            p.receive_message(msg)
        entry.delete(0, tk.END)

    entry.bind("<Return>", send)
    root.mainloop()
except Exception as e:
    print("Error occurred:", e)
    input("Press Enter to exit...")
