import tkinter as tk
from tkinter import ttk, messagebox
import requests
import random
import socket
from urllib.parse import urlparse

# Stil sabitleri
BG_COLOR = "#2c3e50"
FG_COLOR = "#ecf0f1"
BUTTON_COLOR = "#3498db"
BUTTON_HOVER = "#2980b9"
ENTRY_COLOR = "#34495e"
RESULT_COLOR = "#16a085"
ERROR_COLOR = "#e74c3c"
SUCCESS_COLOR = "#2ecc71"

def query_ip():
    ip_address = entry.get().strip()
    if not validate_ip(ip_address):
        result_label.config(text="Geçersiz IP adresi!", fg=ERROR_COLOR, bg=BG_COLOR)
        return

    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        if response['status'] == 'success':
            country = response.get('country', 'Bilinmiyor')
            city = response.get('city', 'Bilinmiyor')
            lat = response.get('lat', 'Bilinmiyor')
            lon = response.get('lon', 'Bilinmiyor')
            isp = response.get('isp', 'Bilinmiyor')

            result_text = (
                f"IP Adresi: {ip_address}\n"
                f"Ülke: {country}\n"
                f"Şehir: {city}\n"
                f"Enlem: {lat}\n"
                f"Boylam: {lon}\n"
                f"ISP: {isp}"
            )
            
            result_label.config(
                text=result_text,
                fg=FG_COLOR, 
                bg=RESULT_COLOR,
                font=("Arial", 11, "bold")
            )
        else:
            result_label.config(text="IP adresi sorgulanamadı!", fg=ERROR_COLOR, bg=BG_COLOR)
    except Exception as e:
        result_label.config(text="Bir hata oluştu!", fg=ERROR_COLOR, bg=BG_COLOR)

def validate_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

def generate_random_ip():
    random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    entry.delete(0, tk.END)
    entry.insert(0, random_ip)

def generate_tc():
    tc = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(8)]
    tc.append((sum(tc[0:9:2]) * 7 - sum(tc[1:8:2])) % 10)
    tc.append((sum(tc[:10])) % 10)
    tc_label.config(text=f"Rastgele TC: {''.join(map(str, tc))}", fg=SUCCESS_COLOR)

def generate_name():
    first_names = ["Ali", "Veli", "Ayşe", "Fatma", "Mehmet", "Zeynep", "Can", "Ece", "Deniz", "Burak"]
    last_names = ["Yılmaz", "Kaya", "Demir", "Çelik", "Öztürk", "Koç", "Arslan", "Aslan", "Polat", "Güneş"]
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    name_label.config(text=f"Rastgele İsim: {name}", fg=SUCCESS_COLOR)

def get_ip_from_url():
    url = url_entry.get().strip()
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc if parsed_url.netloc else parsed_url.path
        ip_address = socket.gethostbyname(hostname)
        url_ip_label.config(text=f"URL IP Adresi: {ip_address}", fg=SUCCESS_COLOR)
    except Exception as e:
        url_ip_label.config(text="Geçersiz URL veya IP bulunamadı!", fg=ERROR_COLOR)

def on_enter(e):
    e.widget['background'] = BUTTON_HOVER

def on_leave(e):
    e.widget['background'] = BUTTON_COLOR

