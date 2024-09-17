import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import os
import sys
import webbrowser

# Function to get the image path
def get_image_path(word):
    try:
        base_path = sys._MEIPASS  # This is where PyInstaller unpacks the files
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(base_path, '..', 'assets', 'images')
    images = {
        "AdamSmith": "adam_smith.png", "CharlesBabbage": "charles_babbage.png",
        "EdwardsDeming": "edwards_deming.png", "EliWhitney": "eli_whitney.png",
        "EltonMayo": "elton_mayo.png", "FrederickWTaylor": "frederick_taylor.png",
        "HenryFord": "henry_ford.png", "HenryGantt": "henry_gantt.png",
        "JamesPWomack": "james_womack.png", "JohnPKotter": "john_kotter.png",
        "JoshepMJuran": "joseph_juran.png", "KaoruIshikawa": "kaoru_ishikawa.png",
        "KurtLewin": "kurt_lewin.png", "MorrisCooke": "morris_cooke.png",
        "PeterSenge": "peter_senge.png", "ShigeoShingo": "shigeo_shingo.png",
        "TaiichiOhno": "taiichi_ohno.png", "WalterAShewhart": "walter_shewhart.png",
        "default": "default.png"
    }
    return os.path.join(images_path, images.get(word, "default.png"))

# Dictionary to map scientist names to their Wikipedia URLs
wikipedia_urls = {
    "AdamSmith": "https://en.wikipedia.org/wiki/Adam_Smith",
    "CharlesBabbage": "https://en.wikipedia.org/wiki/Charles_Babbage",
    "EdwardsDeming": "https://en.wikipedia.org/wiki/W._Edwards_Deming",
    "EliWhitney": "https://en.wikipedia.org/wiki/Eli_Whitney",
    "EltonMayo": "https://en.wikipedia.org/wiki/Elton_Mayo",
    "FrederickWTaylor": "https://en.wikipedia.org/wiki/Frederick_Winslow_Taylor",
    "HenryFord": "https://en.wikipedia.org/wiki/Henry_Ford",
    "HenryGantt": "https://en.wikipedia.org/wiki/Henry_Gantt",
    "JamesPWomack": "https://en.wikipedia.org/wiki/James_P._Womack",
    "JohnPKotter": "https://en.wikipedia.org/wiki/John_P._Kotter",
    "JoshepMJuran": "https://en.wikipedia.org/wiki/Joseph_M._Juran",
    "KaoruIshikawa": "https://en.wikipedia.org/wiki/Kaoru_Ishikawa",
    "KurtLewin": "https://en.wikipedia.org/wiki/Kurt_Lewin",
    "MorrisCooke": "https://en.wikipedia.org/wiki/Morris_Llewellyn_Cooke",
    "PeterSenge": "https://en.wikipedia.org/wiki/Peter_Senge",
    "ShigeoShingo": "https://en.wikipedia.org/wiki/Shigeo_Shingo",
    "TaiichiOhno": "https://en.wikipedia.org/wiki/Taiichi_Ohno",
    "WalterAShewhart": "https://en.wikipedia.org/wiki/Walter_A._Shewhart"
}

# Function to display the image and name
def show_image(word, name_label, image_label):
    image_path = get_image_path(word)
    if word == "default":
        name_label.config(text="")
    elif not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return
    image = Image.open(image_path).resize((300, 475), Image.LANCZOS)
    name_label.config(
        text=f"\nclick on image for more info",
        font=("Arial", 10),  # Smaller font size
        fg="#888888"  # Lighter color to simulate transparency
    )
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
    image_label.name = word  # Store the name in the label for later use

# Function to update the word list and display the image
def update_word_list(found_word, word_labels, name_label, image_label):
    for lbl in word_labels:
        if lbl['text'].lower() == found_word.lower():
            lbl.config(fg="gray", font="Arial 10 overstrike")
            break
    show_image(found_word, name_label, image_label)

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_labels, name_label, image_label):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]
    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="#FFB6C1", state="disabled")  # Light pink for correct words
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_labels, name_label, image_label)
        correct_words.pop(correct_word_index)
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':
            btn.config(bg="#ADD8E6")  # Light blue for default

