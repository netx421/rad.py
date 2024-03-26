#netx421@proton.me
#thanks for using x421 for your sdr needs!
#please share and use the code for your own needs
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QHBoxLayout

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

        # Start/Stop button
        self.start_stop_button = QPushButton("Start Radio")

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

        # Determine selected modulation type
        modulation_type = "AM" if self.am_radio.isChecked() else "FM" if self.fm_radio.isChecked() else "NFM"

        # Build radio command
        if modulation_type == "AM":
            radio_command = f"rtl_fm -M am -f {frequency_entry_value}e6 -s 60k - | sox -t raw -r 60000 -b 16 -e signed-integer -c 1 - -t raw - lowpass 1k | play -q -r 60000 -t raw -e signed-integer -b 16 -c 1 -V1 -"
        else:
            radio_command = f"rtl_fm -f {frequency_entry_value}e6 -M {modulation_type} -s 200000 -r 32000 - | sox -t raw -r 44100 -b 16 -e signed-integer -c 1 - -t raw - lowpass 3k | play -q -r 32000 -t raw -e signed-integer -b 16 -c 1 -V1 -"

        try:
            # Run radio command
            self.radio_process = subprocess.Popen(radio_command, shell=True)
        except PermissionError:
            # Use sudo if permission error occurs
            radio_command = f"sudo {radio_command}"
            self.radio_process = subprocess.Popen(radio_command, shell=True)

        # Display feedback about the radio operations
        print("Starting radio with frequency:", frequency_entry_value, "Modulation type:", modulation_type)

        # Update radio state
        self.is_radio_running = True
        self.start_stop_button.setText("Stop Radio")

    def stop_radio(self):
        # Use pkill to stop the radio process
        subprocess.run(["pkill", "-f", "rtl_fm"])

        # Display feedback about stopping the radio
        print("Stopping radio")

        # Update radio state
        self.is_radio_running = False
        self.start_stop_button.setText("Start Radio")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    radio_app = RadioApp()
    radio_app.show()
    sys.exit(app.exec_())

