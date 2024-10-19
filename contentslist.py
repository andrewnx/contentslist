import tkinter as tk
from tkinter import filedialog, scrolledtext
import os

def list_files(startpath):
    text_output.delete(1.0, tk.END)  # Clear existing text
    omit_folders = [
        'node_modules', '.git', 'vendor', '.idea', '.vscode',
        'storage/logs', 'storage/framework', 'bootstrap/cache',
        'public', '.phpunit.cache', 'tests'
    ]
    for root, dirs, files in os.walk(startpath):
        # Remove directories to be omitted
        dirs[:] = [d for d in dirs if d not in omit_folders and d not in ['.env']]
        
        # Check if the current directory is a subdirectory of any omitted folder
        if any(omit_folder in root.split(os.sep) for omit_folder in omit_folders):
            continue
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        text_output.insert(tk.END, '{}{}/\n'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f != '.env':
                text_output.insert(tk.END, '{}{}\n'.format(subindent, f))

def on_button_click():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        list_files(folder_selected)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(text_output.get(1.0, tk.END))

root = tk.Tk()
root.title("Folder Contents Lister")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

browse_button = tk.Button(frame, text="Select Project Folder", command=on_button_click)
browse_button.pack()

copy_button = tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack()

text_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
text_output.pack(padx=10, pady=10)

root.mainloop()
