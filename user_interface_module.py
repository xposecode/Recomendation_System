"""
user_interface_module.py
File: Graphical User Interface for Music Recommendation System
Author: [Your Name]
Student ID: [Your ID]
Course: [Course Name]
"""

import tkinter as tk
from tkinter import messagebox
import pandas as pd

class MusicAppGUI:
    """Main GUI class for the music recommendation system"""
    
    def __init__(self, data_handler, similarity_engine):
        self.data = data_handler
        self.engine = similarity_engine
        
        self.main_window = tk.Tk()
        self.main_window.title("Music Recommendation System")
        self.main_window.geometry("900x800")
        self.main_window.configure(bg='#F0F0F0')
        
        self.method_choice = tk.StringVar(value="cosine")
        self.comparison_type = tk.StringVar(value="artist")
        self.artist_name = tk.StringVar()
        
        self.setup_interface()
        self.display_instructions()
    
    def display_instructions(self):
        """Show welcome message and instructions"""
        welcome_msg = """🎵 MUSIC RECOMMENDATION SYSTEM 🎵

ASSIGNMENT FUNCTIONS:
1. Find Top 5 Similar Artists
   - Uses cosine, euclidean, or pearson similarity
   - Only shows artists with similarity > 0.8
   - Returns exactly 5 artists

2. Get Artist Recommendations
   - Randomly selects 10 similar artists
   - Weighted by similarity scores
   - Like Spotify recommendations

Instructions:
1. Select calculation method (NO MANHATTAN)
2. Enter artist name
3. Click desired function button

Available Methods:
• Cosine Similarity
• Euclidean Distance
• Pearson Correlation

Sample Artists:"""
        
        artists = self.data.get_all_artists()
        if artists:
            for i in range(min(8, len(artists))):
                welcome_msg += f"\n   • {artists[i]}"
        
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(1.0, welcome_msg)
    
    def setup_interface(self):
        """Create all GUI elements"""
        main_frame = tk.Frame(self.main_window, bg='#F0F0F0')
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            main_frame,
            text="Music Recommendation System",
            font=("Arial", 18, "bold"),
            bg='#F0F0F0',
            fg='#0066CC'
        )
        title_label.pack(pady=(0, 20))
        
        # Method selection
        method_frame = tk.LabelFrame(
            main_frame,
            text="Select Similarity Method (NO MANHATTAN)",
            font=("Arial", 11, "bold"),
            bg='#F0F0F0',
            padx=10,
            pady=10
        )
        method_frame.pack(fill=tk.X, pady=(0, 15))
        
        method_buttons_frame = tk.Frame(method_frame, bg='#F0F0F0')
        method_buttons_frame.pack()
        
        methods = [
            ("Cosine Similarity", "cosine"),
            ("Euclidean Distance", "euclidean"),
            ("Pearson Correlation", "pearson")
        ]
        
        for i, (label_text, method_value) in enumerate(methods):
            rb = tk.Radiobutton(
                method_buttons_frame,
                text=label_text,
                variable=self.method_choice,
                value=method_value,
                bg='#F0F0F0',
                font=("Arial", 10)
            )
            rb.pack(side=tk.LEFT, padx=15)
        
        # Artist input
        input_frame = tk.LabelFrame(
            main_frame,
            text="Enter Artist Name",
            font=("Arial", 11, "bold"),
            bg='#F0F0F0',
            padx=10,
            pady=10
        )
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            input_frame,
            text="Artist Name:",
            font=("Arial", 10, "bold"),
            bg='#F0F0F0'
        ).pack(side=tk.LEFT, padx=5)
        
        self.artist_entry = tk.Entry(
            input_frame,
            textvariable=self.artist_name,
            width=40,
            font=("Arial", 10)
        )
        self.artist_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            input_frame,
            text="Example",
            command=self.fill_example,
            width=10,
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        # Assignment Task Buttons
        task_frame = tk.LabelFrame(
            main_frame,
            text="Calculations",
            font=("Arial", 11, "bold"),
            bg='#F0F0F0',
            padx=10,
            pady=10
        )
        task_frame.pack(fill=tk.X, pady=(0, 20))
        
        button_frame = tk.Frame(task_frame, bg='#F0F0F0')
        button_frame.pack()
        
        # Task 1 Button
        task1_btn = tk.Button(
            button_frame,
            text="Find Top 5 Similar Artists",
            command=self.task1_top_similar,
            font=("Arial", 10, "bold"),
            bg='#4CAF50',
            fg='white',
            width=30,
            height=2
        )
        task1_btn.grid(row=0, column=0, padx=10, pady=5)
        
        # Task 2 Button
        task2_btn = tk.Button(
            button_frame,
            text="Get Artist Recommendations",
            command=self.task2_recommendations,
            font=("Arial", 10, "bold"),
            bg='#2196F3',
            fg='white',
            width=30,
            height=2
        )
        task2_btn.grid(row=0, column=1, padx=10, pady=5)
        
        # Control Buttons
        control_frame = tk.Frame(task_frame, bg='#F0F0F0')
        control_frame.pack(pady=(10, 0))
        
        tk.Button(
            control_frame,
            text="Clear Results",
            command=self.clear_results,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Show Artist Features",
            command=self.show_artist_features,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Exit",
            command=self.main_window.quit,
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Results area
        results_frame = tk.LabelFrame(
            main_frame,
            text="Results",
            font=("Arial", 11, "bold"),
            bg='#F0F0F0',
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_area = tk.Text(
            results_frame,
            width=90,
            height=25,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg='white',
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.output_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(results_frame, command=self.output_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_area.config(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_text = tk.StringVar(value="Ready - Enter artist name and select task")
        status_bar = tk.Label(
            main_frame,
            textvariable=self.status_text,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9),
            bg='#E0E0E0'
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def fill_example(self):
        """Fill input with example artist"""
        artists = self.data.get_all_artists()
        if artists:
            self.artist_name.set(artists[0])
    
    def task1_top_similar(self):
        """Task 1: Find top 5 similar artists"""
        artist = self.artist_name.get().strip()
        
        if not artist:
            messagebox.showwarning("Input Required", "Please enter an artist name")
            return
        
        try:
            self.status_text.set("Finding top 5 similar artists...")
            self.main_window.update()
            
            method = self.method_choice.get()
            
            results = self.engine.find_top_similar_artists(artist, method, 5)
            
            output = "=" * 70 + "\n"
            output += "TASK 1: TOP 5 SIMILAR ARTISTS\n"
            output += "=" * 70 + "\n\n"
            output += f"Target Artist: {artist}\n"
            output += f"Method: {method.upper()}\n"
            output += f"Threshold: Similarity > 0.8\n\n"
            
            if results:
                output += "Top 5 Similar Artists:\n"
                output += "-" * 40 + "\n"
                
                for i, (artist_name, similarity) in enumerate(results, 1):
                    output += f"{i}. {artist_name}\n"
                    output += f"   Similarity Score: {similarity:.4f}\n"
                    output += f"   Interpretation: "
                    
                    if similarity > 0.9:
                        output += "Very High Similarity\n"
                    elif similarity > 0.8:
                        output += "High Similarity\n"
                    else:
                        output += "Moderate Similarity\n"
                    
                    output += "\n"
                
                output += f"Total found: {len(results)} artists\n"
            else:
                output += "No similar artists found with similarity > 0.8\n"
                output += "Try a different artist or method\n"
            
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(1.0, output)
            self.status_text.set(f"Task 1 complete: Found {len(results)} similar artists")
            
        except Exception as error:
            messagebox.showerror("Error", f"Error in Task 1:\n{error}")
            self.status_text.set("Error occurred")
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(1.0, f"Error details:\n{str(error)}")
    
    def task2_recommendations(self):
        """Task 2: Get artist recommendations"""
        artist = self.artist_name.get().strip()
        
        if not artist:
            messagebox.showwarning("Input Required", "Please enter an artist name")
            return
        
        try:
            self.status_text.set("Generating recommendations...")
            self.main_window.update()
            
            method = self.method_choice.get()
            
            recommendations = self.engine.get_artist_recommendations(artist, method, 10)
            
            output = "=" * 70 + "\n"
            output += "TASK 2: ARTIST RECOMMENDATIONS\n"
            output += "=" * 70 + "\n\n"
            output += f"Target Artist: {artist}\n"
            output += f"Method: {method.upper()}\n"
            output += f"Number of recommendations: 10 (like Spotify)\n\n"
            
            if recommendations:
                output += "Recommended Artists:\n"
                output += "-" * 40 + "\n"
                
                for i, (artist_name, similarity) in enumerate(recommendations, 1):
                    output += f"{i}. {artist_name}\n"
                    output += f"   Similarity Score: {similarity:.4f}\n"
                    
                    # Add emoji based on similarity
                    if similarity > 0.9:
                        output += "   Match: 🔥 Perfect Match!\n"
                    elif similarity > 0.7:
                        output += "   Match: ⭐ Great Match\n"
                    elif similarity > 0.5:
                        output += "   Match: ✓ Good Match\n"
                    else:
                        output += "   Match: • Decent Match\n"
                    
                    output += "\n"
                
                # Calculate statistics
                scores = [score for _, score in recommendations]
                avg_score = sum(scores) / len(scores) if scores else 0
                
                output += f"\nStatistics:\n"
                output += f"- Average similarity: {avg_score:.4f}\n"
                output += f"- Highest similarity: {max(scores):.4f}\n"
                output += f"- Lowest similarity: {min(scores):.4f}\n"
                output += f"- Total recommendations: {len(recommendations)}\n"
                
            else:
                output += "No recommendations found\n"
                output += "The artist may not have enough similar artists\n"
            
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(1.0, output)
            self.status_text.set(f"Task 2 complete: Generated {len(recommendations)} recommendations")
            
        except Exception as error:
            messagebox.showerror("Error", f"Error in Task 2:\n{error}")
            self.status_text.set("Error occurred")
    
    def show_artist_features(self):
        """Show artist features dataframe"""
        try:
            df = self.data.get_artist_features_dataframe()
            
            if df is None:
                messagebox.showinfo("No Data", "Artist features dataframe not available")
                return
            
            output = "=" * 70 + "\n"
            output += "ARTIST FEATURES DATAFRAME\n"
            output += "=" * 70 + "\n\n"
            output += f"Shape: {df.shape[0]} artists × {df.shape[1]} features\n\n"
            output += "First 10 artists:\n"
            output += "-" * 70 + "\n"
            
            # Display first 10 rows
            for i, row in df.head(10).iterrows():
                output += f"{i+1}. {row['Artist_name']}\n"
                output += f"   Features: "
                features = []
                for col in df.columns:
                    if col != 'Artist_name':
                        features.append(f"{col}: {row[col]:.3f}")
                output += ", ".join(features[:3]) + "...\n\n"
            
            output += f"\nFeatures calculated: {len(df.columns) - 1}\n"
            output += f"Saved to: artist_features.csv\n"
            
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(1.0, output)
            self.status_text.set("Showing artist features dataframe")
            
        except Exception as error:
            messagebox.showerror("Error", f"Error showing features:\n{error}")
    
    def clear_results(self):
        """Clear all results"""
        self.output_area.delete(1.0, tk.END)
        self.artist_name.set("")
        self.status_text.set("Cleared - Ready for new input")
        self.display_instructions()
    
    def start(self):
        """Start the GUI application"""
        self.main_window.mainloop()