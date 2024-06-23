# FanDuel Lineup Creator Applications

## Introduction

This document provides step-by-step instructions for using two desktop applications designed to create FanDuel lineups based on NASCAR data. These applications utilize PyQt5 for the graphical user interface (GUI) and Pandas for data manipulation.

Note: Using these scripts does not guarantee success in FanDuel competitions. NASCAR results can be unpredictable and influenced by many factors.

## Requirements

- Python 3.x
- PyQt5 library
- Pandas library

You can install the required libraries using pip:

```bash
pip install PyQt5 pandas
```

## Folder Structure and Required Files

1. **Create a Main Folder**:
   - Create a folder on your desktop named `Fanduel Lineup Creator`.

2. **Download and Place Files**:
   - Place the provided Python scripts and batch files (`Lineup.py`, `Lineup.bat`, `Fanduel.py`, `Fanduel.bat`) into the `Fanduel Lineup Creator` folder.

3. **Create Subfolders**:
   - Inside the `Fanduel Lineup Creator` folder, create the following subfolders:
     - `Data`: This folder will contain the NASCAR data files.
     - `Generated Lineups`: This folder will be used to save the generated lineups from `Lineup.py`.
     - `Fanduel Lineup File`: This folder will be used to save the final FanDuel CSV file from `Fanduel.py`.

4. **Place Example Files**:
   - Place the example data files (`Nascar FD Top Stacks.xlsx` and `Driver.xlsx`) in the `Data` folder.

### Example Folder Structure

```
Fanduel Lineup Creator
│
├── Lineup.py
├── Lineup.bat
├── Fanduel.py
├── Fanduel.bat
│
├── Data
│   ├── Nascar FD Top Stacks.xlsx
│   └── Driver.xlsx
│
├── Generated Lineups
│
└── Fanduel Lineup File
```

## Running the Scripts

### Step 1: Generate Lineups

1. **Update NASCAR Data Folder**:
   - Ensure the latest FanDuel driver information is available by downloading the most recent data for the upcoming race and updating the file in the `Data` folder. Replace `Nascar FD Top Stacks.xlsx` with the latest data. The latest `Nascar FD Top Stacks.xlsx` file can also be located in the Discord channel under `fanduel-nascar-files`.

2. **Open the Main Folder**:
   - Navigate to the `Fanduel Lineup Creator` folder you created on your desktop.

3. **Run `Lineup.py`**:
   - Double-click on `Lineup.bat` to execute the `Lineup.py` script.

4. **Provide Inputs**:
   - A GUI will appear prompting you to select the NASCAR data folder and enter the number of lineups and laps.
   - **NASCAR Data Folder**: Select the `Data` folder within the `Fanduel Lineup Creator` folder.
   - **Number of Lineups**: Enter the number of lineups you wish to generate.
   - **Number of Laps**: Enter the number of laps in the race.

5. **Generate Lineups**:
   - Click the "Generate Lineup" button. The generated lineups will be saved as an Excel file in the `Generated Lineups` folder.

### Step 2: Create FanDuel CSV File

1. **Update Driver Data File**:
   - Ensure the latest driver information is available by downloading the most recent data from FanDuel for the upcoming race and updating the file in the `Data` folder. Replace `Driver.xlsx` with the latest data.

2. **Ensure Lineups are Generated**:
   - Make sure that `generated_lineups.xlsx` exists in the `Generated Lineups` folder from the previous step.

3. **Run `Fanduel.py`**:
   - Double-click on `Fanduel.bat` to execute the `Fanduel.py` script.

4. **Provide Inputs**:
   - A GUI will appear prompting you to select the generated lineups file, driver data file, and output directory.
   - **Generated Lineups File**: Select the `generated_lineups.xlsx` file from the `Generated Lineups` folder.
   - **Driver Data File**: Select the `Driver.xlsx` file from the `Data` folder.
   - **Output Directory**: Select the `Fanduel Lineup File` folder within the `Fanduel Lineup Creator` folder.

5. **Generate CSV**:
   - Click the "Generate Lineup" button. The FanDuel CSV file will be saved in the `Fanduel Lineup File` folder.

## Contact for Support

If you have any questions or need further assistance, please reach out on Discord: [xTheRedShirtx](https://discord.gg/aGrKzeW).

## Disclaimer

Please note that using these scripts does not guarantee success in FanDuel competitions. NASCAR results can be highly unpredictable and influenced by many factors. Use these scripts as a tool to assist in creating your lineups, but remember that the final outcomes are subject to variability and chance.

---

By following these instructions, you will be able to set up and use the FanDuel Lineup Creator applications to generate and manage your FanDuel lineups. Ensure to update the necessary data files before each race to maintain accuracy in your projections and lineups.
