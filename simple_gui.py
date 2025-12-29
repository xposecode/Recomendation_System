import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

class SimpleMusicAppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Recommendation System - Test")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f5")
        
        # Header
        tk.Label(self.root, text="Music Recommendation System", 
                font=("Helvetica", 16, "bold"), bg="#f0f0f5", fg="#2c3e50").pack(pady=20)
        
        # Artist input
        tk.Label(self.root, text="Artist Name", font=("Helvetica", 11), 
                bg="#f0f0f5", fg="#34495e").pack()
        
        self.artist_entry = tk.Entry(self.root, width=40, font=("Helvetica", 11))
        self.artist_entry.pack(pady=10)
        
        # Method selection
        self.method = tk.StringVar(value="cosine")
        tk.Label(self.root, text="Similarity Method", font=("Helvetica", 11), 
                bg="#f0f0f5", fg="#34495e").pack()
        
        for method in ["cosine", "euclidean", "pearson"]:
            tk.Radiobutton(self.root, text=method.title(), variable=self.method, 
                          value=method, bg="#f0f0f5", font=("Helvetica", 10)).pack()
        
        # Buttons
        tk.Button(self.root, text="Find Similar Artists", command=self.find_similar,
                 bg="#3498db", fg="white", font=("Helvetica", 10, "bold"),
                 padx=20, pady=10).pack(pady=20)
        
        # Output area
        tk.Label(self.root, text="Results:", font=("Helvetica", 11, "bold"), 
                bg="#f0f0f5", fg="#2c3e50").pack()
        
        self.output = tk.Text(self.root, height=10, width=50)
        self.output.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(self.root, text="Ready", bg="#34495e", 
                                    fg="white", anchor="w")
        self.status_label.pack(fill="x", pady=(10, 0))
        
        print("GUI initialized successfully!")
    
    def find_similar(self):
        artist = self.artist_entry.get().strip()
        if not artist:
            messagebox.showwarning("Error", "Please enter an artist name")
            return
        
        self.status_label.config(text=f"Searching for similar artists to '{artist}'...")
        
        # Simulate results
        import random
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Similar artists to '{artist}':\n\n")
        
        fake_artists = ["Artist A", "Artist B", "Artist C", "Artist D", "Artist E"]
        for i, fake_artist in enumerate(fake_artists, 1):
            score = random.uniform(0.7, 0.99)
            self.output.insert(tk.END, f"{i}. {fake_artist} → {score:.3f}\n")
        
        self.status_label.config(text=f"Found 5 similar artists for '{artist}'")
    
    def start(self):
        print("Starting mainloop...")
        self.root.mainloop()

def main():
    print("Starting simple test GUI...")
    app = SimpleMusicAppGUI()
    app.start()

if __name__ == "__main__":
    main()