def create_button(parent, text, command):
    btn = ttk.Button(
        parent, 
        text=text, 
        command=command,
        style='TButton'
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

root = tk.Tk()
root.title("Kyronoid IP Sorgu Aracı")
root.geometry("500x700")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Stil ayarları
style = ttk.Style()
style.configure('TButton', font=('Arial', 11), background=BUTTON_COLOR, foreground=FG_COLOR)
style.map('TButton', background=[('active', BUTTON_HOVER)])

# Başlık
title_frame = tk.Frame(root, bg=BG_COLOR)
title_frame.pack(pady=20)

title_label = tk.Label(
    title_frame, 
    text="Kyronoid IP Sorgu Aracı", 
    font=("Arial", 18, "bold"), 
    fg=FG_COLOR, 
    bg=BG_COLOR
)
title_label.pack()

# IP Sorgu Bölümü
ip_frame = tk.LabelFrame(
    root, 
    text=" IP Sorgulama ", 
    font=("Arial", 12, "bold"), 
    fg=FG_COLOR, 
    bg=BG_COLOR,
    bd=2,
    relief=tk.GROOVE
)
ip_frame.pack(pady=10, padx=20, fill=tk.X)

tk.Label(
    ip_frame, 
    text="IP Adresi:", 
    font=("Arial", 11), 
    bg=BG_COLOR, 
    fg=FG_COLOR
).pack(anchor=tk.W, padx=10, pady=(5, 0))

entry = tk.Entry(
    ip_frame, 
    font=("Arial", 12), 
    width=30, 
    bg=ENTRY_COLOR, 
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    relief=tk.FLAT
)
entry.pack(pady=5, padx=10)

button_frame = tk.Frame(ip_frame, bg=BG_COLOR)
button_frame.pack(pady=5)

create_button(button_frame, "Sorgula", query_ip).pack(side=tk.LEFT, padx=5)
create_button(button_frame, "Rastgele IP", generate_random_ip).pack(side=tk.LEFT, padx=5)

result_label = tk.Label(
    ip_frame, 
    text="", 
    font=("Arial", 11), 
    bg=RESULT_COLOR, 
    fg=FG_COLOR,
    wraplength=450, 
    justify="left",
    padx=10,
    pady=10,
    relief=tk.GROOVE
)
result_label.pack(pady=10, padx=10, fill=tk.X)

# Araçlar Bölümü
tools_frame = tk.LabelFrame(
    root, 
    text=" Araçlar ", 
    font=("Arial", 12, "bold"), 
    fg=FG_COLOR, 
    bg=BG_COLOR,
    bd=2,
    relief=tk.GROOVE
)
tools_frame.pack(pady=10, padx=20, fill=tk.X)

create_button(tools_frame, "Rastgele TC Üret", generate_tc).pack(pady=5, fill=tk.X, padx=10)
tc_label = tk.Label(
    tools_frame, 
    text="", 
    font=("Arial", 11), 
    bg=BG_COLOR, 
    fg=FG_COLOR
)
tc_label.pack(pady=5)

create_button(tools_frame, "Rastgele İsim Üret", generate_name).pack(pady=5, fill=tk.X, padx=10)
name_label = tk.Label(
    tools_frame, 
    text="", 
    font=("Arial", 11), 
    bg=BG_COLOR, 
    fg=FG_COLOR
)
name_label.pack(pady=5)

# URL'den IP Bölümü
url_frame = tk.LabelFrame(
    tools_frame, 
    text=" URL'den IP Çözümleme ", 
    font=("Arial", 10, "bold"), 
    fg=FG_COLOR, 
    bg=BG_COLOR,
    bd=2,
    relief=tk.GROOVE
)
url_frame.pack(pady=10, padx=10, fill=tk.X)

url_entry = tk.Entry(
    url_frame, 
    font=("Arial", 11), 
    width=30, 
    bg=ENTRY_COLOR, 
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    relief=tk.FLAT
)
url_entry.pack(pady=5, padx=10, fill=tk.X)

create_button(url_frame, "IP Çözümle", get_ip_from_url).pack(pady=5, fill=tk.X, padx=10)
url_ip_label = tk.Label(
    url_frame, 
    text="", 
    font=("Arial", 11), 
    bg=BG_COLOR, 
    fg=FG_COLOR
)
url_ip_label.pack(pady=5)

# Footer
footer_label = tk.Label(
    root, 
    text="© 2023 Kyronoid IP Sorgu Aracı", 
    font=("Arial", 10), 
    fg=FG_COLOR, 
    bg=BG_COLOR
)
footer_label.pack(pady=20)

root.mainloop()