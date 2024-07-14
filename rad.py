#netx421@proton.me
#thanks for using x421 for your sdr needs!
#please share and use the code for your own needs
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QHBoxLayout, QMessageBox

class RadioApp(QWidget):
    def __init__(self):
        super().__init__()

        # Radio control elements
        self.frequency_label = QLabel("Frequency (MHz):")
        self.frequency_entry = QLineEdit()

        # Modulation type radio buttons
        self.am_radio = QRadioButton("AM")
        self.fm_radio = QRadioButton("FM")
        self.nfm_radio = QRadioButton("NFM")
        self.fm_radio.setChecked(True)  # Default to FM

        # Start/Stop button
        self.start_stop_button = QPushButton("Start Radio")

        # Feedback label
        self.feedback_label = QLabel("")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.frequency_label)
        layout.addWidget(self.frequency_entry)

        # Modulation type radio buttons layout
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.am_radio)
        radio_layout.addWidget(self.fm_radio)
        radio_layout.addWidget(self.nfm_radio)
        layout.addLayout(radio_layout)

        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.feedback_label)

        self.setLayout(layout)

        # Connect button click to start_stop_radio method
        self.start_stop_button.clicked.connect(self.start_stop_radio)

        # Variable to keep track of radio state
        self.is_radio_running = False

    def start_stop_radio(self):
        if self.is_radio_running:
            self.stop_radio()
        else:
            self.start_radio()

    def start_radio(self):
        # Get values from radio control elements
        frequency_entry_value = self.frequency_entry.text()

        # Check for empty frequency entry
        if not frequency_entry_value:
            self.feedback_label.setText("Please enter a frequency.")
            return

        # Determine selected modulation type
        modulation_type = "AM" if self.am_radio.isChecked() else "FM" if self.fm_radio.isChecked() else "NFM"

        # Build radio command
        if modulation_type == "AM":
            radio_command = f"rtl_fm -M am -f {frequency_entry_value}e6 -s 120k - | sox -t raw -r 120000 -b 16 -e signed-integer -c 1 - -t raw - lowpass 12k | play -q -r 120000 -t raw -e signed-integer -b 16 -c 1 -V1 -"
        else:
            radio_command = f"rtl_fm -f {frequency_entry_value}e6 -M {modulation_type} -s 200000 -r 32000 - | sox -t raw -r 44100 -b 16 -e signed-integer -c 1 - -t raw - lowpass 3k | play -q -r 32000 -t raw -e signed-integer -b 16 -c 1 -V1 -"

        try:
            # Run radio command
            self.radio_process = subprocess.Popen(radio_command, shell=True)
            # Display feedback about the radio operations
            self.feedback_label.setText(f"Starting radio with frequency: {frequency_entry_value} MHz, Modulation type: {modulation_type}")
            self.is_radio_running = True
            self.start_stop_button.setText("Stop Radio")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start radio: {str(e)}")

    def stop_radio(self):
        try:
            # Use pkill to stop the radio process
            subprocess.run(["pkill", "-f", "rtl_fm"])
            self.feedback_label.setText("Stopping radio")
            self.is_radio_running = False
            self.start_stop_button.setText("Start Radio")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stop radio: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    radio_app = RadioApp()
    radio_app.show()
    sys.exit(app.exec_())