# Function to handle button press
def handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels, name_label, image_label):
    if event.type == tk.EventType.ButtonPress:
        reset_selection(selected_buttons)
        selected_buttons.clear()
        select_button(event.widget, selected_buttons)
    elif event.type == tk.EventType.Motion:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget not in selected_buttons:
            if is_linear_selection(selected_buttons, widget):
                select_button(widget, selected_buttons)
    elif event.type == tk.EventType.ButtonRelease:
        check_word(selected_buttons, correct_words, word_labels, name_label, image_label)

# Helper function to check if the selection is linear
def is_linear_selection(selected_buttons, new_button):
    if not selected_buttons:
        return True
    first_button = selected_buttons[0]
    row_diff = new_button.grid_info()['row'] - first_button.grid_info()['row']
    col_diff = new_button.grid_info()['column'] - first_button.grid_info()['column']
    for btn in selected_buttons:
        if (new_button.grid_info()['row'] - btn.grid_info()['row']) * col_diff != (new_button.grid_info()['column'] - btn.grid_info()['column']) * row_diff:
            return False
    return True

# Function to handle button selection
def select_button(button, selected_buttons):
    selected_buttons.append(button)
    button.config(bg="#E6E6FA")  # Lavender for selected

# Function to reset the game
def reset_game(button_grid, word_labels, correct_words, original_words, name_label, image_label):
    for row in button_grid:
        for btn in row:
            btn.config(bg="#ADD8E6", state="normal")  # Light blue for default
    for lbl in word_labels:
        lbl.config(fg="black", font="Arial 10 bold")
    correct_words.clear()
    correct_words.extend(original_words)
    name_label.config(text="")
    show_image("default", name_label, image_label)

