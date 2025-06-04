import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def start_ui(run_detection_callback):
    """
    Creates a Tkinter UI which allows the user to enter a tumor type,
    launches the detection, displays tumor info and shows the image.
    """
    root = tk.Tk()
    root.title("Brain Tumor Detection System")
    root.geometry("600x500")
    
    # Input frame
    input_frame = ttk.Frame(root, padding="10")
    input_frame.pack(fill=tk.X)
    
    ttk.Label(input_frame, text="Enter tumor type (glioma, meningioma, pituitary):").pack(side=tk.LEFT)
    tumor_entry = ttk.Entry(input_frame, width=30)
    tumor_entry.pack(side=tk.LEFT, padx=5)
    
    def on_detect():
        tumor_type = tumor_entry.get()
        if not tumor_type:
            messagebox.showwarning("Input Error", "Please enter a tumor type.")
            return
        
        # Run detection using the provided callback from main.py
        image_path, info = run_detection_callback(tumor_type)
        if image_path is None:
            messagebox.showerror("Detection Error", info)
            return
        
        # Display info in the text widget
        info_text.config(state=tk.NORMAL)
        info_text.delete('1.0', tk.END)
        info_text.insert(tk.END, info)
        info_text.config(state=tk.DISABLED)
        
        # Open a new window to display the image
        display_image(image_path)
    
    detect_button = ttk.Button(input_frame, text="Detect Tumor", command=on_detect)
    detect_button.pack(side=tk.LEFT, padx=5)
    
    # Text widget to display tumor info and detection results
    info_text = tk.Text(root, wrap=tk.WORD, height=15, state=tk.DISABLED)
    info_text.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
    
    def display_image(image_path):
        # Create a new top-level window
        img_window = tk.Toplevel(root)
        img_window.title("Tumor Image")
        # Load the image and display using PIL's ImageTk
        img = Image.open(image_path)
        img = img.resize((400, 300))  # resize as needed
        img_tk = ImageTk.PhotoImage(img)
        
        lbl = tk.Label(img_window, image=img_tk)
        lbl.image = img_tk  # keep reference
        lbl.pack(padx=10, pady=10)
    
    root.mainloop()