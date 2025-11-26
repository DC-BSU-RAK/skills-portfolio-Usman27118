import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager System")
        self.root.geometry("900x600")
        self.root.config(bg="#2C3E50")
        
        self.students = []
        self.loadStudents()
        self.createGUI()
    
    def loadStudents(self):
        """Load student data from file"""
        try:
            if os.path.exists("studentMarks.txt"):
                with open("studentMarks.txt", "r") as file:
                    lines = file.readlines()
                    num_students = int(lines[0].strip())
                    for i in range(1, num_students + 1):
                        data = lines[i].strip().split(',')
                        student = {
                            'code': data[0],
                            'name': data[1],
                            'course1': int(data[2]),
                            'course2': int(data[3]),
                            'course3': int(data[4]),
                            'exam': int(data[5])
                        }
                        student['total_coursework'] = student['course1'] + student['course2'] + student['course3']
                        student['overall_marks'] = student['total_coursework'] + student['exam']
                        student['percentage'] = (student['overall_marks'] / 160) * 100
                        student['grade'] = self.calculateGrade(student['percentage'])
                        self.students.append(student)
            else:
                # Sample data if file doesn't exist
                sample_data = [
                    "8439,Jake Hobbs,10,11,10,43",
                    "7234,Emma Smith,18,17,19,85",
                    "5678,John Doe,12,13,11,55",
                    "9012,Sarah Jones,15,16,14,72",
                    "6543,Mike Brown,8,9,7,38"
                ]
                for data_line in sample_data:
                    data = data_line.split(',')
                    student = {
                        'code': data[0],
                        'name': data[1],
                        'course1': int(data[2]),
                        'course2': int(data[3]),
                        'course3': int(data[4]),
                        'exam': int(data[5])
                    }
                    student['total_coursework'] = student['course1'] + student['course2'] + student['course3']
                    student['overall_marks'] = student['total_coursework'] + student['exam']
                    student['percentage'] = (student['overall_marks'] / 160) * 100
                    student['grade'] = self.calculateGrade(student['percentage'])
                    self.students.append(student)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading student data: {str(e)}")
    
    def calculateGrade(self, percentage):
        """Calculate grade based on percentage"""
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def createGUI(self):
        """Create the main GUI interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#34495E", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📚 Student Manager System", 
                 font=("Arial", 22, "bold"), bg="#34495E", fg="#ECF0F1").pack(pady=25)
        
        # Menu buttons
        menu_frame = tk.Frame(self.root, bg="#2C3E50")
        menu_frame.pack(pady=20)
        
        btn_style = {"font": ("Arial", 11, "bold"), "width": 22, "height": 2, "bd": 0, "cursor": "hand2"}
        
        tk.Button(menu_frame, text="📋 View All Students", bg="#3498DB", fg="white",
                  command=self.viewAllStudents, **btn_style).grid(row=0, column=0, padx=10, pady=10)
        
        tk.Button(menu_frame, text="🔍 View Individual Student", bg="#9B59B6", fg="white",
                  command=self.viewIndividualStudent, **btn_style).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(menu_frame, text="🏆 Highest Score", bg="#27AE60", fg="white",
                  command=self.showHighestScore, **btn_style).grid(row=1, column=0, padx=10, pady=10)
        
        tk.Button(menu_frame, text="📉 Lowest Score", bg="#E74C3C", fg="white",
                  command=self.showLowestScore, **btn_style).grid(row=1, column=1, padx=10, pady=10)
        
        # Display area
        display_frame = tk.Frame(self.root, bg="#2C3E50")
        display_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(display_frame, text="Results Display", font=("Arial", 12, "bold"),
                 bg="#2C3E50", fg="#ECF0F1").pack(anchor="w", pady=5)
        
        self.display_text = scrolledtext.ScrolledText(display_frame, font=("Courier", 10),
                                                       bg="#ECF0F1", fg="#2C3E50", wrap="word")
        self.display_text.pack(fill="both", expand=True)
        
        # Bottom buttons
        bottom_frame = tk.Frame(self.root, bg="#2C3E50")
        bottom_frame.pack(pady=10)
        
        tk.Button(bottom_frame, text="🔄 Refresh Data", bg="#16A085", fg="white",
                  command=self.refreshData, font=("Arial", 10), width=15, bd=0).pack(side="left", padx=5)
        
        tk.Button(bottom_frame, text="❌ Exit", bg="#C0392B", fg="white",
                  command=self.root.quit, font=("Arial", 10), width=15, bd=0).pack(side="left", padx=5)
    
    def formatStudentRecord(self, student):
        """Format a student record for display"""
        record = f"""
{'='*70}
Student Name:           {student['name']}
Student Number:         {student['code']}
Course Marks:           {student['course1']}/20, {student['course2']}/20, {student['course3']}/20
Total Coursework:       {student['total_coursework']}/60
Exam Mark:              {student['exam']}/100
Overall Marks:          {student['overall_marks']}/160
Overall Percentage:     {student['percentage']:.2f}%
Grade:                  {student['grade']}
{'='*70}
"""
        return record
    
    def viewAllStudents(self):
        """Display all student records"""
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "📋 ALL STUDENT RECORDS\n")
        self.display_text.insert(tk.END, "="*70 + "\n")
        
        for student in self.students:
            self.display_text.insert(tk.END, self.formatStudentRecord(student))
        
        # Summary
        avg_percentage = sum(s['percentage'] for s in self.students) / len(self.students)
        summary = f"""
{'='*70}
SUMMARY
{'='*70}
Total Students:         {len(self.students)}
Average Percentage:     {avg_percentage:.2f}%
{'='*70}
"""
        self.display_text.insert(tk.END, summary)
    
    def viewIndividualStudent(self):
        """View a specific student's record"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Student")
        search_window.geometry("400x250")
        search_window.config(bg="#34495E")
        
        tk.Label(search_window, text="🔍 Search Student", font=("Arial", 16, "bold"),
                 bg="#34495E", fg="#ECF0F1").pack(pady=20)
        
        tk.Label(search_window, text="Enter Student Name or Code:", 
                 bg="#34495E", fg="#ECF0F1", font=("Arial", 11)).pack(pady=5)
        
        search_entry = tk.Entry(search_window, font=("Arial", 12), width=30)
        search_entry.pack(pady=10)
        search_entry.focus()
        
        def search():
            query = search_entry.get().strip().lower()
            found = None
            
            for student in self.students:
                if query == student['code'].lower() or query in student['name'].lower():
                    found = student
                    break
            
            if found:
                self.display_text.delete(1.0, tk.END)
                self.display_text.insert(tk.END, "🔍 INDIVIDUAL STUDENT RECORD\n")
                self.display_text.insert(tk.END, self.formatStudentRecord(found))
                search_window.destroy()
            else:
                messagebox.showwarning("Not Found", "Student not found! Please try again.")
        
        tk.Button(search_window, text="Search", bg="#3498DB", fg="white",
                  command=search, font=("Arial", 11, "bold"), width=15, bd=0).pack(pady=10)
        
        search_entry.bind('<Return>', lambda e: search())
    
    def showHighestScore(self):
        """Display student with highest score"""
        if not self.students:
            messagebox.showwarning("No Data", "No student data available!")
            return
        
        highest = max(self.students, key=lambda s: s['overall_marks'])
        
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "🏆 STUDENT WITH HIGHEST SCORE\n")
        self.display_text.insert(tk.END, self.formatStudentRecord(highest))
    
    def showLowestScore(self):
        """Display student with lowest score"""
        if not self.students:
            messagebox.showwarning("No Data", "No student data available!")
            return
        
        lowest = min(self.students, key=lambda s: s['overall_marks'])
        
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "📉 STUDENT WITH LOWEST SCORE\n")
        self.display_text.insert(tk.END, self.formatStudentRecord(lowest))
    
    def refreshData(self):
        """Reload student data"""
        self.students = []
        self.loadStudents()
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, "✅ Data refreshed successfully!\n\n")
        self.display_text.insert(tk.END, f"Total students loaded: {len(self.students)}\n")
        messagebox.showinfo("Success", "Student data refreshed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()