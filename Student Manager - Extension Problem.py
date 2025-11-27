import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager System - Extended")
        self.root.geometry("950x650")
        self.root.config(bg="#2C3E50")
        self.students = []
        self.loadStudents()
        self.createGUI()
    
    def loadStudents(self):
        self.students = []
        try:
            if os.path.exists("studentMarks.txt"):
                with open("studentMarks.txt", "r") as f:
                    lines = f.readlines()
                    for i in range(1, len(lines)):
                        self.parseStudent(lines[i].strip())
            else:
                samples = ["8439,Jake Hobbs,10,11,10,43", "7234,Emma Smith,18,17,19,85", 
                          "5678,John Doe,12,13,11,55", "9012,Sarah Jones,15,16,14,72"]
                for s in samples:
                    self.parseStudent(s)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading: {str(e)}")
    
    def parseStudent(self, line):
        data = line.split(',')
        student = {'code': data[0], 'name': data[1], 'course1': int(data[2]), 
                   'course2': int(data[3]), 'course3': int(data[4]), 'exam': int(data[5])}
        student['total_coursework'] = student['course1'] + student['course2'] + student['course3']
        student['overall_marks'] = student['total_coursework'] + student['exam']
        student['percentage'] = (student['overall_marks'] / 160) * 100
        student['grade'] = self.calculateGrade(student['percentage'])
        self.students.append(student)
    
    def saveStudents(self):
        try:
            with open("studentMarks.txt", "w") as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(f"{s['code']},{s['name']},{s['course1']},{s['course2']},{s['course3']},{s['exam']}\n")
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving: {str(e)}")
    
    def calculateGrade(self, percentage):
        if percentage >= 70: return 'A'
        elif percentage >= 60: return 'B'
        elif percentage >= 50: return 'C'
        elif percentage >= 40: return 'D'
        else: return 'F'
    
    def createGUI(self):
        title_frame = tk.Frame(self.root, bg="#34495E", height=70)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="📚 Student Manager - Extended", font=("Arial", 20, "bold"), 
                 bg="#34495E", fg="#ECF0F1").pack(pady=20)
        
        menu_frame = tk.Frame(self.root, bg="#2C3E50")
        menu_frame.pack(pady=15)
        
        btn_style = {"font": ("Arial", 10, "bold"), "width": 18, "height": 2, "bd": 0, "cursor": "hand2"}
        
        buttons = [
            ("📋 View All", "#3498DB", self.viewAllStudents),
            ("🔍 View Individual", "#9B59B6", self.viewIndividualStudent),
            ("🏆 Highest Score", "#27AE60", self.showHighestScore),
            ("📉 Lowest Score", "#E74C3C", self.showLowestScore),
            ("🔄 Sort Records", "#F39C12", self.sortStudents),
            ("➕ Add Student", "#1ABC9C", self.addStudent),
            ("🗑️ Delete Student", "#E67E22", self.deleteStudent),
            ("✏️ Update Student", "#8E44AD", self.updateStudent)
        ]
        
        for i, (text, color, cmd) in enumerate(buttons):
            tk.Button(menu_frame, text=text, bg=color, fg="white", command=cmd, **btn_style).grid(
                row=i//4, column=i%4, padx=5, pady=5)
        
        display_frame = tk.Frame(self.root, bg="#2C3E50")
        display_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.display_text = scrolledtext.ScrolledText(display_frame, font=("Courier", 9),
                                                       bg="#ECF0F1", fg="#2C3E50", wrap="word")
        self.display_text.pack(fill="both", expand=True)
        
        tk.Button(self.root, text="❌ Exit", bg="#C0392B", fg="white", command=self.root.quit,
                  font=("Arial", 10), width=15, bd=0).pack(pady=10)
    
    def formatStudentRecord(self, student):
        return f"""{'='*68}
Name: {student['name']:<20} Code: {student['code']}
Courses: {student['course1']}/20, {student['course2']}/20, {student['course3']}/20  |  Total CW: {student['total_coursework']}/60
Exam: {student['exam']}/100  |  Overall: {student['overall_marks']}/160  |  {student['percentage']:.2f}%  |  Grade: {student['grade']}
{'='*68}\n"""
    
    def viewAllStudents(self):
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "📋 ALL STUDENT RECORDS\n\n")
        for s in self.students:
            self.display_text.insert(tk.END, self.formatStudentRecord(s))
        avg = sum(s['percentage'] for s in self.students) / len(self.students) if self.students else 0
        self.display_text.insert(tk.END, f"\n📊 Total: {len(self.students)} | Average: {avg:.2f}%\n")
    
    def findStudent(self, query):
        query = query.strip().lower()
        for s in self.students:
            if query == s['code'].lower() or query in s['name'].lower():
                return s
        return None
    
    def viewIndividualStudent(self):
        query = simpledialog.askstring("Search", "Enter Student Name or Code:")
        if query:
            student = self.findStudent(query)
            if student:
                self.display_text.delete(1.0, tk.END)
                self.display_text.insert(tk.END, "🔍 INDIVIDUAL RECORD\n\n")
                self.display_text.insert(tk.END, self.formatStudentRecord(student))
            else:
                messagebox.showwarning("Not Found", "Student not found!")
    
    def showHighestScore(self):
        if not self.students: return
        highest = max(self.students, key=lambda s: s['overall_marks'])
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "🏆 HIGHEST SCORE\n\n")
        self.display_text.insert(tk.END, self.formatStudentRecord(highest))
    
    def showLowestScore(self):
        if not self.students: return
        lowest = min(self.students, key=lambda s: s['overall_marks'])
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "📉 LOWEST SCORE\n\n")
        self.display_text.insert(tk.END, self.formatStudentRecord(lowest))
    
    def sortStudents(self):
        sort_win = tk.Toplevel(self.root)
        sort_win.title("Sort Options")
        sort_win.geometry("300x200")
        sort_win.config(bg="#34495E")
        
        tk.Label(sort_win, text="🔄 Sort By", font=("Arial", 14, "bold"), 
                 bg="#34495E", fg="#ECF0F1").pack(pady=15)
        
        def sort_and_display(key, reverse):
            self.students.sort(key=lambda s: s[key], reverse=reverse)
            self.viewAllStudents()
            sort_win.destroy()
        
        tk.Button(sort_win, text="📈 Score (Ascending)", bg="#3498DB", fg="white",
                  command=lambda: sort_and_display('overall_marks', False), 
                  font=("Arial", 10), width=20).pack(pady=5)
        tk.Button(sort_win, text="📉 Score (Descending)", bg="#E74C3C", fg="white",
                  command=lambda: sort_and_display('overall_marks', True), 
                  font=("Arial", 10), width=20).pack(pady=5)
        tk.Button(sort_win, text="🔤 Name (A-Z)", bg="#27AE60", fg="white",
                  command=lambda: sort_and_display('name', False), 
                  font=("Arial", 10), width=20).pack(pady=5)
    
    def addStudent(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add Student")
        add_win.geometry("400x350")
        add_win.config(bg="#34495E")
        
        tk.Label(add_win, text="➕ Add New Student", font=("Arial", 14, "bold"),
                 bg="#34495E", fg="#ECF0F1").pack(pady=15)
        
        fields = [("Code (1000-9999):", tk.Entry(add_win)), ("Name:", tk.Entry(add_win)),
                  ("Course 1 (/20):", tk.Entry(add_win)), ("Course 2 (/20):", tk.Entry(add_win)),
                  ("Course 3 (/20):", tk.Entry(add_win)), ("Exam (/100):", tk.Entry(add_win))]
        
        entries = []
        for label, entry in fields:
            tk.Label(add_win, text=label, bg="#34495E", fg="#ECF0F1").pack()
            entry.pack(pady=2)
            entries.append(entry)
        
        def save():
            try:
                code, name = entries[0].get(), entries[1].get()
                c1, c2, c3, exam = int(entries[2].get()), int(entries[3].get()), int(entries[4].get()), int(entries[5].get())
                
                if not (1000 <= int(code) <= 9999 and all(0 <= x <= 20 for x in [c1, c2, c3]) and 0 <= exam <= 100):
                    raise ValueError("Invalid marks range")
                
                self.parseStudent(f"{code},{name},{c1},{c2},{c3},{exam}")
                self.saveStudents()
                add_win.destroy()
                self.viewAllStudents()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        tk.Button(add_win, text="Save", bg="#27AE60", fg="white", command=save,
                  font=("Arial", 10), width=15).pack(pady=10)
    
    def deleteStudent(self):
        query = simpledialog.askstring("Delete", "Enter Student Name or Code to delete:")
        if query:
            student = self.findStudent(query)
            if student:
                if messagebox.askyesno("Confirm", f"Delete {student['name']}?"):
                    self.students.remove(student)
                    self.saveStudents()
                    self.viewAllStudents()
            else:
                messagebox.showwarning("Not Found", "Student not found!")
    
    def updateStudent(self):
        query = simpledialog.askstring("Update", "Enter Student Name or Code to update:")
        if not query:
            return
        
        student = self.findStudent(query)
        if not student:
            messagebox.showwarning("Not Found", "Student not found!")
            return
        
        upd_win = tk.Toplevel(self.root)
        upd_win.title("Update Student")
        upd_win.geometry("350x300")
        upd_win.config(bg="#34495E")
        
        tk.Label(upd_win, text=f"✏️ Update: {student['name']}", font=("Arial", 12, "bold"),
                 bg="#34495E", fg="#ECF0F1").pack(pady=10)
        
        def update_field(field, label):
            new_val = simpledialog.askstring("Update", f"Enter new {label}:")
            if new_val:
                try:
                    if field in ['course1', 'course2', 'course3', 'exam']:
                        student[field] = int(new_val)
                        student['total_coursework'] = student['course1'] + student['course2'] + student['course3']
                        student['overall_marks'] = student['total_coursework'] + student['exam']
                        student['percentage'] = (student['overall_marks'] / 160) * 100
                        student['grade'] = self.calculateGrade(student['percentage'])
                    else:
                        student[field] = new_val
                    self.saveStudents()
                    messagebox.showinfo("Success", f"{label} updated!")
                    upd_win.destroy()
                    self.viewAllStudents()
                except:
                    messagebox.showerror("Error", "Invalid input!")
        
        options = [("Name", 'name'), ("Course 1", 'course1'), ("Course 2", 'course2'),
                   ("Course 3", 'course3'), ("Exam", 'exam')]
        
        for label, field in options:
            tk.Button(upd_win, text=f"Update {label}", bg="#8E44AD", fg="white",
                      command=lambda f=field, l=label: update_field(f, l),
                      font=("Arial", 10), width=20).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()