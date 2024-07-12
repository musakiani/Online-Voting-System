import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

class UniversityVotingSystem:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ajmalkhan@123",
            database="quad"
        )
        self.root = tk.Tk()
        self.root.title("Institute of Information Technology and Quaid-i-Azam University, Islamabad, Pakistan")
        self.candidate_vars = {}
        self.main_menu()
        self.root.mainloop()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Online Voting System of IIT Elections", font=("Arial", 20), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Instructions", font=("Arial", 16, "bold"), fg="black").pack(pady=5)
        instructions = """
        1: First Signup, enter your all details.
        2: Then Login with your ID and cast your vote.
        Note: Only IIT students are allowed to vote.
        """
        tk.Label(self.root, text=instructions, font=("Arial", 12), fg="black").pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login, fg="white", bg="blue").pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.signup, fg="white", bg="green").pack(pady=5)
        tk.Button(self.root, text="Admin Login", command=self.admin_login, fg="white", bg="blue").pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, fg="white", bg="blue").pack(pady=20)

    def signup(self):
        self.clear_window()
        tk.Label(self.root, text="Sign Up", font=("Arial", 20), fg="green").pack(pady=20)
        self.create_entry("Student ID", "reg_student_id_entry")
        self.create_entry("Name", "reg_name_entry")
        self.create_entry("Email", "reg_email_entry")
        tk.Button(self.root, text="Sign Up", command=self.process_registration, fg="white", bg="green").pack(pady=20)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, fg="white", bg="black").pack()

    def process_registration(self):
        student_id = self.reg_student_id_entry.get()
        name = self.reg_name_entry.get()
        email = self.reg_email_entry.get()

        if len(student_id) != 11 or not student_id.isnumeric():
            messagebox.showerror("Error", "Invalid student ID. Student ID must be 11 digits.")
            return

        if not re.match(r"[^@]+@gmail\.com", email):
            messagebox.showerror("Error", "Invalid email address. Please enter a valid Gmail address.")
            return

        # Check if student already exists
        cur = self.db.cursor()
        query = "SELECT * FROM student5 WHERE StudentID=%s"
        cur.execute(query, (student_id,))
        if cur.fetchone():
            messagebox.showerror("Error", "Student already registered")
            return

        # Insert new student
        query = "INSERT INTO student5 (StudentID, Name, Email) VALUES (%s, %s, %s)"
        cur.execute(query, (student_id, name, email))
        self.db.commit()
        messagebox.showinfo("Success", "Registration successful!")
        self.clear_window()  # Clear window after successful registration
        self.main_menu()  # Return to main menu

    def create_entry(self, label_text, entry_var_name, show=""):
        tk.Label(self.root, text=label_text, fg="black").pack()
        entry = tk.Entry(self.root, show=show)
        entry.pack()
        setattr(self, entry_var_name, entry)

    def login(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 20), fg="blue").pack(pady=20)
        self.create_entry("Student ID", "student_id_entry")
        tk.Button(self.root, text="Login", command=self.process_login, fg="white", bg="blue").pack(pady=20)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, fg="white", bg="black").pack()

    def process_login(self):
        student_id = self.student_id_entry.get()
        if len(student_id) != 11 or not student_id.isnumeric():
            messagebox.showerror("Error", "Invalid student ID. Student ID must be 11 digits.")
            return

        cur = self.db.cursor()
        query = "SELECT * FROM student5 WHERE StudentID=%s"
        cur.execute(query, (student_id,))
        user = cur.fetchone()
        if not user:
            messagebox.showerror("Error", "Student ID not found")
            return

        self.after_login(student_id)

    def after_login(self, student_id):
        self.clear_window()
        tk.Label(self.root, text="Welcome", font=("Arial", 20), fg="blue").pack(pady=20)
        tk.Button(self.root, text="Vote", command=lambda: self.vote(student_id), fg="white", bg="blue").pack(pady=5)
        tk.Button(self.root, text="Log Out", command=self.main_menu, fg="white", bg="black").pack(pady=5)

    def vote(self, student_id):
        self.clear_window()
        tk.Label(self.root, text="Vote for Departmental Positions", font=("Arial", 20), fg="blue").pack(pady=20)

        # Check if the student has already voted
        cur = self.db.cursor()
        query = "SELECT * FROM vote5 WHERE StudentID=%s"
        cur.execute(query, (student_id,))
        if cur.fetchone():
            messagebox.showerror("Error", "You have already voted")
            self.after_login(student_id)
            return

        # Fetch positions from the database
        query = "SELECT DISTINCT Position FROM candidate5"
        cur.execute(query)
        positions = cur.fetchall()

        if not positions:
            messagebox.showerror("Error", "No positions available to vote")
            self.after_login(student_id)
            return

        # Display voting options for each position in separate tables
        for position in positions:
            position = position[0]  # Unpack the position tuple
            tk.Label(self.root, text=f"{position}:", font=("Arial", 16, "bold")).pack(pady=10)

            # Fetch candidates for the current position
            query = "SELECT Name, Department, Semester, BallotName FROM candidate5 WHERE Position=%s"
            cur.execute(query, (position,))
            candidates = cur.fetchall()

            if not candidates:
                tk.Label(self.root, text="No candidates registered for this position").pack(pady=5)
                continue

            # Create a frame for the table
            frame = tk.Frame(self.root, borderwidth=2, relief="groove")
            frame.pack(pady=10)

            # Create radio buttons for each candidate
            self.candidate_vars[position] = tk.StringVar()
            for candidate in candidates:
                candidate_info = f"Name: {candidate[0]}, Department: {candidate[1]}, Semester: {candidate[2]}, Ballot Name: {candidate[3]}"
                tk.Radiobutton(frame, text=candidate_info, variable=self.candidate_vars[position], value=candidate[0]).pack(anchor="w")

        # Vote button and back button
        tk.Button(self.root, text="Vote", command=lambda: self.process_vote(student_id), fg="white", bg="blue").pack(pady=20)
        tk.Button(self.root, text="Back", command=lambda: self.after_login(student_id), fg="white", bg="black").pack()

    def process_vote(self, student_id):
        # Get selected candidates from self.candidate_vars
        selected_candidates = {position: candidate.get() for position, candidate in self.candidate_vars.items()}

        # Validate if all positions have been voted
        if any(candidate == "" for candidate in selected_candidates.values()):
            messagebox.showerror("Error", "Please vote for all positions")
            return

        cur = self.db.cursor()

        # Insert votes into the database
        for position, candidate_name in selected_candidates.items():
            query = "INSERT INTO vote5 (StudentID, CandidateName) VALUES (%s, %s)"
            cur.execute(query, (student_id, candidate_name))

        self.db.commit()
        messagebox.showinfo("Success", "Your vote has been cast successfully!")
        self.after_login(student_id)

    def admin_login(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Login", font=("Arial", 20), fg="red").pack(pady=20)
        self.create_entry("Admin Username", "admin_username_entry")
        self.create_entry("Admin Password", "admin_password_entry", show="*")
        tk.Button(self.root, text="Login", command=self.process_admin_login, fg="white", bg="red").pack(pady=20)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, fg="white", bg="black").pack()

    def process_admin_login(self):
        username = self.admin_username_entry.get()
        password = self.admin_password_entry.get()

        # Dummy check for admin credentials
        if username == "admin" and password == "admin123":
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Invalid admin credentials")

    def admin_panel(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Panel", font=("Arial", 20), fg="red").pack(pady=20)
        tk.Button(self.root, text="Register Candidate", command=self.candidate_registration, fg="white", bg="red").pack(pady=20)
        tk.Button(self.root, text="Delete Candidate", command=self.delete_candidate, fg="white", bg="red").pack(pady=20)
        tk.Button(self.root, text="View Voting Results", command=self.show_result, fg="white", bg="red").pack(pady=20)
        tk.Button(self.root, text="View Registered Students", command=self.show_registered_students_admin, fg="white", bg="red").pack(pady=20)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, fg="white", bg="black").pack(pady=20)

    def candidate_registration(self):
        self.clear_window()
        tk.Label(self.root, text="Candidate Registration", font=("Arial", 20), fg="red").pack(pady=20)
        self.create_entry("Student ID", "reg_student_id_entry")
        self.create_entry("Name", "reg_name_entry")
        self.create_entry("Department", "reg_department_entry")
        self.create_entry("Semester", "reg_semester_entry")
        self.create_entry("Ballot Name", "reg_ballot_name_entry")
        self.create_entry("Position", "reg_position_entry")
        tk.Button(self.root, text="Register", command=self.process_candidate_registration, fg="white", bg="red").pack(pady=20)
        tk.Button(self.root, text="Back to Admin Panel", command=self.admin_panel, fg="white", bg="black").pack()

    def process_candidate_registration(self):
        student_id = self.reg_student_id_entry.get()
        name = self.reg_name_entry.get()
        department = self.reg_department_entry.get()
        semester = self.reg_semester_entry.get()
        ballot_name = self.reg_ballot_name_entry.get()
        position = self.reg_position_entry.get()

        # Insert new candidate
        cur = self.db.cursor()
        query = "INSERT INTO candidate5 (StudentID, Name, Department, Semester, BallotName, Position) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (student_id, name, department, semester, ballot_name, position))
        self.db.commit()
        messagebox.showinfo("Success", "Candidate registration successful!")
        self.admin_panel()

    def delete_candidate(self):
        self.clear_window()
        tk.Label(self.root, text="Delete Candidate", font=("Arial", 20), fg="red").pack(pady=20)
        self.create_entry("Student ID", "del_student_id_entry")
        tk.Button(self.root, text="Delete", command=self.process_candidate_deletion, fg="white", bg="red").pack(pady=20)
        tk.Button(self.root, text="Back to Admin Panel", command=self.admin_panel, fg="white", bg="black").pack()

    def process_candidate_deletion(self):
        student_id = self.del_student_id_entry.get()

        cur = self.db.cursor()
        query = "DELETE FROM candidate5 WHERE StudentID=%s"
        cur.execute(query, (student_id,))
        self.db.commit()

        if cur.rowcount > 0:
            messagebox.showinfo("Success", "Candidate deleted successfully!")
        else:
            messagebox.showerror("Error", "Candidate not found!")
        self.admin_panel()

    def show_result(self):
        self.clear_window()
        tk.Label(self.root, text="Voting Results", font=("Arial", 20), fg="purple").pack(pady=20)

        # Fetch voting results from the database
        cur = self.db.cursor()
        query = """
        SELECT candidate5.Position, candidate5.Name, COUNT(vote5.CandidateName) AS VoteCount
        FROM vote5
        JOIN candidate5 ON vote5.CandidateName = candidate5.Name
        GROUP BY candidate5.Position, candidate5.Name
        ORDER BY candidate5.Position, VoteCount DESC
        """
        cur.execute(query)
        results = cur.fetchall()

        for position, name, vote_count in results:
            result_info = f"Position: {position}, Candidate: {name}, Votes: {vote_count}"
            tk.Label(self.root, text=result_info).pack()

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, fg="white", bg="black").pack(pady=20)

    def show_registered_students_admin(self):
        self.clear_window()
        tk.Label(self.root, text="Registered Students", font=("Arial", 20), fg="purple").pack(pady=20)

        cur = self.db.cursor()
        query = "SELECT StudentID, Name, Email FROM student5"
        cur.execute(query)
        students = cur.fetchall()

        if not students:
            tk.Label(self.root, text="No students registered").pack(pady=10)
        else:
            for student in students:
                student_info = f"Student ID: {student[0]}, Name: {student[1]}, Email: {student[2]}"
                tk.Label(self.root, text=student_info).pack(pady=5)

        tk.Button(self.root, text="Back to Admin Panel", command=self.admin_panel, fg="white", bg="black").pack(pady=20)

if __name__ == "__main__":
    UniversityVotingSystem()
