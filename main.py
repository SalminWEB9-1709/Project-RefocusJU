import time
import threading
import json
import pygetwindow as gw
import tkinter as tk
from datetime import datetime
from plyer import notification


PRODUCTIVE = ["code", "vscode", "docs", "notepad", "notebookmla", "slack", "email"]

DISTRACTING = ["youtube", "facebook", "instagram", "tiktok", "whatsapp", "twitter","pinterest"]

STUDY_KEYWORDS = [
    "study", "lecture", "course", "tutorial", "math", "physics",
    "coding", "programming", "python", "education", "learn"
]

WARNING_TIME = 20
BLOCK_TIME = 40

DATA_FILE = "refocus_data.json"


current_window = None
start_time = time.time()

focus_time = 0
distract_time = 0
score = 0

distract_start = None
log = []


def classify(title):
    title = title.lower()

    # SPECIAL CASE: YouTube study mode
    if "youtube" in title:
        if any(word in title for word in STUDY_KEYWORDS):
            return "productive"
        else:
            return "distracting"

    if any(app in title for app in PRODUCTIVE):
        return "productive"
    elif any(app in title for app in DISTRACTING):
        return "distracting"
    else:
        return "neutral"
    
def classify(title):
    title = title.lower()

    if any(app in title for app in PRODUCTIVE):
        return "productive"
    elif any(app in title for app in DISTRACTING):
        return "distracting"
    else:
        return "neutral"

def save_data():
    data = {
        "focus_time": round(focus_time, 1),
        "distract_time": round(distract_time, 1),
        "score": score,
        "sessions": log
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def show_popup(app_name):
    popup = tk.Toplevel()
    popup.title("Distracted!")

    popup.geometry("300x150")
    popup.attributes("-topmost", True)

    label = tk.Label(
        popup,
        text=f"Stop wasting time!\n{app_name}",
        font=("Arial", 14),
        fg="red"
    )
    label.pack(expand=True)

    popup.after(3000, popup.destroy)

root = tk.Tk()
root.title("Refocus Tracker")
root.geometry("350x250")

app_label = tk.Label(root, text="App: ...", font=("Arial", 12))
app_label.pack(pady=5)

status_label = tk.Label(root, text="Status: ...", font=("Arial", 14))
status_label.pack(pady=5)

time_label = tk.Label(root, text="Focus: 0s | Distract: 0s", font=("Arial", 10))
time_label.pack(pady=5)

score_label = tk.Label(root, text="Score: 0", font=("Arial", 12))
score_label.pack(pady=5)


def tracker_loop():
    global current_window, start_time
    global focus_time, distract_time, score
    global distract_start

    while True:
        window = gw.getActiveWindow()
        title = window.title if window else "Unknown"

        # ===== Window Switch Tracking ===== #
        if current_window != title:
            end_time = time.time()
            duration = end_time - start_time

            category = classify(current_window or "")

            if category == "productive":
                focus_time += duration
                score += int(duration // 10) * 10

            elif category == "distracting":
                distract_time += duration
                score -= int(duration // 10) * 5

            log.append({
                "app": current_window,
                "category": category,
                "duration": round(duration, 1),
                "time": str(datetime.now())
            })

            current_window = title
            start_time = time.time()

       
        current_category = classify(title)

      
        if current_category == "distracting":

            if distract_start is None:
                distract_start = time.time()

            elapsed = time.time() - distract_start

            if elapsed > WARNING_TIME and elapsed < BLOCK_TIME:
                notification.notify(
                    title="GET BACK TO WORK!",
                    message=f"You've been wasting time on {title} for {int(elapsed)} seconds.",
                    timeout=3
                )

            elif elapsed >= BLOCK_TIME:
                notification.notify(
                    title="BLOCKED",
                    message=f"{title} is distracting!",
                    timeout=3
                )

                show_popup(title)

                try:
                    window.minimize()
                except:
                    pass

                distract_start = time.time()

        else:
      
            distract_start = None

       
        app_label.config(text=f"App: {title}")

        status_label.config(
            text=f"Status: {current_category.upper()}",
            fg="green" if current_category == "productive"
            else "red" if current_category == "distracting"
            else "orange"
        )

        time_label.config(
            text=f"Focus: {int(focus_time)}s | Distract: {int(distract_time)}s"
        )

        score_label.config(text=f"Score: {score}")

        time.sleep(1)

threading.Thread(target=tracker_loop, daemon=True).start()



def on_close():
    save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)


root.mainloop()
