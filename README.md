IDL Debate Hackathon ‘25

Welcome to the IDL Debate Hackathon ‘25 repository — an AI-powered debate simulator for generating, adjudicating, and voicing debates with realism and educational value.

Project Overview

This project simulates formal debates, leveraging AI for both argument generation and adjudication, and provides a seamless, interactive experience with real-time speech synthesis and a modern web interface.

Requirements
To run this project locally, install the following Python packages:
•	Flask
•	Flask-SocketIO
•	pyttsx3
•	eventlet
•	pypiwin32 (Required only for TTS on Windows)
Install all dependencies with:
pip install flask flask-socketio pyttsx3 eventlet pypiwin32

Features
•	Supports BP & AP Debate Formats: Run British and Asian Parliamentary simulations out of the box.
•	AI Speech Generation: Instantly generates FOR and AGAINST arguments using advanced language models.
•	Automated Adjudication: Disputes are judged by custom AI logic for fairness and learning.
•	Real-Time Streaming: Live, incremental debate text updates via WebSocket with Flask-SocketIO.
•	Offline Voice Synthesis: Uses pyttsx3 to convert speeches to natural audio, alternating speaker voices for realism.
•	Smart Cleanup: Automatically removes audio/transcript files on refresh to keep content fresh.
•	Modern UI: Sleek, minimalist interface with progress bars and responsive audio controls.
•	Buffering for Audio Playback: Ensures speech audio is preloaded for uninterrupted listening.

Team Members
•	Ashi Jain
•	Raghav Anthwal
•	Shashwati Chandra

Built With
•	Python + Flask for fast backend development
•	WebSockets (Flask-SocketIO) for real-time updates
•	AI LLMs for argument generation and adjudication
•	pyttsx3 for reliable, offline TTS
•	HTML/CSS/JS for a polished frontend

🛡 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute with attribution.
Created to promote intelligent, structured debate for education and innovation.
