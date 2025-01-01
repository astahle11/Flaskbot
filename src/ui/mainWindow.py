from chatWidget import ChatBrowser, Prompt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# High-DPI support for better scaling on high-resolution screens
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)

# Set global font for the application
QApplication.setFont(QFont("Arial", 12))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        """Initialize the main window UI."""
        self.setWindowTitle("Chat Application")

        # Create prompt (input area) and chat browser (message display area)
        self.__prompt = Prompt()
        self.__text_edit = self.__prompt.get_text_edit()
        self.__text_edit.returnPressed.connect(
            self.__chat
        )  # Connect Enter key signal to chat handling
        self.__browser = ChatBrowser()

        # Layout to arrange the browser and prompt vertically
        layout = QVBoxLayout()
        layout.addWidget(self.__browser)
        layout.addWidget(self.__prompt)
        layout.setSpacing(0)

        # Set the main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.resize(600, 400)

        # Initial messages
        self.__browser.show_text("Write some text...", True)
        self.__browser.show_text("", False)

    def __chat(self):
        """Handle sending a message."""
        user_message = self.__text_edit.toPlainText().strip()
        if user_message:
            self.__browser.show_text(user_message, True)  # Display the user's message
            self.__browser.show_text(
                f'You said "{user_message}"', False
            )  # Echo the user's message
            self.__text_edit.clear()  # Clear the input area
