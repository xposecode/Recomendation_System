"""
user_interface_module.py - GUI for the recommendation engine
"""

import tkinter as tk
from tkinter import ttk, messagebox

class RecommendationGUI:
    """GUI for the music recommendation engine"""
    
    def __init__(self, data_loader, similarity_calculator):
        self.loader = data_loader
        self.calculator = similarity_calculator
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Music Recommendation Engine")
        self.root.geometry("800x700")
        
        # Variables
        self.metric_var = tk.StringVar(value="cosine")
        self.type_var = tk.StringVar(value="artist")
        self.input1_var = tk.StringVar()
        self.input2_var = tk.StringVar()
        
        # Create widgets
        self.create_widgets()
        
        # Show help message
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Show welcome message in results area"""
        welcome_text = """🎵 WELCOME TO MUSIC RECOMMENDATION ENGINE 🎵

HOW TO USE:
1. Select a similarity metric (Cosine, Euclidean, Pearson, Manhattan)
2. Choose whether to compare Artists or Tracks
3. Enter item names in the input fields
4. Click "Calculate Similarity" or "Get Recommendations"

EXAMPLE ARTISTS IN DATABASE:
"""
        # Add some sample artists
        artists = self.loader.get_all_artists()
        if artists:
            for i, artist in enumerate(artists[:8], 1):
                welcome_text += f"   • {artist}\n"
        
        welcome_text += "\nEXAMPLE USAGE:"
        welcome_text += "\n• For Artists: Enter 'Artist 0' and 'Artist 1'"
        welcome_text += "\n• Click 'Calculate Similarity'"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, welcome_text)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(
            main_frame,
            text="🎵 MUSIC RECOMMENDATION ENGINE 🎵",
            font=("Arial", 18, "bold"),
            foreground="#2E86AB"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Similarity metric selection
        ttk.Label(main_frame, text="Similarity Metric:", 
                 font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        
        metric_frame = ttk.Frame(main_frame)
        metric_frame.grid(row=1, column=1, sticky=tk.W)
        
        metrics = [
            ("Cosine", "cosine"),
            ("Euclidean", "euclidean"),
            ("Pearson", "pearson"),
            ("Manhattan", "manhattan")
        ]
        
        for i, (text, value) in enumerate(metrics):
            rb = ttk.Radiobutton(
                metric_frame,
                text=text,
                variable=self.metric_var,
                value=value
            )
            rb.grid(row=0, column=i, padx=10)
        
        # Item type selection
        ttk.Label(main_frame, text="Compare:", 
                 font=("Arial", 11, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=2, column=1, sticky=tk.W)
        
        types = [("Artists", "artist"), ("Tracks", "track")]
        for i, (text, value) in enumerate(types):
            rb = ttk.Radiobutton(
                type_frame,
                text=text,
                variable=self.type_var,
                value=value,
                command=self.on_type_change
            )
            rb.grid(row=0, column=i, padx=20)
        
        # Input fields
        self.create_input_fields(main_frame)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Style the buttons
        style = ttk.Style()
        style.configure('Success.TButton', font=('Arial', 10, 'bold'))
        style.configure('Info.TButton', font=('Arial', 10))
        
        ttk.Button(
            button_frame,
            text="🔍 Calculate Similarity",
            command=self.calculate_similarity,
            width=22,
            style='Success.TButton'
        ).grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="💡 Get Recommendations",
            command=self.get_recommendations,
            width=22,
            style='Info.TButton'
        ).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_results,
            width=22
        ).grid(row=1, column=0, padx=5, pady=5)
        
        ttk.Button(
            button_frame,
            text="🚪 Quit",
            command=self.root.quit,
            width=22
        ).grid(row=1, column=1, padx=5, pady=5)
        
        # Results area
        results_label = ttk.Label(main_frame, text="Results:", 
                                 font=("Arial", 12, "bold"))
        results_label.grid(row=6, column=0, sticky=tk.W, pady=(10, 5))
        
        # Add help button
        ttk.Button(
            main_frame,
            text="❓ Help",
            command=self.show_help,
            width=10
        ).grid(row=6, column=1, sticky=tk.E, pady=(10, 5))
        
        # Text widget for results
        self.results_text = tk.Text(
            main_frame,
            width=80,
            height=20,
            wrap=tk.WORD,
            font=("Courier New", 10),
            bg="#f8f9fa",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.results_text.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame,
            orient=tk.VERTICAL,
            command=self.results_text.yview
        )
        scrollbar.grid(row=7, column=2, sticky=(tk.N, tk.S))
        self.results_text['yscrollcommand'] = scrollbar.set
        
        # Status bar
        self.status_var = tk.StringVar(value="✅ Ready - Enter items and click a button")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        status_bar.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_input_fields(self, parent):
        """Create input fields"""
        # Item 1
        ttk.Label(parent, text="Item 1:", 
                 font=("Arial", 11)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        
        self.input1_entry = ttk.Entry(
            parent,
            textvariable=self.input1_var,
            width=50,
            font=("Arial", 10)
        )
        self.input1_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Add sample button for item 1
        ttk.Button(
            parent,
            text="Sample",
            command=lambda: self.input1_var.set(self.get_sample_item()),
            width=8
        ).grid(row=3, column=1, sticky=tk.E, padx=5)
        
        # Item 2
        ttk.Label(parent, text="Item 2 (for comparison):", 
                 font=("Arial", 11)).grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        
        self.input2_entry = ttk.Entry(
            parent,
            textvariable=self.input2_var,
            width=50,
            font=("Arial", 10)
        )
        self.input2_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Add sample button for item 2
        ttk.Button(
            parent,
            text="Sample",
            command=lambda: self.input2_var.set(self.get_sample_item()),
            width=8
        ).grid(row=4, column=1, sticky=tk.E, padx=5)
    
    def get_sample_item(self):
        """Get a sample item based on selected type"""
        item_type = self.type_var.get()
        
        if item_type == 'artist':
            artists = self.loader.get_all_artists()
            if artists:
                # Return a different artist than what's already in the fields
                current_items = [self.input1_var.get(), self.input2_var.get()]
                for artist in artists:
                    if artist not in current_items:
                        return artist
                return artists[0]
        else:
            tracks = self.loader.get_all_tracks()
            if tracks:
                return tracks[0]['name']
        
        return "Sample Item"
    
    def on_type_change(self):
        """Handle item type change"""
        # Clear inputs when type changes
        self.input1_var.set("")
        self.input2_var.set("")
        self.status_var.set(f"Switched to {self.type_var.get()} mode")
    
    def calculate_similarity(self):
        """Calculate similarity between two items"""
        item1 = self.input1_var.get().strip()
        item2 = self.input2_var.get().strip()
        
        if not item1 or not item2:
            messagebox.showwarning("Input Required", 
                                 "Please enter both items to compare")
            return
        
        try:
            self.status_var.set("🔄 Calculating similarity...")
            self.root.update()  # Update GUI to show status
            
            metric = self.metric_var.get()
            item_type = self.type_var.get()
            
            # Calculate similarity
            similarity = self.calculator.compute_similarity(
                item1, item2, item_type, metric
            )
            
            if similarity == 0:
                messagebox.showinfo("No Match", 
                                  f"Could not find '{item1}' or '{item2}'\n"
                                  f"Try using sample artists from the list.")
                self.status_var.set("❌ Items not found")
                return
            
            # Get top 5 similar for each
            top5_1 = self.calculator.get_top_similar(item1, item_type, metric, 5)
            top5_2 = self.calculator.get_top_similar(item2, item_type, metric, 5)
            
            # Display results
            result_text = "=" * 70 + "\n"
            result_text += "SIMILARITY RESULTS\n"
            result_text += "=" * 70 + "\n\n"
            result_text += f"📊 METRIC: {metric.upper()}\n"
            result_text += f"🎯 TYPE: {item_type.upper()}S\n\n"
            result_text += f"🔗 Similarity between:\n"
            result_text += f"   • '{item1}'\n"
            result_text += f"   • '{item2}'\n\n"
            result_text += f"⭐ SIMILARITY SCORE: {similarity:.4f}\n\n"
            
            if similarity > 0.7:
                result_text += "💡 Interpretation: Highly Similar\n"
            elif similarity > 0.4:
                result_text += "💡 Interpretation: Moderately Similar\n"
            else:
                result_text += "💡 Interpretation: Not Very Similar\n"
            
            result_text += "\n" + "=" * 70 + "\n"
            result_text += "TOP 5 RECOMMENDATIONS\n"
            result_text += "=" * 70 + "\n\n"
            
            result_text += f"🎤 Top 5 similar to '{item1}':\n"
            if top5_1:
                for name, score in top5_1:
                    result_text += f"   • {name}: {score:.4f}\n"
            else:
                result_text += "   No similar items found\n"
            
            result_text += f"\n🎤 Top 5 similar to '{item2}':\n"
            if top5_2:
                for name, score in top5_2:
                    result_text += f"   • {name}: {score:.4f}\n"
            else:
                result_text += "   No similar items found\n"
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, result_text)
            self.status_var.set(f"✅ Similarity calculated: {similarity:.4f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_var.set("❌ Error occurred")
            # Show traceback in results
            import traceback
            error_details = traceback.format_exc()
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, f"ERROR DETAILS:\n{error_details}")
    
    def get_recommendations(self):
        """Get recommendations for a single item"""
        item1 = self.input1_var.get().strip()
        
        if not item1:
            messagebox.showwarning("Input Required", 
                                 "Please enter an item to get recommendations")
            return
        
        try:
            self.status_var.set("🔄 Generating recommendations...")
            self.root.update()
            
            metric = self.metric_var.get()
            item_type = self.type_var.get()
            
            # Get recommendations
            recommendations = self.calculator.get_top_similar(
                item1, item_type, metric, 10
            )
            
            # Display results
            result_text = "=" * 70 + "\n"
            result_text += "RECOMMENDATION RESULTS\n"
            result_text += "=" * 70 + "\n\n"
            result_text += f"🎯 FOR: {item1}\n"
            result_text += f"📊 TYPE: {item_type.upper()}\n"
            result_text += f"⚙️ METRIC: {metric.upper()}\n\n"
            
            if recommendations:
                result_text += f"🏆 TOP 10 RECOMMENDATIONS:\n\n"
                for i, (name, score) in enumerate(recommendations, 1):
                    # Color code based on score
                    if score > 0.8:
                        prefix = "🔥 "
                    elif score > 0.6:
                        prefix = "⭐ "
                    elif score > 0.4:
                        prefix = "✓ "
                    else:
                        prefix = "• "
                    
                    result_text += f"{i:2}. {prefix}{name[:45]}: {score:.4f}\n"
                
                # Calculate average score
                avg_score = sum(score for _, score in recommendations) / len(recommendations)
                result_text += f"\n📈 Average recommendation score: {avg_score:.4f}"
                
                # Show strongest recommendation
                if recommendations:
                    best_name, best_score = recommendations[0]
                    result_text += f"\n\n🏅 STRONGEST RECOMMENDATION:\n"
                    result_text += f"   '{best_name}' with score: {best_score:.4f}"
            else:
                result_text += "❌ No recommendations found\n"
                result_text += "\n💡 Try using a different item or check your input."
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, result_text)
            self.status_var.set(f"✅ Generated {len(recommendations)} recommendations")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_var.set("❌ Error occurred")
    
    def clear_results(self):
        """Clear all results"""
        self.results_text.delete(1.0, tk.END)
        self.input1_var.set("")
        self.input2_var.set("")
        self.status_var.set("✅ Cleared - Ready for new input")
        self.show_welcome_message()
    
    def show_help(self):
        """Show help information"""
        help_text = """HELP - MUSIC RECOMMENDATION ENGINE

🎯 HOW TO USE:
1. Select similarity metric from the 4 options
2. Choose whether to compare Artists or Tracks
3. Enter item names in the input fields
   • For artists: Use artist names like 'Artist 0', 'Artist 1'
   • For tracks: Use track names like 'Song 0', 'Song 1'
4. Click buttons:
   • 'Calculate Similarity' - Compare two items
   • 'Get Recommendations' - Get similar items for one item
   • 'Clear' - Reset everything
   • 'Sample' - Fill with sample data

📊 SIMILARITY METRICS:
• Cosine - Measures angle between feature vectors
• Euclidean - Measures straight-line distance
• Pearson - Measures linear correlation
• Manhattan - Measures city-block distance

💡 TIPS:
• Use the 'Sample' buttons to quickly fill inputs
• Higher similarity scores (closer to 1) = more similar
• Check the welcome message for sample items
• Results include top 5 recommendations for each item
"""
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("600x500")
        
        help_text_widget = tk.Text(
            help_window,
            wrap=tk.WORD,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        help_text_widget.pack(expand=True, fill=tk.BOTH)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(
            help_window,
            text="Close",
            command=help_window.destroy
        ).pack(pady=10)
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()