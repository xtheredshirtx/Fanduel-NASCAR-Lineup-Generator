import sys
import os
import random
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit

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

        self.label1 = QLabel('Select NASCAR Data Folder:')
        layout.addWidget(self.label1)
        self.button1 = QPushButton('Browse', self)
        self.button1.clicked.connect(self.openFolderDialog)
        layout.addWidget(self.button1)

        self.label2 = QLabel('Enter Number of Lineups:')
        layout.addWidget(self.label2)
        self.lineEdit1 = QLineEdit(self)
        layout.addWidget(self.lineEdit1)

        self.label3 = QLabel('Enter Number of Laps:')
        layout.addWidget(self.label3)
        self.lineEdit2 = QLineEdit(self)
        layout.addWidget(self.lineEdit2)

        self.button2 = QPushButton('Generate Lineup', self)
        self.button2.clicked.connect(self.generate_lineup)
        layout.addWidget(self.button2)

        self.setLayout(layout)

        self.folder_path = ""

    def openFolderDialog(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select NASCAR Data Folder", options=options)
        if folder_path:
            self.folder_path = folder_path
            self.label1.setText(f'Selected: {folder_path}')

    def generate_lineup(self):
        if not self.folder_path or not self.lineEdit1.text() or not self.lineEdit2.text():
            print("Please select all inputs.")
            return

        num_lineups = int(self.lineEdit1.text())
        laps = int(self.lineEdit2.text())

        output_dir = os.path.join(self.folder_path, 'Generated Lineups')
        os.makedirs(output_dir, exist_ok=True)

        try:
            nascar_data = load_nascar_data(self.folder_path)
            lineups = generate_lineups(nascar_data, laps, num_lineups)

            if not lineups:
                print("No valid lineups generated.")
            else:
                for i, lineup in enumerate(lineups, start=1):
                    total_projection = lineup['Projection'].sum()
                    print(f"Lineup {i} (Total Projection: {total_projection}):")
                    print(lineup[['Name', 'Position', 'Salary', 'Projection', 'FanDuel_Score']])
                    print("\n")

                save_lineups_to_excel(lineups, output_dir)
        except Exception as e:
            print(f"An error occurred: {e}")

def load_nascar_data(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    if not files:
        raise FileNotFoundError("No Excel files found in the specified folder.")
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    file_path = os.path.join(folder_path, latest_file)
    nascar_data = pd.read_excel(file_path)
    return nascar_data

def calculate_fanduel_score(row, laps):
    finishing_points = {
        1: 43, 2: 40, 3: 38, 4: 37, 5: 36, 6: 35, 7: 34, 8: 33, 9: 32, 10: 31,
        11: 30, 12: 29, 13: 28, 14: 27, 15: 26, 16: 25, 17: 24, 18: 23, 19: 22, 20: 21,
        21: 20, 22: 19, 23: 18, 24: 17, 25: 16, 26: 15, 27: 14, 28: 13, 29: 12, 30: 11,
        31: 10, 32: 9, 33: 8, 34: 7, 35: 6, 36: 5, 37: 4, 38: 3, 39: 2, 40: 1
    }
    position = row['Position']
    score = finishing_points.get(position, 0)
    score += row['Ceiling-Laps'] * 0.1
    score += row['Projection'] * 0.1
    position_differential = row['Position'] - row['Ceiling']
    score += position_differential * 0.5
    score += laps * 0.1
    score += row['Top5%'] * 10
    return score

def generate_lineups(nascar_data, laps, num_lineups=1):
    nascar_data['FanDuel_Score'] = nascar_data.apply(calculate_fanduel_score, axis=1, laps=laps)
    sorted_data = nascar_data.sort_values(by='FanDuel_Score', ascending=False)
    
    # Filter out drivers with Top 5% chance less than 10%
    filtered_data = sorted_data[sorted_data['Top5%'] >= 10]
    
    lineups = []
    all_drivers_indices = list(range(len(filtered_data)))
    min_salary = filtered_data['Salary'].min()
    
    while len(lineups) < num_lineups:
        lineup_indices = random.sample(all_drivers_indices, 5)
        lineup = filtered_data.iloc[lineup_indices]
        
        if len(lineup) == 5 and lineup['Salary'].sum() <= 50000:
            lineup_df = lineup.copy()
            lineup_df['Total_Projection'] = lineup_df['Projection'].sum()
            lineup_df['Lineup_Number'] = len(lineups) + 1
            lineups.append(lineup_df)
    
    return lineups

def save_lineups_to_excel(lineups, folder_path):
    output_data = []
    for lineup in lineups:
        lineup_number = lineup['Lineup_Number'].iloc[0]
        total_projection = lineup['Total_Projection'].iloc[0]
        header = pd.DataFrame([["Lineup", lineup_number, "", "", "", "", "", "", "", "", "", "", total_projection, ""]], columns=lineup.columns)
        output_data.append(header)
        output_data.append(lineup)
        output_data.append(pd.DataFrame([[""] * len(lineup.columns)], columns=lineup.columns))

    output_df = pd.concat(output_data, ignore_index=True)
    output_file = os.path.join(folder_path, 'generated_lineups.xlsx')
    with pd.ExcelWriter(output_file) as writer:
        output_df.to_excel(writer, sheet_name='Lineups', index=False)
    print(f"Lineups have been saved to {output_file}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
