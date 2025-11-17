import tkinter as tk
from tkinter import messagebox, font
import random
import os

class AlexaJokeTeller:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("600x500")
        self.root.config(bg="#232F3E")  
        
        self.jokes = []
        self.current_joke = None
        self.joke_history = []
        self.favorites = []
        self.jokes_told = 0
        self.punchline_shown = False
        
        self.loadJokes()
        self.createGUI()
        
    def loadJokes(self):
        """Load jokes from file or use default jokes if file not found"""
        try:
            if os.path.exists("randomJokes.txt"):
                with open("randomJokes.txt", "r", encoding="utf-8") as file:
                    self.jokes = [line.strip() for line in file if line.strip()]
            else:
              
                self.jokes = [
                    "Why did the chicken cross the road?To get to the other side.",
                    "What happens if you boil a clown?You get a laughing stock.",
                    "Why don't scientists trust atoms?Because they make up everything.",
                    "What do you call a fake noodle?An impasta.",
                    "Why did the scarecrow win an award?He was outstanding in his field.",
                    "What do you call a bear with no teeth?A gummy bear.",
                    "Why don't eggs tell jokes?They'd crack each other up.",
                    "What do you call a fish with no eyes?Fsh.",
                    "Why did the math book look sad?Because it had too many problems.",
                    "What do you call a sleeping bull?A bulldozer."
                ]
        except Exception as e:
            messagebox.showerror("Error", f"Could not load jokes: {str(e)}")
            self.jokes = ["Why did the programmer quit?Because they didn't get arrays."]
    
    def createGUI(self):
        """Create the main GUI interface"""
        
        title_frame = tk.Frame(self.root, bg="#232F3E")
        title_frame.pack(pady=20)
        
        title_font = font.Font(family="Arial", size=24, weight="bold")
        tk.Label(title_frame, text="🎤 Alexa Joke Teller", font=title_font, 
                 bg="#232F3E", fg="#00D9FF").pack()
        
        self.stats_frame = tk.Frame(self.root, bg="#232F3E")
        self.stats_frame.pack(pady=5)
        
        self.stats_label = tk.Label(self.stats_frame, text=f"Jokes told: {self.jokes_told} | Favorites: {len(self.favorites)}", 
                                     font=("Arial", 10), bg="#232F3E", fg="#FFFFFF")
        self.stats_label.pack()
        
        self.joke_frame = tk.Frame(self.root, bg="#FFFFFF", relief="ridge", bd=2)
        self.joke_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        self.setup_label = tk.Label(self.joke_frame, text="Click 'Tell me a Joke' to hear a joke!", 
                                     font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#232F3E",
                                     wraplength=500, justify="center", pady=20)
        self.setup_label.pack(pady=20)
        
        self.punchline_label = tk.Label(self.joke_frame, text="", 
                                         font=("Arial", 14, "italic"), bg="#FFFFFF", fg="#FF9900",
                                         wraplength=500, justify="center")
        self.punchline_label.pack(pady=10)
        
        button_frame = tk.Frame(self.root, bg="#232F3E")
        button_frame.pack(pady=20)
        
        btn_style = {"font": ("Arial", 12, "bold"), "width": 18, "height": 2, "bd": 0, "cursor": "hand2"}
        
        self.tell_joke_btn = tk.Button(button_frame, text="🎭 Tell me a Joke", 
                                        bg="#00D9FF", fg="#232F3E", 
                                        command=self.tellJoke, **btn_style)
        self.tell_joke_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.punchline_btn = tk.Button(button_frame, text="😂 Show Punchline", 
                                        bg="#FF9900", fg="#FFFFFF", 
                                        command=self.showPunchline, state="disabled", **btn_style)
        self.punchline_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.next_joke_btn = tk.Button(button_frame, text="⏭️ Next Joke", 
                                        bg="#00A86B", fg="#FFFFFF", 
                                        command=self.nextJoke, state="disabled", **btn_style)
        self.next_joke_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.favorite_btn = tk.Button(button_frame, text="⭐ Add to Favorites", 
                                       bg="#FFD700", fg="#232F3E", 
                                       command=self.addToFavorites, state="disabled", **btn_style)
        self.favorite_btn.grid(row=1, column=1, padx=5, pady=5)
        
        bottom_frame = tk.Frame(self.root, bg="#232F3E")
        bottom_frame.pack(pady=10)
        
        small_btn_style = {"font": ("Arial", 10), "width": 15, "bd": 0, "cursor": "hand2"}
        
        tk.Button(bottom_frame, text="📋 View Favorites", bg="#4A5568", fg="#FFFFFF",
                  command=self.viewFavorites, **small_btn_style).pack(side="left", padx=5)
        
        tk.Button(bottom_frame, text="🔄 Reset Stats", bg="#E53E3E", fg="#FFFFFF",
                  command=self.resetStats, **small_btn_style).pack(side="left", padx=5)
        
        tk.Button(bottom_frame, text="❌ Quit", bg="#C53030", fg="#FFFFFF",
                  command=self.quit, **small_btn_style).pack(side="left", padx=5)
    
    def tellJoke(self):
        """Display a random joke setup"""
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available!")
            return
        
        available_jokes = [j for j in self.jokes if j not in self.joke_history[-5:]]
        if not available_jokes:
            available_jokes = self.jokes
        
        self.current_joke = random.choice(available_jokes)
        self.joke_history.append(self.current_joke)
        self.jokes_told += 1
        self.punchline_shown = False
        
        if "?" in self.current_joke:
            parts = self.current_joke.split("?", 1)
            setup = parts[0] + "?"
            self.punchline = parts[1].strip()
        else:
            setup = self.current_joke
            self.punchline = "😄"
        
        self.setup_label.config(text=setup, fg="#232F3E")
        self.punchline_label.config(text="")
        self.updateStats()
   
        self.tell_joke_btn.config(state="disabled")
        self.punchline_btn.config(state="normal")
        self.next_joke_btn.config(state="normal")
        self.favorite_btn.config(state="normal")
    
    def showPunchline(self):
        """Display the punchline"""
        if self.current_joke:
            self.punchline_label.config(text=self.punchline)
            self.punchline_btn.config(state="disabled")
            self.punchline_shown = True
    
    def nextJoke(self):
        """Reset and tell a new joke"""
        self.tellJoke()
    
    def addToFavorites(self):
        """Add current joke to favorites"""
        if self.current_joke and self.current_joke not in self.favorites:
            self.favorites.append(self.current_joke)
            self.updateStats()
            messagebox.showinfo("Added!", "Joke added to favorites! ⭐")
        elif self.current_joke in self.favorites:
            messagebox.showinfo("Already Added", "This joke is already in your favorites!")
    
    def viewFavorites(self):
        """Display favorite jokes in a new window"""
        if not self.favorites:
            messagebox.showinfo("No Favorites", "You haven't added any favorite jokes yet!")
            return
        
        fav_window = tk.Toplevel(self.root)
        fav_window.title("Favorite Jokes")
        fav_window.geometry("500x400")
        fav_window.config(bg="#FFFFFF")
        
        tk.Label(fav_window, text="⭐ Your Favorite Jokes ⭐", 
                 font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)
        
        text_frame = tk.Frame(fav_window)
        text_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 11), 
                              yscrollcommand=scrollbar.set)
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        for i, joke in enumerate(self.favorites, 1):
            text_widget.insert("end", f"{i}. {joke}\n\n")
        
        text_widget.config(state="disabled")
        
        tk.Button(fav_window, text="Close", command=fav_window.destroy,
                  bg="#4A5568", fg="#FFFFFF", font=("Arial", 10)).pack(pady=10)
    
    def resetStats(self):
        """Reset statistics"""
        if messagebox.askyesno("Reset Stats", "Are you sure you want to reset all statistics?"):
            self.jokes_told = 0
            self.joke_history = []
            self.favorites = []
            self.updateStats()
            self.setup_label.config(text="Click 'Tell me a Joke' to hear a joke!")
            self.punchline_label.config(text="")
            self.tell_joke_btn.config(state="normal")
            self.punchline_btn.config(state="disabled")
            self.next_joke_btn.config(state="disabled")
            self.favorite_btn.config(state="disabled")
    
    def updateStats(self):
        """Update statistics display"""
        self.stats_label.config(text=f"Jokes told: {self.jokes_told} | Favorites: {len(self.favorites)}")
    
    def quit(self):
        """Exit the application"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlexaJokeTeller(root)
    root.mainloop()