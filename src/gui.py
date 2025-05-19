from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QTextEdit, QLabel, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
import sys
import os
from main import VoiceAssistant

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.assistant = VoiceAssistant()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('S.U.N.N.Y - AI Assistant')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #0077ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0066cc;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 1px solid #0077ff;
                border-radius: 5px;
                font-family: 'Consolas';
                font-size: 14px;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #0077ff;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        
        # Add status display
        self.status_label = QLabel('S.U.N.N.Y Status: Ready')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Add output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setMinimumHeight(300)
        layout.addWidget(self.output_display)
        
        # Add input mode selector
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(['Voice Mode', 'Text Mode'])
        layout.addWidget(self.mode_selector)
        
        # Add input field for text mode
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your command here...")
        self.input_field.setMaximumHeight(100)
        layout.addWidget(self.input_field)
        
        # Add control buttons
        button_layout = QVBoxLayout()
        
        self.start_button = QPushButton('Start Assistant')
        self.start_button.clicked.connect(self.start_assistant)
        button_layout.addWidget(self.start_button)
        
        self.voice_auth_button = QPushButton('Setup Voice Authentication')
        self.voice_auth_button.clicked.connect(self.setup_voice_auth)
        button_layout.addWidget(self.voice_auth_button)
        
        self.send_button = QPushButton('Send Command')
        self.send_button.clicked.connect(self.send_command)
        button_layout.addWidget(self.send_button)
        
        layout.addLayout(button_layout)
        
        # Set window properties
        self.setMinimumSize(600, 800)
        self.center_window()
        
        # Initialize status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # Update every second

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def update_status(self):
        # Add dynamic status updates
        import psutil
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        self.status_label.setText(
            f'S.U.N.N.Y Status: Ready | CPU: {cpu}% | RAM: {memory}%'
        )

    def log_output(self, text):
        self.output_display.append(f"S.U.N.N.Y: {text}")

    def start_assistant(self):
        mode = self.mode_selector.currentText()
        self.log_output(f"Starting in {mode}")
        if mode == 'Voice Mode':
            self.start_voice_mode()
        else:
            self.start_text_mode()

    def setup_voice_auth(self):
        self.log_output("Setting up voice authentication...")
        self.assistant.record_voice_sample()
        self.log_output("Voice authentication setup complete!")

    def send_command(self):
        command = self.input_field.toPlainText().strip()
        if command:
            self.log_output(f"Command: {command}")
            response = self.assistant.get_chat_response(command)
            self.assistant.speak(response)
            self.log_output(f"Response: {response}")
            self.input_field.clear()

    def start_voice_mode(self):
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.log_output("Voice mode activated. Listening...")
        # Start voice recognition in a separate thread
        self.voice_thread = VoiceThread(self.assistant)
        self.voice_thread.response_signal.connect(self.handle_voice_response)
        self.voice_thread.start()

    def start_text_mode(self):
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.log_output("Text mode activated. Type your commands.")

    def handle_voice_response(self, response):
        self.log_output(response)

class VoiceThread(QThread):
    response_signal = pyqtSignal(str)
    
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        
    def run(self):
        while True:
            try:
                audio = self.assistant.recognizer.listen()
                if self.assistant.authenticator.verify_voice(audio):
                    command = self.assistant.recognizer.recognize(audio)
                    if command:
                        response = self.assistant.get_chat_response(command)
                        self.assistant.speak(response)
                        self.response_signal.emit(response)
            except Exception as e:
                self.response_signal.emit(f"Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = AssistantGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()