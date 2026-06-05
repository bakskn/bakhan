"""
================================================================================
                  TRUE KUNDALI DECODER (AI-POWERED)
        Single Kundali + Match + Muhurtha + Transit + Numerology + Career + Health
              Hindu + Islamic + Roman + Mayan Civilizations Mix
                    Developed by - B A KHAN (+91-9935310660)
================================================================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
import datetime as dt
from google import genai
import pyperclip
import qrcode
from PIL import Image, ImageTk

# ========== API SETUP ==========
API_KEY = "AQ.Ab8RN6LXgM2CW0uj28o5ZBZnts3NNQStWra6tgXcyrkgcFWB1w"
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

class TrueKUNDALIDecoder:
    def __init__(self, root):
        self.root = root
        self.root.title("True KUNDALI Decoder (AI-Powered) | Developed by B A KHAN")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#0F0F1A')
        
        # Colors
        self.bg_dark = '#0F0F1A'
        self.bg_light = '#1A1A2E'
        self.gold = '#FFD700'
        self.saffron = '#FF9933'
        self.white = '#FFFFFF'
        
        # Nakshatras
        self.nakshatras = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
        
        self.current_data = {}
        self.mode = tk.StringVar(value="single")
        self.create_gui()
    
    def create_gui(self):
        # Banner - Fixed height, QR inside
        banner = tk.Frame(self.root, bg=self.bg_light, height=140)
        banner.pack(fill=tk.X)
        banner.pack_propagate(False)
        
        # QR Code - Top Right Corner (Always Visible)
        qr_frame = tk.Frame(banner, bg=self.bg_light)
        qr_frame.pack(side=tk.RIGHT, padx=15, pady=5)
        
        upi_string = "upi://pay?pa=9935310660@upi&pn=B%20A%20Khan&am=100&cu=INR"
        qr_img = qrcode.make(upi_string)
        qr_img = qr_img.resize((75, 75))
        self.qr_photo = ImageTk.PhotoImage(qr_img)
        
        qr_label = tk.Label(qr_frame, image=self.qr_photo, bg=self.bg_light, cursor="hand2")
        qr_label.pack()
        qr_label.bind("<Button-1>", lambda e: self.copy_upi())
        
        tk.Label(qr_frame, text="SCAN TO PAY", font=('Segoe UI', 7, 'bold'), bg=self.bg_light, fg=self.gold).pack()
        tk.Label(qr_frame, text="स्वेच्छित दक्षिणा", font=('Nirmala UI', 8, 'bold'), bg=self.bg_light, fg=self.saffron).pack()
        
        # Title Frame
        title_frame = tk.Frame(banner, bg=self.bg_light)
        title_frame.pack(pady=8)
        
        tk.Label(title_frame, text="🔱 TRUE KUNDALI DECODER (AI-POWERED) 🔱", 
                font=('Segoe UI', 22, 'bold'), bg=self.bg_light, fg=self.gold).pack()
        
        tk.Label(title_frame, text="🌍 हिंदू · इस्लामिक · रोमन · माया — चारों सभ्यताओं के ज्योतिष का अद्वितीय संगम 🌎", 
                font=('Segoe UI', 10, 'italic'), bg=self.bg_light, fg=self.saffron).pack(pady=2)
        
        tk.Label(title_frame, text="Single Kundali | Match | Muhurtha | Transit | Numerology | Career | Health", 
                font=('Segoe UI', 9), bg=self.bg_light, fg='#B8B8B8').pack()
        
        dev_frame = tk.Frame(title_frame, bg=self.bg_light)
        dev_frame.pack(pady=2)
        
        tk.Label(dev_frame, text="Developed by - ", font=('Segoe UI', 9), bg=self.bg_light, fg='#B8B8B8').pack(side=tk.LEFT)
        tk.Label(dev_frame, text="B A KHAN", font=('Segoe UI', 10, 'bold'), bg=self.bg_light, fg=self.gold).pack(side=tk.LEFT)
        tk.Label(dev_frame, text="(+91-9935310660)", font=('Segoe UI', 9), bg=self.bg_light, fg=self.saffron).pack(side=tk.LEFT, padx=5)
        
        # Main container
        main = tk.Frame(self.root, bg=self.bg_dark)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left Panel - Input
        left = tk.Frame(main, bg=self.bg_light, relief=tk.RAISED, bd=2)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,20), ipadx=20, ipady=15)
        
        # Mode Selection
        mode_frame = tk.Frame(left, bg=self.bg_light)
        mode_frame.pack(pady=10)
        tk.Label(mode_frame, text="📌 Mode:", font=('Segoe UI', 12, 'bold'), bg=self.bg_light, fg=self.gold).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="Single (Only Me)", variable=self.mode, value="single", bg=self.bg_light, fg=self.white, selectcolor=self.bg_light, command=self.toggle_fields).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Match (Two Persons)", variable=self.mode, value="match", bg=self.bg_light, fg=self.white, selectcolor=self.bg_light, command=self.toggle_fields).pack(side=tk.LEFT, padx=10)
        
        # Person 1 Frame
        self.p1_frame = tk.LabelFrame(left, text="👤 PERSON 1 DETAILS", font=('Segoe UI', 12, 'bold'), bg=self.bg_light, fg=self.gold, bd=2, relief=tk.RIDGE)
        self.p1_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.p1_entries = {}
        fields1 = [("Full Name *:", "name1"), ("Date (DD/MM/YYYY) *:", "date1"), ("Time (HH:MM) *:", "time1"), ("Latitude *:", "lat1"), ("Longitude *:", "lon1"), ("Timezone (±HH:MM) *:", "tz1")]
        defaults1 = ["", "04/07/1996", "09:10", "19.0760", "72.8777", "+05:30"]
        
        for i, (label, key) in enumerate(fields1):
            f = tk.Frame(self.p1_frame, bg=self.bg_light)
            f.pack(pady=4, fill=tk.X, padx=5)
            tk.Label(f, text=label, width=22, anchor='w', bg=self.bg_light, fg=self.white).pack(side=tk.LEFT)
            e = tk.Entry(f, width=22, bg='#2A2A3E', fg=self.white)
            e.insert(0, defaults1[i])
            e.pack(side=tk.LEFT, padx=5)
            self.p1_entries[key] = e
        
        # Person 2 Frame (initially hidden)
        self.p2_frame = tk.LabelFrame(left, text="👤 PERSON 2 DETAILS", font=('Segoe UI', 12, 'bold'), bg=self.bg_light, fg=self.gold, bd=2, relief=tk.RIDGE)
        
        self.p2_entries = {}
        fields2 = [("Full Name *:", "name2"), ("Date (DD/MM/YYYY) *:", "date2"), ("Time (HH:MM) *:", "time2"), ("Latitude *:", "lat2"), ("Longitude *:", "lon2"), ("Timezone (±HH:MM) *:", "tz2")]
        defaults2 = ["", "15/08/1998", "14:30", "19.0760", "72.8777", "+05:30"]
        
        for i, (label, key) in enumerate(fields2):
            f = tk.Frame(self.p2_frame, bg=self.bg_light)
            f.pack(pady=4, fill=tk.X, padx=5)
            tk.Label(f, text=label, width=22, anchor='w', bg=self.bg_light, fg=self.white).pack(side=tk.LEFT)
            e = tk.Entry(f, width=22, bg='#2A2A3E', fg=self.white)
            e.insert(0, defaults2[i])
            e.pack(side=tk.LEFT, padx=5)
            self.p2_entries[key] = e
        
        # Buttons
        btn_frame = tk.Frame(left, bg=self.bg_light)
        btn_frame.pack(pady=15)
        
        self.gen_btn = tk.Button(btn_frame, text="🔮 GENERATE ALL REPORTS", command=self.generate_all, bg=self.gold, fg='#0F0F1A', font=('Segoe UI', 12, 'bold'), padx=20, pady=8)
        self.gen_btn.pack()
        
        self.copy_btn = tk.Button(btn_frame, text="📋 COPY ALL REPORTS", command=self.copy_all, bg=self.saffron, fg='#0F0F1A', font=('Segoe UI', 12, 'bold'), padx=20, pady=8, state='disabled')
        self.copy_btn.pack(pady=5)
        
        # Right Panel - Tabs
        right = tk.Frame(main, bg=self.bg_light)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tabs = ["📋 MY KUNDALI", "💑 MATCHING", "🕌 MUHURTHA", "🪐 TRANSIT", "🔢 NUMEROLOGY", "💼 CAREER", "❤️ HEALTH"]
        self.text_widgets = {}
        for tab in tabs:
            frame = tk.Frame(self.notebook, bg='#FFF8E7')
            self.notebook.add(frame, text=tab)
            txt = scrolledtext.ScrolledText(frame, font=('Nirmala UI', 11), wrap=tk.WORD, bg='#FFF8E7', fg='#1A1A2E', padx=15, pady=15)
            txt.pack(fill=tk.BOTH, expand=True)
            self.text_widgets[tab] = txt
        
        # Initial toggle
        self.toggle_fields()
    
    def toggle_fields(self):
        if self.mode.get() == "single":
            self.p2_frame.pack_forget()
        else:
            self.p2_frame.pack(fill=tk.X, pady=10, padx=10, after=self.p1_frame)
    
    def copy_upi(self):
        pyperclip.copy("9935310660@upi")
        messagebox.showinfo("UPI ID", "✅ UPI ID copied! Use any UPI app to pay.")
    
    def validate_fields(self):
        for key, entry in self.p1_entries.items():
            if not entry.get().strip():
                return False, f"Person 1: {key.replace('1','')} is required"
        
        if self.mode.get() == "match":
            for key, entry in self.p2_entries.items():
                if not entry.get().strip():
                    return False, f"Person 2: {key.replace('2','')} is required"
        
        return True, ""
    
    def get_house(self, lon, lagna):
        return int(((lon - lagna) % 360) / 30) + 1
    
    def get_nakshatra(self, lon):
        return self.nakshatras[int((lon * 27) / 360) % 27]
    
    def get_chart(self, date_str, time_str, lat, lon, tz):
        parts = date_str.split('/')
        formatted = f"{parts[2]}/{parts[1]}/{parts[0]}"
        dt_obj = Datetime(formatted, time_str, tz)
        pos = GeoPos(float(lat), float(lon))
        return Chart(dt_obj, pos)
    
    def call_ai(self, prompt):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            return response.text
        except Exception as e:
            return f"⚠️ AI सेवा व्यस्त है: {str(e)[:100]}"
    
    def generate_all(self):
        valid, msg = self.validate_fields()
        if not valid:
            messagebox.showerror("Validation Error", f"❌ {msg}\n\nAll fields are mandatory!")
            return
        
        try:
            self.gen_btn.config(text="⏳ GENERATING...", state='disabled')
            self.copy_btn.config(state='disabled')
            self.root.update()
            
            name1 = self.p1_entries['name1'].get().strip()
            date1 = self.p1_entries['date1'].get().strip()
            time1 = self.p1_entries['time1'].get().strip()
            lat1 = float(self.p1_entries['lat1'].get().strip())
            lon1 = float(self.p1_entries['lon1'].get().strip())
            tz1 = self.p1_entries['tz1'].get().strip()
            
            if self.mode.get() == "match":
                name2 = self.p2_entries['name2'].get().strip()
                date2 = self.p2_entries['date2'].get().strip()
                time2 = self.p2_entries['time2'].get().strip()
                lat2 = float(self.p2_entries['lat2'].get().strip())
                lon2 = float(self.p2_entries['lon2'].get().strip())
                tz2 = self.p2_entries['tz2'].get().strip()
            else:
                name2 = None
            
            chart1 = self.get_chart(date1, time1, lat1, lon1, tz1)
            if name2:
                chart2 = self.get_chart(date2, time2, lat2, lon2, tz2)
            
            planets1 = {p: chart1.get(getattr(const, p.upper())).lon for p in ['sun','moon','mars','mercury','jupiter','venus','saturn']}
            if name2:
                planets2 = {p: chart2.get(getattr(const, p.upper())).lon for p in ['sun','moon','mars','mercury','jupiter','venus','saturn']}
            lagna1 = chart1.get(const.ASC).lon
            if name2:
                lagna2 = chart2.get(const.ASC).lon
            age1 = dt.datetime.now().year - int(date1.split('/')[2])
            
            base_style = """
            महत्वपूर्ण: तुम्हारी पहचान एक सार्वभौमिक ज्योतिषी (Universal Astrologer) है।
            तुम हिंदू, इस्लामिक, रोमन और माया सभ्यताओं के ज्योतिष का मिश्रण हो।
            भाषा हिंदी होगी। अच्छे और बुरे दोनों पहलू बताओ।
            """
            
            prompt_kundali = f"""{base_style}
            {name1} के लिए विश्लेषण करो:
            ग्रह: {planets1}, लग्न: {lagna1:.1f}°, आयु: {age1}
            सरल हिंदी में बताओ: पिछला जन्म, वर्तमान, भविष्य"""
            
            if name2:
                moon1, moon2 = self.get_nakshatra(planets1['moon']), self.get_nakshatra(planets2['moon'])
                prompt_match = f"""{base_style}
                {name1} और {name2} का मिलान करो:
                {name1}: ग्रह {planets1}, चंद्र {moon1}
                {name2}: ग्रह {planets2}, चंद्र {moon2}
                गुना स्कोर, अनुकूलता, उपाय बताओ।"""
            else:
                prompt_match = "Single mode selected. No matching data available."
            
            prompt_muhurtha = f"{base_style}\n{name1} के लिए शुभ मुहूर्त बताओ।"
            prompt_transit = f"{base_style}\n{name1} के लिए गोचर विश्लेषण बताओ।"
            
            total = sum(int(d) for d in date1 if d.isdigit())
            lucky = total % 9 or 9
            prompt_num = f"{base_style}\n{name1}, जन्म {date1}, भाग्यांक {lucky} के अनुसार विश्लेषण करो।"
            prompt_career = f"{base_style}\nग्रह: {planets1}, लग्न: {lagna1:.1f}° के अनुसार करियर बताओ।"
            prompt_health = f"{base_style}\nग्रह: {planets1}, लग्न: {lagna1:.1f}° के अनुसार स्वास्थ्य बताओ।"
            
            for tab in self.text_widgets.values():
                tab.delete(1.0, tk.END)
                tab.insert(1.0, "🤖 AI सोच रहा है... 15-20 सेकंड लगेंगे")
            self.root.update()
            
            results = {}
            prompts = [prompt_kundali, prompt_match, prompt_muhurtha, prompt_transit, prompt_num, prompt_career, prompt_health]
            titles = list(self.text_widgets.keys())
            
            for title, prompt in zip(titles, prompts):
                self.text_widgets[title].delete(1.0, tk.END)
                self.text_widgets[title].insert(1.0, f"⏳ {title} जनरेट हो रहा है...")
                self.root.update()
                res = self.call_ai(prompt)
                self.text_widgets[title].delete(1.0, tk.END)
                self.text_widgets[title].insert(1.0, res)
                results[title] = res
                self.root.update()
            
            self.current_data = results
            self.copy_btn.config(state='normal')
            self.gen_btn.config(text="🔮 GENERATE ALL REPORTS", state='normal')
            messagebox.showinfo("Success", f"✅ {name1} के लिए सभी रिपोर्ट तैयार!")
            
        except Exception as e:
            self.gen_btn.config(text="🔮 GENERATE ALL REPORTS", state='normal')
            self.copy_btn.config(state='disabled')
            messagebox.showerror("Error", f"❌ {str(e)}\n\nकृपया सही जानकारी दर्ज करें")
    
    def copy_all(self):
        if not self.current_data:
            return
        text = ""
        for title, content in self.current_data.items():
            text += f"\n{'='*60}\n{title}\n{'='*60}\n{content}\n"
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "✅ सभी रिपोर्ट कॉपी हो गईं!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrueKUNDALIDecoder(root)
    root.mainloop()