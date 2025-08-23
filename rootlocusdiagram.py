# pip install customtkinter control matplotlib numpy
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import control as ctrl
import numpy as np
import ast

def parse_coeffs(text: str):
    """Accept '1 3 2', '1,3,2', or '[1, 3, 2]'."""
    s = text.strip()
    try:
        if s.startswith("["):
            return [float(x) for x in ast.literal_eval(s)]
    except Exception:
        pass
    s = s.replace(",", " ")
    return [float(x) for x in s.split() if x]

def draw_root_locus(ax, G):
    """Plot the root locus using whichever API is available."""
    ax.clear()
    ax.set_title("Root Locus")
    ax.set_xlabel("Real axis")
    ax.set_ylabel("Imag axis")
    ax.grid(True)

    try:
        # Newer API (0.10+)
        rldata = ctrl.root_locus_map(G)
        rldata.plot(ax=ax)
    except Exception:
        # Older API (<=0.9.x)
        rlist, klist = ctrl.root_locus(G, plot=False)  # <-- lowercase 'plot'
        # rlist shape: (len(klist), n_branches)
        for branch in rlist.T:
            ax.plot(np.real(branch), np.imag(branch), '.', markersize=3)

def update_plot(event=None):
    try:
        num = parse_coeffs(num_entry.get())
        den = parse_coeffs(den_entry.get())
        G = ctrl.tf(num, den)

        draw_root_locus(ax, G)

        K = gain_slider.get()
        sys_cl = ctrl.feedback(K * G, 1)
        poles = ctrl.pole(sys_cl)

        ax.plot(np.real(poles), np.imag(poles), 'rx', markersize=10, label=f"Poles (K={K:.2f})")
        ax.legend(loc="best")
        canvas.draw()
        status_label.configure(text=f"Closed-loop poles: {np.round(poles, 4)}")
    except Exception as e:
        status_label.configure(text=f"Error: {e}")

# --- GUI setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Root Locus Analyzer")
app.geometry("900x650")

# Inputs
inputs = ctk.CTkFrame(app)
inputs.pack(pady=10)

ctk.CTkLabel(inputs, text="Numerator:").grid(row=0, column=0, padx=6, pady=6, sticky="e")
num_entry = ctk.CTkEntry(inputs, width=300)
num_entry.grid(row=0, column=1, padx=6, pady=6)

ctk.CTkLabel(inputs, text="Denominator:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
den_entry = ctk.CTkEntry(inputs, width=300)
den_entry.grid(row=1, column=1, padx=6, pady=6)

# Useful defaults (something that actually moves with K)
num_entry.insert(0, "1")          # G(s) = 1 / (s^2 + 3s + 2)
den_entry.insert(0, "1 3 2")

# Gain slider
ctk.CTkLabel(app, text="Gain K").pack()
gain_slider = ctk.CTkSlider(app, from_=0.0, to=100.0, number_of_steps=100, command=update_plot, width=500)
gain_slider.set(1.0)
gain_slider.pack(pady=6)

# Matplotlib canvas
fig, ax = plt.subplots(figsize=(7,4))
canvas = FigureCanvasTkAgg(fig, master=app)
canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

# Buttons/status
btns = ctk.CTkFrame(app)
btns.pack(pady=6)
ctk.CTkButton(btns, text="Plot / Refresh", command=update_plot).grid(row=0, column=0, padx=6)
status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=6)

update_plot()  # initial plot
app.mainloop()