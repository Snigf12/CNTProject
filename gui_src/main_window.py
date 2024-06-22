from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from .new_device import AddDeviceSettings

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('IoT Emulator')
        self.setGeometry(350, 350, 800, 430)
        
        # Create a scroll area for the main window layout
        scroll_area = QScrollArea()
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll_area)
        
        # Create a widget to contain the main window layout
        main_widget = QWidget()
        scroll_area.setWidgetResizable(True)  # Allow resizing of the contained widget
        scroll_area.setWidget(main_widget)

        # Create a layout for the main window
        self.layout = QVBoxLayout(main_widget)

        # Add the title label
        self.title_label = QLabel('IoT Emulator')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center horizontally
        self.layout.addStretch(1)  # Add stretch factor to push the title_label to the top
        
        # Initialize row count
        self.row_count = 0
        
        # Add initial row
        self.add_row()
        
        # Add button to add devices
        self.add_row_button = QPushButton('+ Add a Device', self)
        self.add_row_button.clicked.connect(self.add_row)
        self.layout.addWidget(self.add_row_button)

    def add_row(self):
        self.row_count += 1
        device_widget = AddDeviceSettings('Device'+str(self.row_count) + ':')
        self.layout.insertWidget(self.layout.count() - 1,device_widget)  # Add the row to the layout above the button