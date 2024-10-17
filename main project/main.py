import tkinter as tk
from tkinter import Toplevel
from tkinter import ttk, messagebox
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import webbrowser
import json
import re
import hashlib
from PIL import Image, ImageTk
import string
import os



class MusicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Silence Of Symphony")
        self.iconbitmap("logo.ico")
        self.geometry("400x600")
        self.current_window = None
        self.user_data = {} 
        self.load_user_data()
        self.music_data = self.load_music_data()  
        self.show_login_page()
        

    def show_login_page(self):
        if self.current_window:
            self.current_window.destroy()

        self.current_window = LoginPage(self)
        self.current_window.pack(fill="both", expand=True)

    def show_register_page(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = RegisterPage(self)
    
    def show_verify_code_page(self, email, recovery_code):
        for widget in self.winfo_children():
            widget.destroy()
        verify_page = VerifyCodePage(self, email, recovery_code)
        verify_page.pack(expand=True, fill="both")
    
    def show_captcha_page(self, email, recovery_code):
        for widget in self.winfo_children():
            widget.destroy()
        captcha_page = CaptchaPage(self, email, recovery_code)  
        captcha_page.pack(expand=True, fill="both")

    def show_forgot_password_page(self):
        if self.current_window:
            self.current_window.destroy()  
        self.current_window = ForgotPasswordPage(self) 
        self.current_window.pack(expand=True, fill="both")

    def show_reset_password_page(self, email):
        for widget in self.winfo_children():
            widget.destroy()
        reset_password_page = ResetPasswordPage(self, email) 
        reset_password_page.pack(expand=True, fill="both")

    def show_main_page(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = MusicRecommender(self)

    
    def save_user_data(self):
        with open('user_data.txt', 'w') as f:
            for email, info in self.user_data.items():
                f.write(f"{info['username']},{info['name']},{info['lname']},{email},{info['password']}\n")
        
    def load_user_data(self):
        if os.path.exists('user_data.txt'):
            with open('user_data.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 5:  
                        username, name, lname, email, password = parts
                        self.user_data[email] = {'username': username, 'name': name, 'lname': lname, 'password': password}

                        
    def load_music_data(self):

        music_data = []

        music_data.append({"title": "Song 1", "artist": "Artist 1", "genre": "Rock"})
        music_data.append({"title": "Song 2", "artist": "Artist 2", "genre": "Pop"})
        music_data.append({"title": "Song 3", "artist": "Artist 3", "genre": "Jazz"})
        return music_data
    def pass_action(self):
        self.show_forgot_password_page()
    
def hash_password(password):
    # change to hash with sha256
        return hashlib.sha256(password.encode()).hexdigest()

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Login")
        self.pack(expand=True, fill="both")
        self.master.geometry("370x500")
        self.background_image = Image.open("guitar.png")
        self.background_image = self.background_image.resize((370, 500), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas = tk.Canvas(self, width=400, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        self.canvas.create_text(200, 70, text="SOS", font=("Arial", 24), fill="red")
        self.canvas.create_text(200, 110, text="Silence of symphony", font=("Arial", 16), fill="white")

        self.canvas.create_text(159, 208, text="User Name", font=("Arial", 16), fill="white")

        self.username_entry = tk.Entry(self, width=30)
        self.canvas.create_window(200, 230, window=self.username_entry)
        self.canvas.create_text(155, 278, text="Password", font=("Arial", 16), fill="white")

        self.password_entry = tk.Entry(self, show="*", width=30)
        self.canvas.create_window(200, 300, window=self.password_entry)

        self.show_password_btn = tk.Button(self.canvas, text="🙉", command=self.toggle_password_visibility, font=("Arial", 12), width=2)
        self.canvas.create_window(310, 300, window=self.show_password_btn)

        self.login_button = tk.Button(self, text="Login", font=("arial", 16), command=self.login, bg="green", fg="white")
        self.canvas.create_window(145, 350, window=self.login_button)

        self.register_button = tk.Button(self, text="Sign Up", font=("arial", 12), 
                                command=self.master.show_register_page, bg=self.cget('bg'), fg="green", relief="flat", highlightthickness=4,  
                                highlightbackground="green",  highlightcolor="green",width=10,  
                                )                           
        self.canvas.create_window(245, 350, window=self.register_button)

        self.forgot_password_button = tk.Button(
                                    self.canvas,
                                    text="Forgot Password?",
                                    command=lambda: self.master.show_forgot_password_page(),
                                    bg="#ADD8E6",  # رنگ پس‌زمینه دکمه
                                    fg="black",  # رنگ متن
                                    font=("Arial", 12),
                                    borderwidth=0,  # حاشیه دکمه
                                    activebackground="#87CEFA",  # رنگ پس‌زمینه فعال دکمه
                                    highlightthickness=0  # حذف حاشیه فعال
                                    )

        self.canvas.create_window(200, 400, window=self.forgot_password_button)

    def toggle_password_visibility(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.show_password_btn.config(text='🙈')  
        else:
            self.password_entry.config(show='*')
            self.show_password_btn.config(text='🙉')

    

    def login(self):
        user_name = self.username_entry.get().strip()  
        password = self.password_entry.get().strip()

        if not user_name or not password:
            messagebox.showerror("Login", "Please enter both username and password.")
            return

        if not os.path.exists('user_data.txt'):
            messagebox.showerror("Login", "User data file not found.")
            return

        # change pass entry to hash
        hashed_password = hash_password(password)

        with open('user_data.txt', 'r') as f:
            users = [line.strip().split(',') for line in f]

        user_found = False
        for user in users:
            # chek hashed pass and user name
            if len(user) == 5 and user[0] == user_name and user[4] == hashed_password:
                user_found = True
                break
                
        if user_found:
            self.master.show_main_page()  
        else:
            messagebox.showerror("Login", "Invalid username or password.")
    

class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Register")
        self.pack(expand=True, fill="both")
        self.master.geometry("350x480")
        
        # Background image
        self.background_image = Image.open("electric3.jpg")
        self.background_image = self.background_image.resize((380, 500), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Canvas for background
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.canvas.create_text(126, 40, text="User Name", font=("Arial", 12), fill="white")
        self.username_entry = tk.Entry(self, width=30)
        self.canvas.create_window(180, 60, window=self.username_entry)

        self.canvas.create_text(124, 100, text="First Name", font=("Arial", 12), fill="white")
        self.name_entry = tk.Entry(self, width=30)
        self.canvas.create_window(180, 120, window=self.name_entry)

        self.canvas.create_text(126, 160, text="Last Name", font=("Arial", 12), fill="white")
        self.lname_entry = tk.Entry(self, width=30)
        self.canvas.create_window(180, 180, window=self.lname_entry)

        self.canvas.create_text(108, 220, text="Email", font=("Arial", 12), fill="white")
        self.email_entry = tk.Entry(self, width=30)
        self.canvas.create_window(180, 240, window=self.email_entry)

        self.canvas.create_text(124, 280, text="Password", font=("Arial", 12), fill="white")
        self.password_entry = tk.Entry(self, show="*", width=30)
        self.canvas.create_window(180, 300, window=self.password_entry)

        self.canvas.create_text(150, 340, text="Confirm Password", font=("Arial", 12), fill="white")
        self.confirm_password_entry = tk.Entry(self, show="*", width=30)
        self.canvas.create_window(180, 360, window=self.confirm_password_entry)

        self.sign_up_button = tk.Button(self, text="Sign Up >", command=self.register, font=("Arial", 12), bg="green", fg="white")
        self.canvas.create_window(230, 415, window=self.sign_up_button)

        self.back_to_login_button = tk.Button(self, text="< Back", command=self.master.show_login_page, font=("Arial", 12), bg="red", fg="white")
        self.canvas.create_window(120, 415, window=self.back_to_login_button)

    def hash_password(self, password):
        # هش کردن پسورد با استفاده از SHA-256
        return hashlib.sha256(password.encode()).hexdigest()
    def register(self):
        name = self.name_entry.get()
        lname = self.lname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        username = self.username_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # chek all box to be full
        if not name or not lname or not email or not username or not password or not confirm_password:
            messagebox.showerror("Register", "All fields are required.")
            return

       
        if password != confirm_password:
            messagebox.showerror("Register", "Passwords do not match.")
            return

        
        if len(password) < 8:
            messagebox.showerror("Register", "Password must be at least 8 characters long.")
            return

        # chek email with regx
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Register", "Invalid email format!")
            return

        # chek email exist
        if os.path.exists('user_data.txt'):
            with open('user_data.txt', 'r') as f:
                for line in f:
                    existing_email = line.strip().split(',')[3]  # email in index 4
                    if existing_email == email:
                        messagebox.showerror("Register", "Invalid email!")
                        return

        # change pass to hash
        hashed_password = self.hash_password(password)

        # save user data
        registration_info = f"{username},{name},{lname},{email},{hashed_password}\n"
        try:
            with open('user_data.txt', 'a') as f:
                f.write(registration_info)
            messagebox.showinfo("Register", "Registration successful!")
            self.master.show_login_page()  # back to login
        except Exception as e:
            messagebox.showerror("Register", f"Error saving data: {e}")


class MusicRecommender(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Music Recommender")
        self.master.geometry("450x500")

        # Load songs database
        self.file_path = "mbti_songs.xlsx"  # Adjust the path as necessary
        self.songs_database = self.load_songs_database(self.file_path)

        # Create canvas for background
        self.canvas = tk.Canvas(self.master, width=450, height=500)
        self.canvas.pack(fill="both", expand=True)

        # Load and resize background image to fit window size
        self.bg_image = Image.open("electric2.jpg")  # Adjust path as necessary
        self.bg_image = self.bg_image.resize((450, 500), Image.LANCZOS)  # Fit to window
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # MBTI Type selection
        self.mbti_label = tk.Label(self.master, text="Select MBTI Type:", bg="lightblue", font=("Arial", 12))
        self.canvas.create_window(225, 40, window=self.mbti_label)

        self.mbti_combobox = ttk.Combobox(self.master, values=list(self.songs_database.keys()))
        self.canvas.create_window(225, 80, window=self.mbti_combobox)

        self.mbti_info_button = tk.Button(self.master, text="❓", command=self.show_mbti_info, bg="yellow", borderwidth=0, font=("Arial", 13))
        self.canvas.create_window(320, 40, window=self.mbti_info_button)

        # Checkbox for genres, instruments, and moods
        self.genres = ["Pop", "Indie", "Folk", "Rock", "R&B", "Funk"]
        self.instruments = ["Symphonic", "Piano", "Guitar", "Drums", "Various" , "Violin" ]
        self.moods = ["Happy", "Sad", "Energetic", "Calm", "Romantic", "Nostalgic" ]

        self.frame_genre, self.genre_vars = self.create_checkbox_frame("Select Genre:", self.genres, x_position=80, y_position=230)
        self.frame_instrument, self.instrument_vars = self.create_checkbox_frame("Select Instrument:", self.instruments, x_position=230, y_position=230)
        self.frame_mood, self.mood_vars = self.create_checkbox_frame("Select Mood:", self.moods, x_position=380, y_position=230)
        

        # Suggest and Clear All buttons
        self.suggest_button = tk.Button(self.master, text="Suggest Music", command=self.on_suggest, bg='green', fg='white', font=("Arial", 15))
        self.canvas.create_window(140, 400, window=self.suggest_button)

        self.clear_button = tk.Button(self.master, text="Clear All", command=self.clear_all, bg='red', fg='white', font=("Arial", 15))
        self.canvas.create_window(360, 400, window=self.clear_button)

        self.about_button = tk.Button(text="about me", command=self.about_action, bg="blue", fg="white")
        self.canvas.create_window(410, 30, window=self.about_button) 

        self.back_button = tk.Button(
            self.master,
            text="close",
            command=self.go_back_to_login,
            font=("Arial", 12),
            bg="red",
            fg="white"
        )
        self.canvas.create_window(415, 70, window=self.back_button)
    
    def go_back_to_login(self):
        self.master.destroy()  # این خط صفحه فعلی را می‌بندد
        self.master.show_login_page()
    # Function to create checkbox frames
    def create_checkbox_frame(self, label_text, options, x_position, y_position):
        frame = tk.Frame(self.master, bg="lightgray")
        self.canvas.create_window(x_position, y_position, window=frame)

        label = tk.Label(frame, text=label_text, bg="lightgray", font=("Arial", 10))
        label.pack(anchor='w')

        vars = []
        for option in options:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(frame, text=option, variable=var, bg="lightgray", font=("Arial", 10))
            checkbox.pack(anchor='w')
            vars.append(var)

        return frame, vars

    def load_songs_database(self, file_path):
        try:
            mbti_songs_df = pd.read_excel(file_path)
            songs_database = {}
            for index, row in mbti_songs_df.iterrows():
                mbti_type = row['MBTI']
                song_info = (row['Song'], row['Genre'], row['Instrument'], row.get('Mood', ''))  # Mood added

                if mbti_type not in songs_database:
                    songs_database[mbti_type] = []
                songs_database[mbti_type].append(song_info)
            return songs_database
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the songs database: {str(e)}")
            return {}

    def on_suggest(self):
        selected_mbti = self.mbti_combobox.get()
        if not selected_mbti:
            messagebox.showwarning("Error", "Please select your MBTI type.")
            return

        selected_genres = [self.genres[i] for i, var in enumerate(self.genre_vars) if var.get()]
        selected_instruments = [self.instruments[i] for i, var in enumerate(self.instrument_vars) if var.get()]
        selected_moods = [self.moods[i] for i, var in enumerate(self.mood_vars) if var.get()]

        filtered_songs = self.filter_songs(selected_mbti, selected_genres, selected_instruments, selected_moods)

        if not filtered_songs:
            messagebox.showwarning("Error", "No songs match your selections.")
            return

        # Sort songs alphabetically by song name
        sorted_songs = sorted(filtered_songs, key=lambda x: x[0])

        # Display results
        self.show_results(sorted_songs)

    

    def filter_songs(self, mbti_type, genres, instruments, moods):
        filtered_songs = []

        # Get songs based on selected MBTI type
        if mbti_type in self.songs_database:
            for song in self.songs_database[mbti_type]:
                if ((not genres or song[1] in genres) and
                        (not instruments or song[2] in instruments) and
                        (not moods or song[3] in moods)):
                    filtered_songs.append(song)

        return filtered_songs

    def show_results(self, sorted_songs):
        result_window = tk.Toplevel()
        result_window.title("Music Suggestions")
        result_window.geometry("400x300")
        result_window.configure(bg="lightgray")

        result_text = tk.Text(result_window, wrap=tk.WORD, bg="white", font=("Arial", 12))
        result_text.pack(expand=True, fill=tk.BOTH)

        for i, song in enumerate(sorted_songs, 1):
            result_text.insert(tk.END, f"{i}. {song[0]} (Genre: {song[1]}, Instrument: {song[2]}, Mood: {song[3]})\n")

        result_text.config(state=tk.DISABLED)  # Make text widget read-only

    def clear_all(self):
        self.mbti_combobox.set('')
        self.search_entry.delete(0, tk.END)
        self.add_search_placeholder(None)  # Reset placeholder
        for var in self.genre_vars + self.instrument_vars + self.mood_vars:
            var.set(False)

    def show_mbti_info(self):
        mbti_description = (
        "The Myers-Briggs Type Indicator (MBTI) is a personality assessment tool\n\n"
        "that categorizes individuals into 16 distinct personality types based on their\n\n"
        "preferences in four dichotomies:"
    )
    
        response = messagebox.askyesno("MBTI Information", mbti_description + "\n\nDo you want to open the MBTI information page?")
        if response:
            webbrowser.open("https://www.16personalities.com/")

    def about_action(self):
        self.about_window = tk.Toplevel(self.master)  
        self.about_window.title("About Me")

        self.canvas = tk.Canvas(self.about_window, width=425, height=340)
        self.canvas.pack(pady=10)

        about_text = (
            "Hello!\n\n"
            "I'm Ilya Hemmati, a Computer Science student.\n\n"
            "I share my projects and code on GitHub. \n\n"
            "and I'm passionate about developing useful software.\n\n"
            "This program processes music data and suggests songs\n\n"
            "based on user preferences.\n\n"
            "📧 Email: iliya.hemati.nia@gmail.com\n\n"
            "🌐 GitHub Profile:\n\n"
            "📥 Download Link:"
        )

        self.canvas.create_text(20, 20, text=about_text, fill="black", font=("Arial", 12), anchor="nw")

        self.github_link = self.canvas.create_text(228, 281, text="Visit My GitHub Profile", fill="blue", font=("Arial", 12), tags="github")
        self.canvas.tag_bind("github", "<Button-1>", self.open_github)

        self.canvas.tag_bind("github", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("github", "<Leave>", lambda e: self.canvas.config(cursor=""))

        self.download_link = self.canvas.create_text(210, 318, text="Download app", fill="blue", font=("Arial", 12), tags="download")
        self.canvas.tag_bind("download", "<Button-1>", self.open_download)

        self.canvas.tag_bind("download", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("download", "<Leave>", lambda e: self.canvas.config(cursor=""))


        translate_button = tk.Button(self.about_window, text="ترجمه به فارسی", command=self.show_farsi_translation, bg="blue", fg="white")
        translate_button.pack(pady=10)

        close_button = tk.Button(self.about_window, text="Close", command=self.about_window.destroy, bg="red", fg="white")
        close_button.pack(pady=20)

    def open_github(self, event):
        webbrowser.open("https://github.com/your-github-profile")

    def open_download(self, event):
        webbrowser.open("https://your-download-link.com")

    def show_farsi_translation(self):
        self.about_window.destroy()
        
        farsi_window = tk.Toplevel(self.master)
        farsi_window.title("ترجمه به فارسی")
    
        farsi_window.geometry("450x550")
    
        farsi_text = (
            "سلام!\n\n"
            ".من ایلیا همتی هستم، دانشجوی رشته کامپیوتر\n\n"
            ".شما میتوانید دیگر پروژه های من را در گیت هاب مشاهده کنید\n\n"
            ".و به توسعه نرم‌افزارهای کاربردی علاقه‌مند هستم\n\n"
            ".این برنامه داده‌های موسیقی را پردازش می‌کند\n\n"
            "و بر اساس ( سلیقه‌های کاربر، شخصیت و ...)\n\n"
            ".آهنگ‌ها را پیشنهاد می‌دهد\n\n"
            "📧 ایمیل:\n" 
            "iliya.hemati.nia@gmail.com\n\n"
            "🌐 مشاهده پروفایل گیت هاب من:\n\n\n"
            "📥 لینک دانلود برنامه:"
        )
    
        def open_github(event):
            webbrowser.open("https://github.com/your-github-profile")
    
        def open_download(event):
            webbrowser.open("https://your-download-link.com")
    
        self.canvas = tk.Canvas(farsi_window, width=365, height=500)
        self.canvas.pack(pady=10)
    
        self.canvas.create_text(20, 20, text=farsi_text, fill="black", font=("Arial", 12), anchor="nw", justify="center", width=360)
    
        self.github_link = self.canvas.create_text(190, 360, text="مشاهده پروفایل", fill="blue", font=("Arial", 14), tags="github")
        self.canvas.tag_bind("github", "<Button-1>", open_github)
    
        self.canvas.tag_bind("github", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("github", "<Leave>", lambda e: self.canvas.config(cursor=""))
    
        self.download_link = self.canvas.create_text(195, 415, text="دانلود برنامه", fill="blue", font=("Arial", 14), tags="download")
        self.canvas.tag_bind("download", "<Button-1>", open_download)
    
        self.canvas.tag_bind("download", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("download", "<Leave>", lambda e: self.canvas.config(cursor=""))
    
        close_farsi_button = tk.Button(farsi_window, text="بستن", command=farsi_window.destroy,bg="red", fg="white")
        self.canvas.create_window(190, 480, window=close_farsi_button)

class CaptchaPage(tk.Frame):
    def __init__(self, master, email, recovery_code):
        super().__init__(master)
        self.email = email
        self.recovery_code = recovery_code
        self.captcha_code = self.generate_captcha()  
        self.setup_ui()
        self.master.geometry("400x380")

    def setup_ui(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        title_label = tk.Label(self.canvas, text="Captcha Verification", font=("Arial", 24), bg="white")
        self.canvas.create_window(200, 30, window=title_label)

        self.captcha_label = tk.Label(self.canvas, text=self.captcha_code, font=("Arial", 24), bg="white")
        self.canvas.create_window(200, 100, window=self.captcha_label)

        self.captcha_entry = tk.Entry(self.canvas, width=15, font=("Arial", 16), justify="center")
        self.canvas.create_window(200, 150, window=self.captcha_entry)

        self.submit_button = tk.Button(self.canvas, text="Submit", command=self.verify_captcha , bg="green" , fg="white" , font=("Arial" , 14))
        self.canvas.create_window(200, 200, window=self.submit_button)

        self.reload_button = tk.Button(self.canvas, text=" reload 🔃 ", command=self.reload_captcha , font=("Arial" , 14) , bg="yellow")
        self.canvas.create_window(200, 250, window=self.reload_button)

    def generate_captcha(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def reload_captcha(self):
        self.captcha_code = self.generate_captcha()  
        self.captcha_label.config(text=self.captcha_code)  

    def verify_captcha(self):
        if self.captcha_entry.get() == self.captcha_code:
            messagebox.showinfo("Success", "Captcha verified successfully!")
            self.master.show_reset_password_page(self.email)
        else:
            messagebox.showerror("Error", "Invalid captcha. Please try again.")
            self.reload_captcha()  


class ForgotPasswordPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Forgot Password")
        self.pack(expand=True, fill="both")
        self.configure(bg="white")
        self.master.geometry("350x400")
        
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.icon_image = Image.open("resetpass.jpg")
        self.icon_image = self.icon_image.resize((250, 250), Image.LANCZOS)
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.canvas.create_image(185, 100, image=self.icon_photo)

        self.canvas.create_text(185, 230, text="Forgot Password", font=("Arial", 24), fill="black")

        email_frame = tk.Frame(self, bg="white")
        self.canvas.create_window(190, 290, window=email_frame)

        self.email_entry = tk.Entry(email_frame, width=21, font=("Arial", 16), fg="gray")
        self.email_entry.pack(side="left", padx=5)
        self.email_entry.insert(0, "Enter your email")

        self.email_entry.bind("<FocusIn>", self.on_entry_click)
        self.email_entry.bind("<FocusOut>", self.on_focus_out)

        self.back_button = tk.Button(self, text=" < Back ", command=self.master.show_login_page, font=("Arial", 15), bg="red", fg="white")
        self.canvas.create_window(110, 360, window=self.back_button)

        self.submit = tk.Button(self, text=" Submit > ", command=self.send_recovery_code, font=("Arial", 14), bg="green", fg="white")
        self.canvas.create_window(250, 360, window=self.submit)


    def on_entry_click(self, event):
        if self.email_entry.get() == "Enter your email":
            self.email_entry.delete(0, tk.END)  
            self.email_entry.config(fg='black')  

    def on_focus_out(self, event):
        if self.email_entry.get() == "":
            self.email_entry.insert(0, "Enter your email")
            self.email_entry.config(fg='gray')

    def send_recovery_code(self):
        to_email = self.email_entry.get().strip()

        if not to_email:
            messagebox.showerror("Error", "Please enter your email.")
            return

        # بررسی فرمت ایمیل
        if not re.match(r"[^@]+@[^@]+\.[^@]+", to_email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        
        # بررسی وجود ایمیل در داده‌ها
        if to_email not in self.master.user_data:
            messagebox.showerror("Error", "Invalid Email.")
            return

        recovery_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.master.user_data[to_email]['recovery_code'] = recovery_code

        try:
            self.send_email(to_email, recovery_code)
            messagebox.showinfo("Recovery", "Recovery code sent to your email.")
            self.master.show_verify_code_page(to_email, recovery_code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send recovery code: {e}")

    def send_email(self, to_email, recovery_code):
        sender_email = "aghayehemati2@gmail.com"
        sender_password = "ltsu ueyw cgns llat"  

        subject = "Your Recovery Code"
        body = f"Your recovery code is: {recovery_code}"

        msg = MIMEText(body)
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")

    

class VerifyCodePage(tk.Frame):
    def __init__(self, master, email, recovery_code):  
        super().__init__(master)
        self.email = email
        self.recovery_code = recovery_code  
        self.master.title("Verify Code")
        self.pack(expand=True, fill="both")
        self.configure(bg="white")
        self.master.geometry("350x430")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.icon_image = Image.open("emailicon.png")
        self.icon_image = self.icon_image.resize((300, 300), Image.LANCZOS)
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.canvas.create_image(185, 100, image=self.icon_photo)

        code_frame = tk.Frame(self, bg="white")
        self.canvas.create_window(180, 210, window=code_frame)

        self.code_entry = tk.Entry(code_frame, width=15, font=("Arial", 16), fg="gray")
        self.code_entry.pack(side="left", padx=5)
        self.code_entry.insert(0, "Enter code")

        self.code_entry.bind("<FocusIn>", self.on_entry_click)
        self.code_entry.bind("<FocusOut>", self.on_focus_out)

        self.verify_button = tk.Button(self, text="Verify", command=self.verify_code, font=("Arial", 14), bg="green", fg="white")
        self.canvas.create_window(125, 270, window=self.verify_button)

        self.back_button = tk.Button(self, text="Edit Email", command=self.go_back, font=("Arial", 14), bg="red", fg="white")
        self.canvas.create_window(220, 270, window=self.back_button)

        
   
    def go_back(self):
        self.destroy()  # بستن پنجره فعلی
        self.master.show_forgot_password_page()

    def on_entry_click(self, event):
        if self.code_entry.get() == "Enter code":
            self.code_entry.delete(0, "end")  
            self.code_entry.config(fg="black")

    def on_focus_out(self, event):
        if self.code_entry.get() == "":
            self.code_entry.insert(0, "Enter code")
            self.code_entry.config(fg="gray")

    def verify_code(self):
        entered_code = self.code_entry.get()
        if entered_code == self.recovery_code:
            self.master.show_captcha_page(self.email, self.recovery_code)
        else:
            messagebox.showerror("Error", "Invalid code. Please try again.")

class ResetPasswordPage(tk.Frame):
    def __init__(self, master, email):
        super().__init__(master)
        self.master.title("Reset Password")
        self.pack(expand=True, fill="both")
        self.configure(bg="white")
        self.email = email
        self.master.geometry("400x300")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.title_label = tk.Label(self.canvas, text="Reset Password", font=("Arial", 24), bg="white")
        self.canvas.create_window(200, 40, window=self.title_label)

        self.new_password_label = tk.Label(self.canvas, text="New Password", font=("Arial", 12), bg="white")
        self.canvas.create_window(190, 90, window=self.new_password_label)

        self.new_password_entry = tk.Entry(self.canvas, show="*", width=20)
        self.canvas.create_window(200, 120, window=self.new_password_entry)

        self.show_password_btn_new = tk.Button(self.canvas, text="🙉", command=self.toggle_new_password_visibility, font=("Arial", 12), width=2)
        self.canvas.create_window(280, 125, window=self.show_password_btn_new)

        self.confirm_new_password_label = tk.Label(self.canvas, text="Confirm New Password", font=("Arial", 12), bg="white")
        self.canvas.create_window(190, 160, window=self.confirm_new_password_label)

        self.confirm_new_password_entry = tk.Entry(self.canvas, show="*", width=20)
        self.canvas.create_window(200, 190, window=self.confirm_new_password_entry)

        self.show_password_btn_confirm = tk.Button(self.canvas, text="🙉", command=self.toggle_confirm_password_visibility, font=("Arial", 12), width=2)
        self.canvas.create_window(280, 195, window=self.show_password_btn_confirm)

        self.submit_button = tk.Button(self.canvas, text="Submit", command=self.reset_password, bg="green", fg="white", font=("Arial", 12))
        self.canvas.create_window(200, 240, window=self.submit_button)

    def toggle_new_password_visibility(self):
        if self.new_password_entry.cget('show') == '*':
            self.new_password_entry.config(show='')
            self.show_password_btn_new.config(text='🙈')  
        else:
            self.new_password_entry.config(show='*')
            self.show_password_btn_new.config(text='🙉') 

    def toggle_confirm_password_visibility(self):
        if self.confirm_new_password_entry.cget('show') == '*':
            self.confirm_new_password_entry.config(show='')
            self.show_password_btn_confirm.config(text='🙈')  
        else:
            self.confirm_new_password_entry.config(show='*')
            self.show_password_btn_confirm.config(text='🙉') 
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def reset_password(self):
        new_password = self.new_password_entry.get()
        confirm_new_password = self.confirm_new_password_entry.get()

        if not new_password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        if new_password == confirm_new_password:
            hashed_password = self.hash_password(new_password)  # هش کردن پسورد جدید
            self.master.user_data[self.email]['password'] = hashed_password  # ذخیره پسورد هش شده
            self.master.save_user_data()
            messagebox.showinfo("Success", "Password reset successful!")
            self.master.show_login_page() 
            self.destroy() 
        else:
            messagebox.showerror("Error", "Passwords do not match.")



if __name__ == "__main__":
    app = MusicApp()
    app.mainloop()
