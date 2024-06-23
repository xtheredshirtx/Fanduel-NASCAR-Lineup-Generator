import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

# Normalize names by removing periods and extra spaces
def normalize_name(name):
    return name.replace('.', '').strip()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'FanDuel Lineup Creator'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout()

        self.label1 = QLabel('Select Generated Lineups File:')
        layout.addWidget(self.label1)
        self.button1 = QPushButton('Browse', self)
        self.button1.clicked.connect(self.openFileNameDialog1)
        layout.addWidget(self.button1)

        self.label2 = QLabel('Select Driver Data File:')
        layout.addWidget(self.label2)
        self.button2 = QPushButton('Browse', self)
        self.button2.clicked.connect(self.openFileNameDialog2)
        layout.addWidget(self.button2)

        self.label3 = QLabel('Select Output Directory:')
        layout.addWidget(self.label3)
        self.button3 = QPushButton('Browse', self)
        self.button3.clicked.connect(self.openDirectoryDialog)
        layout.addWidget(self.button3)

        self.button4 = QPushButton('Generate Lineup', self)
        self.button4.clicked.connect(self.generate_lineup)
        layout.addWidget(self.button4)

        self.setLayout(layout)

        self.generated_lineups_path = ""
        self.driver_data_path = ""
        self.output_dir = ""

    def openFileNameDialog1(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Generated Lineups File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            self.generated_lineups_path = fileName
            self.label1.setText(f'Selected: {fileName}')

    def openFileNameDialog2(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Driver Data File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            self.driver_data_path = fileName
            self.label2.setText(f'Selected: {fileName}')

    def openDirectoryDialog(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", options=options)
        if directory:
            self.output_dir = directory
            self.label3.setText(f'Selected: {directory}')

    def generate_lineup(self):
        if not self.generated_lineups_path or not self.driver_data_path or not self.output_dir:
            print("Please select all files and output directory.")
            return

        # Ensure the required folder exists
        os.makedirs(os.path.join(self.output_dir, 'Fanduel Lineup File'), exist_ok=True)

        output_csv_path = os.path.join(self.output_dir, 'Fanduel Lineup File', 'fanduel_lineup.csv')

        # Read the generated lineups
        lineups = pd.read_excel(self.generated_lineups_path)

        # Read the driver data
        driver_data = pd.read_excel(self.driver_data_path)

        # Create a full name column for matching and normalize it
        driver_data['Full Name'] = (driver_data['First Name'] + ' ' + driver_data['Last Name']).apply(normalize_name)

        # Create a dictionary for quick lookup of driver IDs
        driver_lookup = driver_data.set_index('Full Name')['Player ID + Player Name'].to_dict()

        # Prepare the output data
        output_data = []

        # Iterate over the lineups and extract the relevant driver IDs
        current_lineup = []
        for _, row in lineups.iterrows():
            name = row['Name']
            if name == 'Lineup':
                if current_lineup:
                    output_data.append(current_lineup)
                current_lineup = []
            elif pd.notna(name):
                normalized_name = normalize_name(name)
                driver_id = driver_lookup.get(normalized_name)
                if driver_id:
                    current_lineup.append(driver_id.split(':')[0])
                else:
                    print(f"Driver not found in lookup: {normalized_name}")

        # Add the last lineup if it exists
        if current_lineup:
            output_data.append(current_lineup)

        # Convert the list of lists to a dataframe and set the header as 'Driver' for all columns
        output_df = pd.DataFrame(output_data, columns=['Driver'] * 5)

        # Save the dataframe to a CSV file
        output_df.to_csv(output_csv_path, index=False)

        print(f'FanDuel lineup CSV file has been created: {output_csv_path}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
