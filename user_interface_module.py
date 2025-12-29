import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkfont

class MusicAppGUI:
    def __init__(self, loader, engine):
        self.loader = loader
        self.engine = engine

        self.root = tk.Tk()
        self.root.title("Music Recommendation System")
        self.root.geometry("700x650")
        self.root.configure(bg="#f0f0f5")
        
        # Set custom font
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=11)
        self.button_font = tkfont.Font(family="Helvetica", size=10, weight="bold")
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#f0f0f5")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="Music Recommendation System", 
                font=self.title_font, bg="#f0f0f5", fg="#2c3e50").pack()
        
        # Artist input section
        input_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1, padx=15, pady=15)
        input_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(input_frame, text="Artist Name", font=self.label_font, 
                bg="#ffffff", fg="#34495e").pack(anchor="w", pady=(0, 5))
        
        self.artist_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 11), 
                                     relief="solid", bd=1, highlightthickness=1)
        self.artist_entry.pack(fill="x", pady=(0, 10))
        self.artist_entry.bind("<Return>", lambda e: self.find_similar())
        
        # Similarity method selection
        method_frame = tk.Frame(input_frame, bg="#ffffff")
        method_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(method_frame, text="Similarity Method", font=self.label_font, 
                bg="#ffffff", fg="#34495e").pack(anchor="w", pady=(0, 8))
        
        self.method = tk.StringVar(value="cosine")
        
        # Create a frame for radio buttons with better layout
        radio_frame = tk.Frame(method_frame, bg="#ffffff")
        radio_frame.pack(fill="x")
        
        methods = ["cosine", "euclidean", "pearson"]
        colors = ["#3498db", "#2ecc71", "#9b59b6"]
        
        for i, m in enumerate(methods):
            rb_frame = tk.Frame(radio_frame, bg="#ffffff")
            rb_frame.pack(side="left", padx=(0, 20))
            
            # Custom radio button style
            rb = tk.Radiobutton(rb_frame, text=m.title(), variable=self.method, 
                               value=m, bg="#ffffff", font=self.label_font,
                               activebackground="#ffffff", selectcolor="#ecf0f1")
            rb.pack(side="left")
            
            # Add color indicator
            color_indicator = tk.Frame(rb_frame, width=12, height=12, bg=colors[i])
            color_indicator.pack(side="left", padx=(5, 0))
        
        # Button section
        button_frame = tk.Frame(main_frame, bg="#f0f0f5")
        button_frame.pack(fill="x", pady=(0, 15))
        
        # Style for buttons
        button_style = {
            "font": self.button_font,
            "bd": 0,
            "relief": "flat",
            "padx": 20,
            "pady": 10,
            "cursor": "hand2"
        }
        
        self.similar_btn = tk.Button(button_frame, text="Find Top 5 Similar Artists", 
                                    command=self.find_similar, bg="#3498db", fg="white",
                                    **button_style)
        self.similar_btn.pack(side="left", padx=(0, 10))
        
        self.recommend_btn = tk.Button(button_frame, text="Get Recommendations", 
                                      command=self.recommend, bg="#e74c3c", fg="white",
                                      **button_style)
        self.recommend_btn.pack(side="left")
        
        # Output section
        output_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
        output_frame.pack(fill="both", expand=True)
        
        # Output header
        output_header = tk.Frame(output_frame, bg="#2c3e50", height=30)
        output_header.pack(fill="x")
        
        self.output_title = tk.Label(output_header, text="Results", font=self.button_font, 
                                    bg="#2c3e50", fg="white")
        self.output_title.pack(side="left", padx=10)
        
        # Clear button
        clear_btn = tk.Button(output_header, text="Clear", font=("Helvetica", 9), 
                             command=lambda: self.output.delete(1.0, tk.END),
                             bg="transparent", fg="white", bd=0, cursor="hand2")
        clear_btn.pack(side="right", padx=10)
        
        # Output text area with scrollbar
        text_frame = tk.Frame(output_frame, bg="#ffffff")
        text_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.output = tk.Text(text_frame, height=15, width=60, font=("Courier", 10),
                             yscrollcommand=scrollbar.set, bg="#ecf0f1", relief="flat")
        self.output.pack(fill="both", expand=True)
        
        scrollbar.config(command=self.output.yview)
        
        # Status bar
        self.status_bar = tk.Label(main_frame, text="Ready", bg="#34495e", 
                                  fg="white", anchor="w", font=("Helvetica", 9))
        self.status_bar.pack(fill="x", pady=(10, 0))
        
        # Add some example artists for quick testing
        self.add_examples_dropdown()
        
        # Configure tag colors for output
        self.output.tag_configure("header", foreground="#2c3e50", font=("Helvetica", 11, "bold"))
        self.output.tag_configure("artist", foreground="#2980b9", font=("Courier", 10, "bold"))
        self.output.tag_configure("score", foreground="#27ae60")
        
        # Set focus to entry widget
        self.artist_entry.focus_set()

    def add_examples_dropdown(self):
        """Add a dropdown with example artists for quick testing"""
        example_frame = tk.Frame(self.root, bg="#f0f0f5")
        example_frame.place(relx=1.0, rely=0.1, anchor="ne", x=-20, y=0)
        
        tk.Label(example_frame, text="Try:", bg="#f0f0f5", 
                font=("Helvetica", 9)).pack(side="left", padx=(0, 5))
        
        example_artists = ["The Beatles", "Radiohead", "Taylor Swift", 
                          "Kendrick Lamar", "Daft Punk", "Beyoncé"]
        
        example_var = tk.StringVar(value="Select Artist")
        example_menu = tk.OptionMenu(example_frame, example_var, *example_artists,
                                    command=self.select_example_artist)
        example_menu.config(font=("Helvetica", 9), bg="#ffffff", width=15)
        example_menu.pack()

    def select_example_artist(self, artist):
        """Set the selected example artist in the entry field"""
        self.artist_entry.delete(0, tk.END)
        self.artist_entry.insert(0, artist)
        self.status_bar.config(text=f"Selected: {artist}")

    def find_similar(self):
        artist = self.artist_entry.get().strip()
        if not artist:
            messagebox.showwarning("Missing Information", "Please enter an artist name")
            self.artist_entry.focus_set()
            return

        self.status_bar.config(text=f"Finding similar artists to '{artist}'...")
        self.root.update()
        
        try:
            results = self.engine.find_top_similar_artists(artist, self.method.get())
            
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"Top 5 artists similar to:\n", "header")
            self.output.insert(tk.END, f"{artist}\n\n", "artist")
            
            for i, (a, s) in enumerate(results, 1):
                self.output.insert(tk.END, f"{i}. ", "header")
                self.output.insert(tk.END, f"{a}", "artist")
                self.output.insert(tk.END, f" → {s:.3f}\n", "score")
            
            self.status_bar.config(text=f"Found {len(results)} similar artists for '{artist}'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not find artist: {str(e)}")
            self.status_bar.config(text="Error finding similar artists")

    def recommend(self):
        artist = self.artist_entry.get().strip()
        if not artist:
            messagebox.showwarning("Missing Information", "Please enter an artist name")
            self.artist_entry.focus_set()
            return

        self.status_bar.config(text=f"Getting recommendations based on '{artist}'...")
        self.root.update()
        
        try:
            recs = self.engine.get_artist_recommendations(artist, self.method.get())
            
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"Recommendations based on:\n", "header")
            self.output.insert(tk.END, f"{artist}\n\n", "artist")
            
            for i, (a, s) in enumerate(recs, 1):
                self.output.insert(tk.END, f"{i}. ", "header")
                self.output.insert(tk.END, f"{a}", "artist")
                self.output.insert(tk.END, f" → {s:.3f}\n", "score")
            
            self.status_bar.config(text=f"Found {len(recs)} recommendations based on '{artist}'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not get recommendations: {str(e)}")
            self.status_bar.config(text="Error getting recommendations")

    def start(self):
        self.root.mainloop()