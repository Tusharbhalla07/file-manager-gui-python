import os
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, simpledialog, scrolledtext
from PIL import Image, ImageTk

# === APP WINDOW ===
app = ttk.Window(themename="cosmo")
app.title("🗂️ Beautiful File Manager")
app.geometry("800x650")
app.resizable(False, False)

# === BACKGROUND IMAGE ===
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((800, 650), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ttk.Label(app, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# === FUNCTIONS ===
def create_file():
    filename = simpledialog.askstring("Create File", "Enter file name:")
    if filename:
        try:
            with open(filename, 'x'):
                messagebox.showinfo("Success", f"File '{filename}' created.")
        except FileExistsError:
            messagebox.showerror("Error", f"'{filename}' already exists.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def view_all_files():
    files = [f for f in os.listdir() if os.path.isfile(f)]
    if files:
        messagebox.showinfo("Files", "\n".join(files))
    else:
        messagebox.showinfo("Empty", "No files found.")

def delete_file():
    filename = filedialog.askopenfilename(title="Select file to delete")
    if filename:
        try:
            os.remove(filename)
            messagebox.showinfo("Deleted", f"{filename} deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def read_file():
    filename = filedialog.askopenfilename(title="Select file to read")
    if filename:
        try:
            with open(filename, 'r') as f:
                content = f.read()
            text_area.delete('1.0', 'end')
            text_area.insert('end', content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def edit_file(mode):
    filename = filedialog.askopenfilename(title="Select file to edit")
    if filename:
        content = simpledialog.askstring("Edit File", "Enter content:")
        if content:
            try:
                with open(filename, mode) as f:
                    f.write("\n" + content + "\n")
                messagebox.showinfo("Updated", "Content saved.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

def rename_file():
    filename = filedialog.askopenfilename(title="Select file to rename")
    if filename:
        new_name = simpledialog.askstring("Rename File", "Enter new file name:")
        if new_name:
            try:
                os.rename(filename, new_name)
                messagebox.showinfo("Renamed", f"Renamed to {new_name}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

def save_as_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filename:
        try:
            content = text_area.get('1.0', 'end')
            with open(filename, 'w') as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Content saved to '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def create_folder():
    foldername = simpledialog.askstring("Create Folder", "Enter folder name:")
    if foldername:
        try:
            os.mkdir(foldername)
            messagebox.showinfo("Success", f"Folder '{foldername}' created.")
        except FileExistsError:
            messagebox.showerror("Error", "Folder already exists.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def open_folder():
    folder_path = filedialog.askdirectory(title="Select a folder")
    if folder_path:
        try:
            files = os.listdir(folder_path)
            if files:
                text_area.delete('1.0', 'end')
                text_area.insert('end', f"Files in {folder_path}:\n\n" + "\n".join(files))
            else:
                messagebox.showinfo("Empty", "The folder is empty.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def show_file_info():
    filename = filedialog.askopenfilename(title="Select file for info")
    if filename:
        try:
            size = os.path.getsize(filename)
            created = time.ctime(os.path.getctime(filename))
            modified = time.ctime(os.path.getmtime(filename))
            info = f"Name: {os.path.basename(filename)}\nSize: {size} bytes\nCreated: {created}\nModified: {modified}"
            messagebox.showinfo("File Info", info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def clear_text_area():
    text_area.delete('1.0', 'end')

def toggle_theme():
    current_theme = app.style.theme.name
    app.style.theme_use("darkly" if current_theme != "darkly" else "cosmo")

def about_app():
    messagebox.showinfo("About", "🗂️ File Manager App\nBuilt by Tushar Bhalla using Python + ttkbootstrap")

# === LOGO + TITLE ===
top_frame = ttk.Frame(app, bootstyle="secondary", padding=10)
top_frame.pack(fill='x')

logo_img = Image.open("logo.png")
logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(logo_img)

ttk.Label(top_frame, image=logo).pack(side='left', padx=10)
ttk.Label(top_frame, text="File Manager App", font=("Segoe UI", 20, "bold")).pack(side='left', padx=10)

# === BUTTONS ===
button_frame = ttk.Frame(app)
button_frame.pack(pady=10)

button_style = {'bootstyle': 'info-outline', 'width': 25}
buttons = []

btn_texts_funcs = [
    ("📝 Create File", create_file),
    ("📄 View Files", view_all_files),
    ("📂 Open File", read_file),
    ("🗑️ Delete File", delete_file),
    ("➕ Append to File", lambda: edit_file('a')),
    ("♻️ Overwrite File", lambda: edit_file('w')),
    ("✏️ Rename File", rename_file),
    ("💾 Save As", save_as_file),
    ("📁 Create Folder", create_folder),
    ("📁 Open Folder", open_folder),
    ("ℹ️ File Info", show_file_info),
    ("🧹 Clear Output", clear_text_area),
    ("🌓 Toggle Theme", toggle_theme),
]

for idx, (text, func) in enumerate(btn_texts_funcs):
    btn = ttk.Button(button_frame, text=text, command=func, **button_style)
    btn.grid(row=idx // 2, column=idx % 2, padx=10, pady=8)
    buttons.append(btn)

# === TEXT AREA ===
text_area = scrolledtext.ScrolledText(app, wrap='word', font=("Consolas", 11), width=95, height=15)
text_area.pack(pady=20, padx=15)

# === MENU BAR ===
menu_bar = ttk.Menu(app)

file_menu = ttk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="📝 New File", command=create_file)
file_menu.add_command(label="📂 Open File", command=read_file)
file_menu.add_command(label="💾 Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="📁 Create Folder", command=create_folder)
file_menu.add_command(label="📁 Open Folder", command=open_folder)
file_menu.add_separator()
file_menu.add_command(label="🚪 Exit", command=app.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = ttk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="ℹ️ About", command=about_app)
menu_bar.add_cascade(label="Help", menu=help_menu)

app.config(menu=menu_bar)

# === BRING TO FRONT ===
top_frame.lift()
button_frame.lift()
text_area.lift()

# === RUN APP ===
app.mainloop()
