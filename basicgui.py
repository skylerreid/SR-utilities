import customtkinter as ctk
import pandas as pd

def load_csv():
    filepath = entry.get().strip()
    try:
        df = pd.read_csv(filepath)
        preview = df.head().to_string()  # get first 5 rows as text
        result_label.configure(text=preview)
    except Exception as e:
        result_label.configure(text=f"Error: {e}")

# --- Setup GUI ---
ctk.set_appearance_mode("dark")   # "light" / "dark" / "system"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CSV Previewer")
app.geometry("800x600")

# File path input
entry_label = ctk.CTkLabel(app, text="CSV File Path:")
entry_label.pack(pady=5)

entry = ctk.CTkEntry(app, placeholder_text="Enter path to CSV file", width=400)
entry.pack(pady=5)

# Load button
button = ctk.CTkButton(app, text="Load CSV", command=load_csv)
button.pack(pady=10)

# Result display (multi-line text)
result_label = ctk.CTkLabel(app, text="", justify="left")
result_label.pack(pady=10, padx=20)

app.mainloop()
