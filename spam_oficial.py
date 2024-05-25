import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, colorchooser
import random
import time
import pyautogui
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class SpammerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spammer App")
        self.usage_count = 0
        self.max_free_usage = 5

        self.create_widgets()

        # Product keys
        self.permanent_product_key = "120206"
        self.temporary_product_key = "060212"
        self.product_key_validity = 15 * 60  # 15 minutos em segundos
        self.is_paid_version = False

    def create_widgets(self):
        self.message_label = tk.Label(self.root, text="Mensagens de Spam (uma por linha):")
        self.message_label.pack()
        
        self.message_text = tk.Text(self.root, height=10, width=50)
        self.message_text.pack()
        
        self.interval_label = tk.Label(self.root, text="Intervalo entre mensagens (milissegundos):")
        self.interval_label.pack()
        
        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack()
        
        self.duration_label = tk.Label(self.root, text="Duração total do spam (segundos ou 'infinito'):")
        self.duration_label.pack()
        
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.pack()
        
        self.start_button = tk.Button(self.root, text="Iniciar Spammer", command=self.start_spamming)
        self.start_button.pack()
        
        self.stop_button = tk.Button(self.root, text="Parar Spammer", command=self.stop_spamming)
        self.stop_button.pack()
        
        self.activate_button = tk.Button(self.root, text="Ativar Versão Paga", command=self.activate_paid_features)
        self.activate_button.pack()

        self.create_paid_features_button()
        
        self.help_button = tk.Button(self.root, text="Ajuda", command=self.show_help)
        self.help_button.pack()
        
        self.feedback_button = tk.Button(self.root, text="Sugestões/Críticas/Bug Report", command=self.send_feedback)
        self.feedback_button.pack()

        self.stop_event = threading.Event()
    
    def start_spamming(self):
        if self.usage_count >= self.max_free_usage and not self.is_paid_version:
            messagebox.showwarning("Limite Alcançado", "Você atingiu o limite de 5 usos diários na versão gratuita.")
            return
        
        messages = self.message_text.get("1.0", tk.END).strip().split("\n")
        if not messages or (len(messages) == 1 and messages[0] == ''):
            messagebox.showwarning("Aviso", "Por favor, insira pelo menos uma mensagem de spam.")
            return
        
        interval = self.interval_entry.get().strip()
        if not interval.isdigit():
            messagebox.showwarning("Aviso", "Por favor, insira um intervalo válido em milissegundos.")
            return
        interval = int(interval)
        
        duration = self.duration_entry.get().strip()
        if duration.lower() == "infinito":
            duration = float("inf")
        elif not duration.isdigit():
            messagebox.showwarning("Aviso", "Por favor, insira uma duração válida em segundos ou 'infinito'.")
            return
        else:
            duration = int(duration)
        
        self.stop_event.clear()
        self.usage_count += 1
        
        spam_thread = threading.Thread(target=self.spam_messages, args=(messages, interval, duration))
        spam_thread.start()
    
    def spam_messages(self, messages, interval, duration):
        start_time = time.time()
        while not self.stop_event.is_set():
            if time.time() - start_time > duration:
                break
            
            current_focus = self.root.focus_get()
            if current_focus not in (self.message_text, self.interval_entry, self.duration_entry):
                message = random.choice(messages)
                pyautogui.typewrite(message)
                pyautogui.press("enter")
            
            time.sleep(interval / 1000)
    
    def stop_spamming(self):
        self.stop_event.set()
    
    def activate_paid_features(self):
        product_key = simpledialog.askstring("Ativar Versão Paga", "Digite a Product Key:")
        if product_key == self.permanent_product_key:
            self.is_paid_version = True
            messagebox.showinfo("Sucesso", "Versão paga ativada permanentemente!")
        elif product_key == self.temporary_product_key:
            self.is_paid_version = True
            self.root.after(self.product_key_validity * 1000, self.deactivate_paid_features)
            messagebox.showinfo("Sucesso", "Versão paga ativada por 15 minutos!")
        else:
            messagebox.showerror("Erro", "Product Key inválida!")
        if self.is_paid_version:
            self.enable_paid_features()
    
    def deactivate_paid_features(self):
        self.is_paid_version = False
        messagebox.showinfo("Expirado", "Sua versão paga temporária expirou.")
    
    def enable_paid_features(self):
        self.import_button.config(state="normal")
        self.bg_color_button.config(state="normal")
        self.save_log_button.config(state="normal")
        self.uppercase_button.config(state="normal")
        self.countdown_button.config(state="normal")
        self.randomize_button.config(state="normal")
        self.repeat_button.config(state="normal")
        self.emojis_button.config(state="normal")

    def create_paid_features_button(self):
        self.import_button = tk.Button(self.root, text="Importar Mensagens", command=self.import_messages, state="disabled")
        self.import_button.pack()

        self.bg_color_button = tk.Button(self.root, text="Escolher Cor de Fundo", command=self.choose_bg_color, state="disabled")
        self.bg_color_button.pack()

        self.save_log_button = tk.Button(self.root, text="Salvar Log", command=self.save_log, state="disabled")
        self.save_log_button.pack()

        self.uppercase_button = tk.Button(self.root, text="Transformar Mensagens em Maiúsculas", command=self.uppercase_messages, state="disabled")
        self.uppercase_button.pack()

        self.countdown_button = tk.Button(self.root, text="Contagem Regressiva para Spam", command=self.countdown_to_spam, state="disabled")
        self.countdown_button.pack()

        self.randomize_button = tk.Button(self.root, text="Aleatorizar Ordem das Mensagens", command=self.randomize_messages, state="disabled")
        self.randomize_button.pack()

        self.repeat_button = tk.Button(self.root, text="Repetir Mensagens X Vezes", command=self.repeat_messages, state="disabled")
        self.repeat_button.pack()

        self.emojis_button = tk.Button(self.root, text="Adicionar Carinhas às Mensagens", command=self.add_emojis, state="disabled")
        self.emojis_button.pack()

    def import_messages(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                messages = file.read()
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert(tk.END, messages)
    
    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.root.config(bg=color)
    
    def save_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.message_text.get("1.0", tk.END))
            messagebox.showinfo("Sucesso", "Log salvo com sucesso!")
    
    def uppercase_messages(self):
        messages = self.message_text.get("1.0", tk.END).strip().split("\n")
        uppercase_messages = [msg.upper() for msg in messages]
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert(tk.END, "\n".join(uppercase_messages))
    
    def countdown_to_spam(self):
        duration = simpledialog.askinteger("Contagem Regressiva", "Digite a duração da contagem regressiva em segundos:")
        if duration:
            for i in range(duration, 0, -1):
                self.message_label.config(text=f"Mensagens de Spam (contagem regressiva: {i})")
                self.root.update()
                time.sleep(1)
            self.message_label.config(text="Mensagens de Spam:")
            self.start_spamming()
    
    def randomize_messages(self):
        messages = self.message_text.get("1.0", tk.END).strip().split("\n")
        random.shuffle(messages)
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert(tk.END, "\n".join(messages))
    
    def repeat_messages(self):
        repeat_count = simpledialog.askinteger("Repetir Mensagens", "Digite o número de vezes para repetir cada mensagem:")
        if repeat_count:
            messages = self.message_text.get("1.0", tk.END).strip().split("\n")
            repeated_messages = [msg for msg in messages for _ in range(repeat_count)]
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert(tk.END, "\n".join(repeated_messages))
    
    def add_emojis(self):
        messages = self.message_text.get("1.0", tk.END).strip().split("\n")
        emoji_messages = [f"{msg} :)" for msg in messages]
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert(tk.END, "\n".join(emoji_messages))

    def show_help(self):
        help_text = (
            "Instruções:\n"
            "1. Insira as mensagens de spam (uma por linha).\n"
            "2. Defina o intervalo entre as mensagens em milissegundos.\n"
            "3. Defina a duração total do spam em segundos ou 'infinito'.\n"
            "4. Clique em 'Iniciar Spammer' para começar o spam.\n"
            "5. Clique em 'Parar Spammer' para parar o spam.\n"
            "6. Para acessar recursos adicionais, ative a versão paga."
        )
        messagebox.showinfo("Ajuda", help_text)
    
    def send_feedback(self):
        feedback = simpledialog.askstring("Sugestões/Críticas/Bug Report", "Digite sua mensagem:")
        if feedback:
            self.send_email(feedback)

    def send_email(self, feedback):
        try:
            email_sender = "your_email@gmail.com"
            email_password = "your_password"
            email_receiver = "qsphere.technologies@gmail.com"
            subject = "Spammer App: Sugestão / Crítica / Bug Report"
            message = f"Subject: {subject}\n\n{feedback}"
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, message)
            server.quit()
            
            messagebox.showinfo("Sucesso", "Sua mensagem foi enviada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar mensagem: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpammerApp(root)
    root.mainloop()