# Function to resize the grid when the window size changes
def resize_grid(event, button_grid, canvas, grid_frame):
    global button_size
    grid_width = min(event.width, event.height)
    button_size = grid_width // len(crossword)
    for row in button_grid:
        for btn in row:
            btn.config(width=button_size//10, height=button_size//23, font=("Arial", button_size//4))
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas_center_x = (canvas.winfo_width() - grid_frame.winfo_width()) // 2
    canvas_center_y = (canvas.winfo_height() - grid_frame.winfo_height()) // 2
    canvas.coords(canvas.create_window((canvas_center_x, canvas_center_y), window=grid_frame, anchor="nw"))

# Function to open the Wikipedia page
def open_wikipedia(event):
    name = event.widget.name
    if name in wikipedia_urls:
        webbrowser.open(wikipedia_urls[name])

def main():
    global crossword, correct_words, original_words

    # Define the crossword puzzle and correct words
    crossword = [
        list("EYPWEYKGXVTEJJOTOICQ"), list("LIKQKZWMGTLOFHSLFHIK"), list("ICHCMWTRNTHYLLPZACWS"),
        list("WMTZKWZAONIWELTRUKAH"), list("HRPXKGGNPBTHNQLEUMLC"), list("INOHVYMKQACAKEIXEPTO"),
        list("TQSLRAORIXRCSCJLQGEO"), list("NEHNYTCIVUABREVXFNRV"), list("EMEOTACGJMAZQENXDIAD"),
        list("YHQENHTMOBKQIKSLXMSR"), list("OLRYIIPWBTTNAGYRNEHO"), list("AUMOWEPAKKDTBOXDTDEF"),
        list("PDHOHSGSECIQEWHBTSWY"), list("RNASEEMORRISCOOKEDHR"), list("OEOMFVMOLBRRYPUMURAN"),
        list("FJAOSOGNIHSOEGIHSARE"), list("SJIYIMOFQHNIKDVQDWTH"), list("MKAORUISHIKAWAEXSDTT"),
        list("PABEZPETERSENGERSEFY"), list("OFQOGUNFHGIAFFMLFDGC")
    ]
    correct_words = [
        "AdamSmith", "CharlesBabbage", "EdwardsDeming", "EliWhitney", "EltonMayo", "FrederickWTaylor",
        "HenryFord", "HenryGantt", "JamesPWomack", "JohnPKotter", "JoshepMJuran", "KaoruIshikawa",
        "KurtLewin", "MorrisCooke", "PeterSenge", "ShigeoShingo", "TaiichiOhno", "WalterAShewhart"
    ]
    original_words = correct_words.copy()

    # Create the main window
    root = tk.Tk()
    root.geometry("1320x750")

    # Create frames and labels
    sidebar_frame = tk.Frame(root, bg="#F0F8FF", relief="solid", bd=0)  # Alice blue for sidebar
    sidebar_frame.grid(row=0, column=0, padx=5, pady=10, sticky="ns")
    canvas = Canvas(root, bg="#F0F8FF")  # Alice blue for canvas background
    canvas.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
    grid_frame = tk.Frame(canvas, bg="#F0F8FF", relief="solid", bd=0)  # Alice blue for grid background
    canvas.create_window((0, 0), window=grid_frame, anchor="nw")
    image_section_frame = tk.Frame(root, bg="#F0F8FF", relief="solid", bd=0)  # Alice blue for image section
    image_section_frame.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
    name_label = tk.Label(image_section_frame, text="", font=("Arial", 15, "bold"), bg="#F0F8FF", fg="black")
    name_label.pack(pady=10)
    image_label = tk.Label(image_section_frame, bg="#F0F8FF")
    image_label.pack(expand=True)

    # Display the default image at the start
    show_image("default", name_label, image_label)

    # Bind the click event to the image_label
    image_label.bind("<Button-1>", open_wikipedia)

    # Configure grid to resize dynamically
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Create the grid of buttons
    button_size = 40
    button_grid = []
    selected_buttons = []
    for i, row in enumerate(crossword):
        button_row = []
        for j, letter in enumerate(row):
            btn = tk.Button(grid_frame, text=letter, width=button_size//10, height=button_size//20, font=("Arial", 14, "bold"),
                            bg="#ADD8E6", relief="flat", bd=0)  # Light blue for default
            btn.grid(row=i, column=j, padx=6, pady=6, ipadx=1.3, ipady=1.3, sticky="nsew")
            btn.bind("<ButtonPress-1>", lambda event, b=btn: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, name_label, image_label))
            btn.bind("<B1-Motion>", lambda event, b=btn: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, name_label, image_label))
            btn.bind("<ButtonRelease-1>", lambda event, b=btn: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, name_label, image_label))
            button_row.append(btn)
        button_grid.append(button_row)

    # Set the window title
    root.title("Chaos Grid")

    # Initialize the word_buttons list
    word_buttons = []

    # Create a frame to contain the word buttons and the reset button
    container_frame = tk.Frame(sidebar_frame, bg="#F0F8FF")
    container_frame.pack(fill=tk.BOTH, expand=True)

    words_frame = tk.Frame(container_frame, bg="#F0F8FF")
    words_frame.pack(fill=tk.BOTH, expand=True)

    for word in correct_words:
        btn = tk.Button(words_frame, text=word, font="Arial 10 bold", bg="#ADD8E6", relief="flat")  # Light blue for default
        btn.pack(fill=tk.X, pady=5, padx=10)
        word_buttons.append(btn)

    # Add reset button at the bottom
    reset_button = tk.Button(container_frame, text="Reset Game", font="Arial 10 bold", bg="red", fg="white", relief="flat", command=lambda: reset_game(button_grid, word_buttons, correct_words, original_words, name_label, image_label))
    reset_button.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

    # Bind the resize function to the canvas resize event
    canvas.bind("<Configure>", lambda event: resize_grid(event, button_grid, canvas, grid_frame))

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()