# Project-RefocusJU
This project was developed as a collaborative group effort by Salmon Newton Sangma and Salmin Janisha Sangma. Originally 
conceived as a productivity tool, we implemented several key enhancements and logic refinements to finalize it for our final project submission.


Project Overview
The Refocus Tracker is an automated productivity management system designed to monitor screen time and actively discourage digital distractions.
It functions as a background supervisor that categorizes user activity and intervenes when focus wavers.

How It Works: Step-by-Step
1. Environmental Setup
The project relies on three core frameworks: PyGetWindow for active window detection, Plyer for system-level notifications,
and Tkinter for the graphical user interface. These are integrated within a Python environment to allow for real-time monitoring.

3. Activity Classification
The system uses a classify() function to analyze the title of the active window. We defined specific lists:

Productive: Keywords like "vscode," "docs," and "notepad."

Distracting: Keywords like "facebook," "youtube," and "tiktok."

Study Keywords: A special logic layer (for YouTube) that identifies educational content vs. entertainment.

3. Real-Time Tracking & Scoring
Using a background thread, the app polls the active window every second. It calculates the duration spent on each task and updates a scoring system:

Focus Points: Users earn 10 points for every 10 seconds of productive work.

Penalty Points: Users lose 5 points for every 10 seconds of distraction.

4. Active Intervention (The Block System)
Unlike passive trackers, this project takes action. If a user remains on a distracting app for 20 seconds, t
he system sends a desktop notification. If the distraction continues for 40 seconds, the script triggers a "Distracted!" popup and
 automatically minimizes the distracting window to force the user back to work.

6. Data Logging
Upon closing the application, all session data—including specific app names, durations, and timestamps—is serialized into
a refocus_data.json file. This allows users to review their long-term productivity trends and habits.
