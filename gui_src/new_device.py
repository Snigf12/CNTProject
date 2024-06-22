from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QCheckBox
from PyQt6.QtCore import Qt
from .animated_toggle import AnimatedToggle

class AddDeviceSettings(QWidget):
    def __init__(self, label_name):
        super().__init__()
        self.initUI(label_name)

    def initUI(self, label_name):
        # Create a layout for the widget
        layout = QVBoxLayout(self)

        # Create a horizontal layout to contain the label and dropdown list and all the device configuration
        self.device_layout = QHBoxLayout()
        
        # Add a label for the device name
        device_label = QLabel(label_name)
        device_label.setStyleSheet("margin: 0px; padding: 0px;")
        self.device_layout.addWidget(device_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Create a dropdown list for protocol selection
        self.dropdownp = QComboBox()
        self.dropdownp.addItems(["Select a Protocol", "MQTT", "CoAP"])
        self.dropdownp.setStyleSheet("margin: 0px; padding: 0px;")
        self.device_layout.addWidget(self.dropdownp, alignment=Qt.AlignmentFlag.AlignLeft)

        # Create a dropdown list for sensor selection
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Select a Device", "Air Sensors", "Environmental Sensors","Water Sensors"])
        self.dropdown.currentIndexChanged.connect(self.updateCheckboxes)
        self.dropdown.setStyleSheet("margin: 0px; padding: 0px;")
        self.device_layout.addWidget(self.dropdown, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add the horizontal layout to the main vertical layout
        layout.addLayout(self.device_layout)

        # Create a layout for the checkboxes
        self.checkbox_layout = QVBoxLayout()
        self.device_layout.addLayout(self.checkbox_layout)

        # Initialize the label for the checkboxes
        self.checkbox_label = None
        self.toggle_button = None

        # Initialize an empty list to store checkboxes
        self.checkboxes = []

    def updateCheckboxes(self, index):
        # Clear existing checkboxes
        for checkbox in self.checkboxes:
            checkbox.setParent(None)
            checkbox.deleteLater()
        self.checkboxes.clear()

        # I clear the checkbox_label each time the dropdown list has changes
        # to update them again.
        if self.checkbox_label:
            self.checkbox_label.setParent(None)
            self.checkbox_label.deleteLater()
            self.checkbox_label = None

        # I clear the toggle_button each time the dropdown list has changes
        # to update them again.
        if self.toggle_button:
            self.toggle_button.setParent(None)
            self.toggle_button.deleteLater()
            self.toggle_button = None

        # Add label if it doesn't exist
        if not self.checkbox_label:
            self.checkbox_label = QLabel('Select the Sensors for the Device:')
            self.checkbox_layout.addWidget(self.checkbox_label)

        # Add new checkboxes based on the selected option
        if index == 0:  # Select Device
            # I clear the checkbox_label if the dropdown list is the default value
            # to update them again.
            if self.checkbox_label:
                self.checkbox_label.setParent(None)
                self.checkbox_label.deleteLater()
                self.checkbox_label = None

            # I clear the toggle_button if the dropdown list is the default value
            # to update them again.
            if self.toggle_button:
                self.device_layout.removeWidget(self.toggle_button)
                self.toggle_button.deleteLater()
                self.toggle_button = None

        if index == 1:  # Air Sensors
            #Add Checkboxes
            checkbox = QCheckBox("CO2 Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("CO Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("NO2 Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("O3 Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            if not self.toggle_button:
                # Now I add teh toggle button that will start the Docker with the device or create the Docker container
                # If the device doesn't exist.
                self.toggle_button = AnimatedToggle()
                self.device_layout.addWidget(self.toggle_button)
        elif index == 2:  # Env Sensors
            #Add Checkboxes
            checkbox = QCheckBox("Temperature and Humidity Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("Noise Level Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("Light Intensity Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            if not self.toggle_button:
                # Now I add teh toggle button that will start the Docker with the device or create the Docker container
                # If the device doesn't exist.
                self.toggle_button = AnimatedToggle()
                self.device_layout.addWidget(self.toggle_button)
        elif index == 3:  # Water Sensors
            #Add Checkboxes
            checkbox = QCheckBox("Turbidity Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("pH Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("Electric Conductivity Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            checkbox = QCheckBox("Disolved Oxygen Sensor")
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.checkbox_layout.addWidget(checkbox)
            if not self.toggle_button:
                # Now I add teh toggle button that will start the Docker with the device or create the Docker container
                # If the device doesn't exist.
                self.toggle_button = AnimatedToggle()
                self.device_layout.addWidget(self.toggle_button)