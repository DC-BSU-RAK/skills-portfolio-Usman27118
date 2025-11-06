import tkinter as tk
from tkinter import messagebox
import random

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("400x300")
        self.score = 0
        self.question_count = 0
        self.attempt = 1
        self.current_answer = 0
        self.difficulty = 0
        self.num1 = 0
        self.num2 = 0
        self.operation = ''
        self.displayMenu()
    
    def displayMenu(self):
        self.clearWindow()
        tk.Label(self.root, text="DIFFICULTY LEVEL", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="1. Easy", width=20, command=lambda: self.startQuiz(1)).pack(pady=5)
        tk.Button(self.root, text="2. Moderate", width=20, command=lambda: self.startQuiz(2)).pack(pady=5)
        tk.Button(self.root, text="3. Advanced", width=20, command=lambda: self.startQuiz(3)).pack(pady=5)
    
    def startQuiz(self, level):
        self.difficulty = level
        self.score = 0
        self.question_count = 0
        self.nextQuestion()
    
    def randomInt(self):
        if self.difficulty == 1:
            return random.randint(1, 9), random.randint(1, 9)
        elif self.difficulty == 2:
            return random.randint(10, 99), random.randint(10, 99)
        else:
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self):
        return random.choice(['+', '-'])
    
    def nextQuestion(self):
        if self.question_count >= 10:
            self.displayResults()
            return
        
        self.question_count += 1
        self.attempt = 1
        self.num1, self.num2 = self.randomInt()
        self.operation = self.decideOperation()
        
        if self.operation == '+':
            self.current_answer = self.num1 + self.num2
        else:
            self.current_answer = self.num1 - self.num2
        
        self.displayProblem()
    
    def displayProblem(self):
        self.clearWindow()
        tk.Label(self.root, text=f"Question {self.question_count}/10", font=("Arial", 12)).pack(pady=10)
        tk.Label(self.root, text=f"Score: {self.score}/100", font=("Arial", 10)).pack()
        tk.Label(self.root, text=f"{self.num1} {self.operation} {self.num2} = ", 
                 font=("Arial", 20, "bold")).pack(pady=20)
        
        if self.attempt == 2:
            tk.Label(self.root, text="Try again! (5 points)", fg="orange", font=("Arial", 10)).pack()
        
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14), width=15)
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())
        
        tk.Button(self.root, text="Submit", command=self.checkAnswer, width=15).pack(pady=10)
    
    def checkAnswer(self):
        try:
            user_answer = int(self.answer_entry.get())
            if self.isCorrect(user_answer):
                if self.attempt == 1:
                    self.score += 10
                    messagebox.showinfo("Correct!", "Great job! +10 points")
                else:
                    self.score += 5
                    messagebox.showinfo("Correct!", "Well done! +5 points")
                self.nextQuestion()
            else:
                if self.attempt == 1:
                    self.attempt = 2
                    messagebox.showwarning("Incorrect", "Wrong answer. Try again!")
                    self.displayProblem()
                else:
                    messagebox.showerror("Incorrect", f"Wrong again. The answer was {self.current_answer}")
                    self.nextQuestion()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def isCorrect(self, user_answer):
        return user_answer == self.current_answer
    
    def displayResults(self):
        self.clearWindow()
        
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        tk.Label(self.root, text="Quiz Complete!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Final Score: {self.score}/100", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Grade: {grade}", font=("Arial", 16, "bold"), 
                 fg="green" if self.score >= 70 else "red").pack(pady=10)
        
        tk.Button(self.root, text="Play Again", command=self.displayMenu, width=15).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=15).pack(pady=5)
    
    def clearWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()