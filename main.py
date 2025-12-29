import tkinter as tk
from tkinter import ttk, messagebox
import random

class MusicAppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Recommendation System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header
        header_label = tk.Label(
            main_frame,
            text="🎵 Music Recommendation System",
            font=("Arial", 24, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        # Left Panel - Input and Controls
        left_panel = ttk.Frame(main_frame, padding="10")
        left_panel.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E), padx=(0, 20))
        
        # Search Section
        search_frame = ttk.LabelFrame(left_panel, text="Search", padding="15")
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Artist/Track Selection
        self.search_type = tk.StringVar(value="artist")
        
        ttk.Radiobutton(
            search_frame,
            text="Artist",
            variable=self.search_type,
            value="artist",
            command=self.on_search_type_change
        ).grid(row=0, column=0, padx=(0, 15))
        
        ttk.Radiobutton(
            search_frame,
            text="Track",
            variable=self.search_type,
            value="track",
            command=self.on_search_type_change
        ).grid(row=0, column=1)
        
        # Name Input
        ttk.Label(search_frame, text="Name:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            search_frame,
            textvariable=self.name_var,
            width=30,
            font=("Arial", 11)
        )
        self.name_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Auto-complete list (sample data)
        self.artists_list = [
            "The Beatles", "Radiohead", "Taylor Swift", "Kendrick Lamar",
            "Daft Punk", "Beyoncé", "Coldplay", "Drake", "Ed Sheeran",
            "Ariana Grande", "Billie Eilish", "The Weeknd", "Post Malone",
            "Lana Del Rey", "Bruno Mars", "Lady Gaga", "Kanye West",
            "Rihanna", "Eminem", "Imagine Dragons"
        ]
        
        self.tracks_list = [
            "Blinding Lights", "Shape of You", "Bad Guy", "Dance Monkey",
            "Someone You Loved", "Sunflower", "Perfect", "Believer",
            "Lovely", "Thinking Out Loud", "Rolling in the Deep",
            "Uptown Funk", "Happy", "Despacito", "Old Town Road"
        ]
        
        # Similarity Method
        ttk.Label(search_frame, text="Similarity Method:", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(20, 5)
        )
        
        self.method_var = tk.StringVar(value="cosine")
        
        methods_frame = ttk.Frame(search_frame)
        methods_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        methods = [("Cosine", "cosine"), ("Euclidean", "euclidean"), ("Pearson", "pearson")]
        for i, (text, value) in enumerate(methods):
            ttk.Radiobutton(
                methods_frame,
                text=text,
                variable=self.method_var,
                value=value
            ).grid(row=0, column=i, padx=(0, 15))
        
        # Buttons
        buttons_frame = ttk.Frame(search_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        
        ttk.Button(
            buttons_frame,
            text="Find Similar Artists",
            command=self.find_similar_artists,
            width=20
        ).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="Find Similar Tracks",
            command=self.find_similar_tracks,
            width=20
        ).grid(row=0, column=1)
        
        # Right Panel - Results
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        # Tab 1: Similar Artists
        self.artists_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.artists_frame, text="Similar Artists")
        
        # Artists Results
        artists_header = tk.Label(
            self.artists_frame,
            text="Top Similar Artists",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        artists_header.pack(pady=(10, 15))
        
        # Treeview for artists
        self.artists_tree = ttk.Treeview(
            self.artists_frame,
            columns=("Rank", "Artist", "Similarity", "Genre"),
            show="headings",
            height=12
        )
        
        # Configure columns
        self.artists_tree.heading("Rank", text="Rank")
        self.artists_tree.heading("Artist", text="Artist")
        self.artists_tree.heading("Similarity", text="Similarity Score")
        self.artists_tree.heading("Genre", text="Genre")
        
        self.artists_tree.column("Rank", width=50, anchor=tk.CENTER)
        self.artists_tree.column("Artist", width=200)
        self.artists_tree.column("Similarity", width=120, anchor=tk.CENTER)
        self.artists_tree.column("Genre", width=100)
        
        # Scrollbar
        artists_scroll = ttk.Scrollbar(
            self.artists_frame,
            orient="vertical",
            command=self.artists_tree.yview
        )
        self.artists_tree.configure(yscrollcommand=artists_scroll.set)
        
        self.artists_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        artists_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tab 2: Similar Tracks
        self.tracks_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tracks_frame, text="Similar Tracks")
        
        # Tracks Results
        tracks_header = tk.Label(
            self.tracks_frame,
            text="Recommended Tracks",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        tracks_header.pack(pady=(10, 15))
        
        # Treeview for tracks
        self.tracks_tree = ttk.Treeview(
            self.tracks_frame,
            columns=("Rank", "Track", "Artist", "Similarity", "Duration"),
            show="headings",
            height=12
        )
        
        # Configure columns
        self.tracks_tree.heading("Rank", text="Rank")
        self.tracks_tree.heading("Track", text="Track Name")
        self.tracks_tree.heading("Artist", text="Artist")
        self.tracks_tree.heading("Similarity", text="Similarity Score")
        self.tracks_tree.heading("Duration", text="Duration")
        
        self.tracks_tree.column("Rank", width=50, anchor=tk.CENTER)
        self.tracks_tree.column("Track", width=200)
        self.tracks_tree.column("Artist", width=150)
        self.tracks_tree.column("Similarity", width=120, anchor=tk.CENTER)
        self.tracks_tree.column("Duration", width=80, anchor=tk.CENTER)
        
        # Scrollbar
        tracks_scroll = ttk.Scrollbar(
            self.tracks_frame,
            orient="vertical",
            command=self.tracks_tree.yview
        )
        self.tracks_tree.configure(yscrollcommand=tracks_scroll.set)
        
        self.tracks_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        tracks_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tab 3: Details
        self.details_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.details_frame, text="Details")
        
        # Details text
        self.details_text = tk.Text(
            self.details_frame,
            height=20,
            width=60,
            font=("Arial", 10),
            wrap=tk.WORD,
            bg="white",
            relief=tk.FLAT
        )
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Bind Enter key
        self.name_entry.bind("<Return>", lambda e: self.on_enter_pressed())
        
        # Set initial placeholder
        self.update_placeholder()
        
    def on_search_type_change(self):
        self.update_placeholder()
        
    def update_placeholder(self):
        search_type = self.search_type.get()
        if search_type == "artist":
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, "Enter artist name...")
            self.name_entry.config(foreground="grey")
        else:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, "Enter track name...")
            self.name_entry.config(foreground="grey")
            
        # Bind focus events for placeholder
        self.name_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.name_entry.bind("<FocusOut>", self.on_entry_focus_out)
        
    def on_entry_focus_in(self, event):
        if self.name_entry.get() in ["Enter artist name...", "Enter track name..."]:
            self.name_entry.delete(0, tk.END)
            self.name_entry.config(foreground="black")
            
    def on_entry_focus_out(self, event):
        if not self.name_entry.get():
            self.update_placeholder()
            
    def on_enter_pressed(self):
        search_type = self.search_type.get()
        if search_type == "artist":
            self.find_similar_artists()
        else:
            self.find_similar_tracks()
            
    def find_similar_artists(self):
        query = self.name_var.get().strip()
        if not query or query in ["Enter artist name...", "Enter track name..."]:
            messagebox.showwarning("Input Required", "Please enter an artist name.")
            return
            
        method = self.method_var.get()
        self.status_var.set(f"Finding artists similar to '{query}' using {method}...")
        
        # Clear previous results
        for item in self.artists_tree.get_children():
            self.artists_tree.delete(item)
            
        # Generate fake data (replace with your actual similarity calculations)
        genres = ["Rock", "Pop", "Hip-Hop", "Electronic", "R&B", "Jazz", "Country"]
        
        for i in range(1, 11):
            artist = f"Similar Artist {i}"
            similarity = round(random.uniform(0.7, 0.99), 3)
            genre = random.choice(genres)
            
            # Color code based on similarity
            tag = ""
            if similarity > 0.9:
                tag = "high"
            elif similarity > 0.8:
                tag = "medium"
            else:
                tag = "low"
                
            self.artists_tree.insert("", tk.END, values=(i, artist, similarity, genre), tags=(tag,))
            
        # Configure tags for colors
        self.artists_tree.tag_configure("high", foreground="green")
        self.artists_tree.tag_configure("medium", foreground="orange")
        self.artists_tree.tag_configure("low", foreground="red")
        
        # Update details
        self.update_details(f"Found 10 artists similar to '{query}'")
        
        # Switch to artists tab
        self.notebook.select(0)
        self.status_var.set(f"Found 10 artists similar to '{query}'")
        
    def find_similar_tracks(self):
        query = self.name_var.get().strip()
        if not query or query in ["Enter artist name...", "Enter track name..."]:
            messagebox.showwarning("Input Required", "Please enter a track name.")
            return
            
        method = self.method_var.get()
        self.status_var.set(f"Finding tracks similar to '{query}' using {method}...")
        
        # Clear previous results
        for item in self.tracks_tree.get_children():
            self.tracks_tree.delete(item)
            
        # Generate fake data (replace with your actual similarity calculations)
        artists = ["Artist A", "Artist B", "Artist C", "Artist D", "Artist E",
                  "Artist F", "Artist G", "Artist H", "Artist I", "Artist J"]
        
        for i in range(1, 11):
            track = f"Recommended Track {i}"
            artist = random.choice(artists)
            similarity = round(random.uniform(0.65, 0.98), 3)
            duration = f"{random.randint(2, 5)}:{random.randint(10, 59):02d}"
            
            # Color code based on similarity
            tag = ""
            if similarity > 0.9:
                tag = "high"
            elif similarity > 0.8:
                tag = "medium"
            else:
                tag = "low"
                
            self.tracks_tree.insert("", tk.END, values=(i, track, artist, similarity, duration), tags=(tag,))
            
        # Configure tags for colors
        self.tracks_tree.tag_configure("high", foreground="green")
        self.tracks_tree.tag_configure("medium", foreground="orange")
        self.tracks_tree.tag_configure("low", foreground="red")
        
        # Update details
        self.update_details(f"Found 10 tracks similar to '{query}'")
        
        # Switch to tracks tab
        self.notebook.select(1)
        self.status_var.set(f"Found 10 tracks similar to '{query}'")
        
    def update_details(self, message):
        self.details_text.delete(1.0, tk.END)
        
        details = f"""
{message}

Similarity Method: {self.method_var.get().title()}
Query: {self.name_var.get()}

RECOMMENDATION DETAILS:
=======================

Based on audio features analysis:
• Danceability: High
• Energy: Moderate
• Tempo: {random.randint(100, 140)} BPM
• Valence: {random.choice(['Positive', 'Neutral', 'Negative'])}
• Acousticness: {random.randint(20, 80)}%

Top matches found using collaborative filtering
and content-based filtering techniques.

Note: These are demo results. Connect to your
music database for real recommendations.
"""
        self.details_text.insert(1.0, details)
        
    def run(self):
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

def main():
    app = MusicAppGUI()
    app.run()

if __name__ == "__main__":
    main()