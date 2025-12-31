🧑‍🚀 Among Us Desktop Pet

A fun desktop pet inspired by Among Us!
Features:

Crewmates and an Impostor with knife animation

Walks around your desktop

Chat with your pets

Help menu (H) and Settings menu (O)

Optional AI replies using OpenAI

Optional walking sounds

🎮 Features

Multiple pets (Crewmates + Impostor)

Impostor pet is red and mischievous

Keyboard controls:

Space → Jump

F → Feed

N → Rename (not impostor)

H → Open/close help menu

O → Open/close settings menu

Mouse controls:

Left-click → Jump

Drag → Move pet

Double-click → Toggle follow mouse

Chat window → Type messages and pets respond

⚙️ Requirements

Python 3.8+

Optional:

pygame → For walking sounds (pip install pygame)

openai → For AI replies (pip install openai + set OPENAI_API_KEY)

Optional step.wav sound file for walking

If pygame or step.wav are missing, the program will still run safely.

📝 Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/amongus-desktop-pet.git
cd amongus-desktop-pet


Install dependencies (optional for sound and AI):

pip install pygame openai


Add step.wav to the project folder (optional).

Run the program:

python main.py


⚠️ Do not double-click the .py file if you want to see errors in the console.

💻 Controls
Mouse

Left-click → Jump

Drag → Move pet

Double-click → Follow mouse

Keyboard

Space → Jump

F → Feed

N → Rename (not impostor)

H → Help menu

O → Settings menu

Chat

Type your message → Press Enter → Pets respond

🎨 Customization

Change pet colors in the code (AmongUsPet class)

Adjust PET_COUNT, WALK_SPEED, PET_SIZE in settings section

Add your own .wav sounds for walking

⚠️ Notes

Transparent backgrounds work best on Windows

AI replies require an OpenAI API key

Sound is optional and auto-disabled if pygame or step.wav is missing

📜 License

This project is MIT licensed. Feel free to modify and share!
