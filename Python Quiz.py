import customtkinter as ctk
import os

# Colors
YELLOW = "#FFD700"
WHITE = "#FFFFFF"
DARK_GRAY = "#2C3E50"
GREEN = "#27AE60"
RED = "#C0392B"
BLUE = "#2980B9"
PURPLE = "#8E44AD" 

class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Expert Quiz")
        self.geometry("850x650")
        ctk.set_appearance_mode("light")
        
        self.lives = 3
        self.correct_count = 0
        self.incorrect_count = 0
        self.skipped_count = 0
        self.current_q_index = 0
        self.timer_running = False

        # 15 Order-wise Questions
        self.questions_data = [
            {"q": "1. Who created Python?", "options": ["Guido van Rossum", "Dennis Ritchie", "James Gosling", "Bjarne Stroustrup"], "ans": "Guido van Rossum"},
            {"q": "2. Is Python case-sensitive?", "options": ["Yes", "No", "Only for variables", "Depends on OS"], "ans": "Yes"},
            {"q": "3. Python is Procedural or OOP language?", "options": ["Procedural Only", "OOP Only", "Both", "None"], "ans": "Both"},
            {"q": "4. How many keywords are there in Python (3.11+)?", "options": ["30", "33", "35", "37"], "ans": "35"},
            {"q": "5. Which function is used to display output in Python?", "options": ["output()", "display()", "print()", "write()"], "ans": "print()"},
            {"q": "6. Which function is used to take input from the user?", "options": ["get()", "input()", "scanf()", "read()"], "ans": "input()"},
            {"q": "7. What is the file extension of Python?", "options": [".python", ".pyt", ".py", ".p"], "ans": ".py"},
            {"q": "8. Which symbol is used for comments in Python?", "options": ["//", "/*", "#", "--"], "ans": "#"},
            {"q": "9. Which keyword is used for 'Classes' in Python?", "options": ["className", "class", "def", "struct"], "ans": "class"},
            {"q": "10. Which symbol is used for equality in Python?", "options": ["=", "==", "===", "is"], "ans": "=="},
            {"q": "11. What is the output of 2 ** 3 in Python?", "options": ["6", "8", "9", "5"], "ans": "8"},
            {"q": "12. Which data type is used to store multiple items in a single variable?", "options": ["int", "float", "list", "bool"], "ans": "list"},
            {"q": "13. How do you define a function in Python?", "options": ["function", "void", "def", "method"], "ans": "def"},
            {"q": "14. Which operator is used for floor division?", "options": ["/", "%", "//", "**"], "ans": "//"},
            {"q": "15. Which statement is used to exit a loop?", "options": ["stop", "exit", "break", "return"], "ans": "break"}
        ]
        
        self.setup_ui()
        self.start_game()

    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color=YELLOW, height=100, corner_radius=0)
        self.header.pack(fill="x")

        self.lives_label = ctk.CTkLabel(self.header, text="", font=("Helvetica", 18, "bold"), text_color=DARK_GRAY)
        self.lives_label.place(relx=0.1, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self.header, text="PYTHON QUIZ", font=("Helvetica", 40, "bold"), text_color=DARK_GRAY)
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")

        self.timer_label = ctk.CTkLabel(self.header, text="", font=("Helvetica", 28, "bold"), text_color=DARK_GRAY)
        self.timer_label.place(relx=0.9, rely=0.5, anchor="center")

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="#F8F9F9", corner_radius=30, border_width=1, border_color="#E0E0E0")
        self.container.pack(pady=40, padx=60, fill="both", expand=True)

        self.main_q_label = ctk.CTkLabel(self.container, text="", font=("Helvetica", 22, "bold"), text_color=DARK_GRAY, wraplength=600)
        self.main_q_label.pack(pady=40)

        # Options Grid
        self.ans_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.ans_frame.pack(pady=10)

        self.buttons = []
        for i in range(4):
            btn = ctk.CTkButton(self.ans_frame, text="", width=260, height=55, fg_color=WHITE, 
                               text_color=DARK_GRAY, border_width=2, border_color="#D5DBDB",
                               font=("Helvetica", 15, "bold"), corner_radius=15, 
                               command=lambda i=i: self.check_answer(i))
            btn.grid(row=i//2, column=i%2, padx=15, pady=15)
            self.buttons.append(btn)

        # Bottom Buttons
        self.action_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.action_frame.pack(pady=20)

        self.skip_btn = ctk.CTkButton(self.action_frame, text="SKIP", fg_color=PURPLE, hover_color="#71368A", 
                                     width=130, height=45, corner_radius=22, font=("Helvetica", 14, "bold"), 
                                     command=self.skip_question)
        self.skip_btn.grid(row=0, column=0, padx=20)

        self.next_btn = ctk.CTkButton(self.action_frame, text="NEXT", fg_color=BLUE, hover_color="#1F618D", 
                                     width=130, height=45, corner_radius=22, font=("Helvetica", 14, "bold"), 
                                     state="disabled", command=self.next_question)
        self.next_btn.grid(row=0, column=1, padx=20)

        self.restart_btn = ctk.CTkButton(self.container, text="RESTART QUIZ", fg_color=GREEN, 
                                        width=200, height=50, corner_radius=25, font=("Helvetica", 18, "bold"), 
                                        command=self.start_game)

    def start_game(self):
        self.lives = 3
        self.correct_count = 0
        self.incorrect_count = 0
        self.skipped_count = 0
        self.current_q_index = 0
        self.questions = self.questions_data 
        
        self.restart_btn.pack_forget()
        self.ans_frame.pack(pady=10)
        self.action_frame.pack(pady=20)
        self.lives_label.configure(text=f"❤️ {self.lives}")
        self.load_question()

    def load_question(self):
        if self.current_q_index < len(self.questions) and self.lives > 0:
            self.next_btn.configure(state="disabled")
            self.skip_btn.configure(state="normal")
            for btn in self.buttons:
                btn.configure(fg_color=WHITE, state="normal", border_color="#D5DBDB", text_color=DARK_GRAY)
            
            q_data = self.questions[self.current_q_index]
            self.main_q_label.configure(text=q_data["q"])
            
            for i, option in enumerate(q_data["options"]):
                self.buttons[i].configure(text=option)

            self.timer_seconds = 15
            self.timer_running = True
            self.update_timer()
        else:
            self.end_game()

    def update_timer(self):
        if self.timer_running and self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_label.configure(text=str(self.timer_seconds))
            self.after(1000, self.update_timer)
        elif self.timer_seconds == 0 and self.timer_running:
            self.skip_question()

    def check_answer(self, idx):
        if not self.timer_running: return
        self.timer_running = False
        
        selected = self.buttons[idx].cget("text")
        correct_ans = self.questions[self.current_q_index]["ans"]

        for btn in self.buttons: btn.configure(state="disabled")

        if selected == correct_ans:
            self.correct_count += 1
            self.buttons[idx].configure(fg_color=GREEN, border_color=GREEN, text_color=WHITE)
        else:
            self.incorrect_count += 1
            self.lives -= 1
            self.buttons[idx].configure(fg_color=RED, border_color=RED, text_color=WHITE)
            for btn in self.buttons:
                if btn.cget("text") == correct_ans:
                    btn.configure(fg_color=GREEN, border_color=GREEN, text_color=WHITE)
            self.lives_label.configure(text=f"❤️ {self.lives}")

        self.next_btn.configure(state="normal")
        self.skip_btn.configure(state="disabled")

    def skip_question(self):
        self.timer_running = False
        self.skipped_count += 1
        self.next_question()

    def next_question(self):
        self.current_q_index += 1
        self.load_question()

    def end_game(self):
        self.timer_running = False
        self.ans_frame.pack_forget()
        self.action_frame.pack_forget()
        
        title = "WELL DONE! 👏" if self.correct_count >= 10 else "TRY AGAIN! 😟"

        stats = f"{title}\n\nCorrect: {self.correct_count}\nIncorrect: {self.incorrect_count}\nSkipped: {self.skipped_count}\n\nFinal Score: {self.correct_count}/15"
        self.main_q_label.configure(text=stats)
        self.restart_btn.pack(pady=30)

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()