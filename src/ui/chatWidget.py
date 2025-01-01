from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ChatBrowser(QScrollArea):
    """Widget to display chat messages in a scrollable area."""

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins

        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setWidget(self.container)
        self.setWidgetResizable(True)
        self.setFixedSize(460, 480)  # Adjusted size to match parent

    def add_message(self, message: str, is_user: bool):
        """Add a new message to the chat."""
        label = QLabel(message)
        label.setWordWrap(True)  # Allow text wrapping
        label.setAlignment(
            Qt.AlignmentFlag.AlignRight if is_user else Qt.AlignmentFlag.AlignLeft
        )

        # Style the message differently based on sender
        if is_user:
            label.setStyleSheet(
                "background-color: #DCF8C6; padding: 10px; border-radius: 5px;"
            )
        else:
            label.setStyleSheet(
                "background-color: #FFF; padding: 10px; border-radius: 5px;"
            )

        # Add the message to the layout
        self.layout.addWidget(label)

        # Auto-scroll to the bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class TextInput(QTextEdit):
    """Text input box for typing messages."""

    def __init__(self):
        super().__init__()
        # Set fixed size for input box
        self.setFixedSize(460, 140)

    returnPressed = pyqtSignal()  # Signal emitted when Enter is pressed

    def keyPressEvent(self, event):
        """Emit `returnPressed` when Enter is pressed (Shift+Enter inserts a newline)."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                super().keyPressEvent(event)  # Add a new line
            else:
                self.returnPressed.emit()  # Emit the signal for Enter
        else:
            super().keyPressEvent(event)


class Prompt(QWidget):
    """Widget that contains the text input box."""

    def __init__(self):
        super().__init__()
        self.input = TextInput()

        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.setContentsMargins(0, 5, 5, 5)  # Consistent margins
        self.setLayout(layout)

        self.setFixedSize(460, 150)  # Adjusted size to match parent

    def get_input(self) -> TextInput:
        """Return the text input widget."""
        return self.input
