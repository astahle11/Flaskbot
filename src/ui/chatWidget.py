from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


# ChatBrowser: Displays chat messages in a scrollable area
class ChatBrowser(QScrollArea):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        """Initialize the UI for the chat browser."""
        # Layout to stack chat messages vertically
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align messages to the top
        layout.setSpacing(0)  # No spacing between messages
        layout.setContentsMargins(0, 0, 0, 0)  # No margins around messages

        # Widget to contain the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Configure the scroll area
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def show_text(self, text, is_user_message):
        """Add a new chat message to the browser.

        Args:
            text (str): The message text.
            is_user_message (bool): True if the message is from the user, False otherwise.
        """
        chat_label = QLabel(text)
        chat_label.setWordWrap(True)  # Allow text to wrap
        chat_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )  # Allow text selection

        # Style based on message sender
        if is_user_message:
            chat_label.setStyleSheet("QLabel { padding: 1em; }")
            chat_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            chat_label.setStyleSheet("QLabel { background-color: #DDD; padding: 1em; }")
            chat_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Add the message to the layout
        self.widget().layout().addWidget(chat_label)

    def event(self, event):
        """Automatically scroll to the bottom when new messages are added."""
        if event.type() == 43:  # QEvent.LayoutRequest
            self.verticalScrollBar().setSliderPosition(
                self.verticalScrollBar().maximum()
            )
        return super().event(event)


# TextEditPrompt: A custom text input widget that supports detecting Enter key presses
class TextEditPrompt(QTextEdit):
    returnPressed = pyqtSignal()  # Signal emitted when Enter is pressed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_ui()

    def __init_ui(self):
        """Initialize the UI for the text edit prompt."""
        self.setStyleSheet("QTextEdit { border: 1px solid #AAA; }")

    def keyPressEvent(self, event):
        """Handle key presses to detect Enter/Shift+Enter."""
        if event.key() in (
            Qt.Key.Key_Enter,
            Qt.Key.Key_Return,
        ):  # Handle Enter/Return keys
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                # Allow Shift+Enter to add a new line
                super().keyPressEvent(event)
            else:
                # Emit returnPressed for regular Enter
                self.returnPressed.emit()
        else:
            super().keyPressEvent(event)


# Prompt: A wrapper for the TextEditPrompt with dynamic height adjustment
class Prompt(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        """Initialize the UI for the input prompt."""
        self.__text_edit = TextEditPrompt()
        self.__text_edit.textChanged.connect(
            self.update_height
        )  # Update height on text change

        # Set up a horizontal layout for the prompt
        layout = QHBoxLayout()
        layout.addWidget(self.__text_edit)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.setLayout(layout)

        # Initialize the height of the widget
        self.update_height()

    def update_height(self):
        """Adjust the height of the prompt based on content."""
        document = self.__text_edit.document()
        height = document.size().height()
        self.setMaximumHeight(
            int(height + document.documentMargin())
        )  # Add margin to the height

    def get_text_edit(self):
        """Return the TextEditPrompt for external access."""
        return self.__text_edit
