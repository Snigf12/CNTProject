from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize, QEasingCurve, QPropertyAnimation

class AnimatedToggle(QWidget):
    def __init__(self):
        super().__init__()

        # Set up layout
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Set spacing to 0
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align to left

        # Create button and label
        self.button = QPushButton(" ", self)
        self.label = QLabel("Off", self)

        # Set minimum and maximum heights
        height = 30
        width = 30
        self.button.setFixedHeight(height)
        self.button.setFixedWidth(width)
        self.label.setFixedHeight(height)
        self.label.setFixedWidth(width)

        # Set initial styles
        self.button.setStyleSheet("background-color: white; margin: 0px; padding: 0px;")
        self.label.setStyleSheet("background-color: grey; color: black; margin: 0px; padding: 0px;")

        # Add button and label to layout
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)

        # Connect button click event
        self.button.clicked.connect(self.toggle)

        # Animation for button
        self.button_animation = QPropertyAnimation(self.button, b"geometry")
        self.button_animation.setDuration(200)
        self.button_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Animation for label
        self.label_animation = QPropertyAnimation(self.label, b"geometry")
        self.label_animation.setDuration(200)
        self.label_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on
        if self.is_on:
            # Move button to the right
            self.button_animation.setStartValue(self.button.geometry())
            self.button_animation.setEndValue(self.button.geometry().translated(self.button.width(), 0))

            # Move label to the left
            self.label_animation.setStartValue(self.label.geometry())
            self.label_animation.setEndValue(self.label.geometry().translated(-self.label.width(), 0))

            self.label.setText("On")
            self.label.setStyleSheet("background-color: green; color: white;")

        else:
            # Move button to the left
            self.button_animation.setStartValue(self.button.geometry())
            self.button_animation.setEndValue(self.button.geometry().translated(-self.button.width(), 0))

            # Move label to the right
            self.label_animation.setStartValue(self.label.geometry())
            self.label_animation.setEndValue(self.label.geometry().translated(self.label.width(), 0))

            self.label.setText("Off")
            self.label.setStyleSheet("background-color: grey; color: black;")

        self.button_animation.start()
        self.label_animation.start()

    def deleteLater(self):
        del self