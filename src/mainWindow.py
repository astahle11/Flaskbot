from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from ui.chatWidget import ChatBrowser, Prompt

class MainWindow(QMainWindow):
    """Main application window for the chat app."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("mainWindow.py")
        self.setFixedSize(480, 650)  # Use fixed size to match components

        # Create the chat display and input box
        self.chat_browser = ChatBrowser()
        self.prompt = Prompt()

        # Connect the input box's signal to the message handler
        self.prompt.get_input().returnPressed.connect(self.send_message)

        # Arrange the chat browser and prompt vertically
        layout = QVBoxLayout()
        layout.setSpacing(0)  # Remove spacing between widgets
        layout.setContentsMargins(10, 10, 10, 10)  # Add consistent margins
        layout.addWidget(self.chat_browser)
        layout.addWidget(self.prompt)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align everything to the top

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_message(self):
        """Handle sending a message."""
        # Get the user's input
        text = self.prompt.get_input().toPlainText().strip()
        if text:
            # Display the user's message
            self.chat_browser.add_message(text, is_user=True)

            # Simulate a reply (for testing)
            self.chat_browser.add_message(f"You said: {text}", is_user=False)

            # Clear the input box
            self.prompt.get_input().clear()