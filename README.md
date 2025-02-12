# PressureCooker25
Pressure Cooker assignment - Group 25

# Pokemon Team Analyzer

A Python tool for analyzing Pokemon teams and providing suggestions for team improvement. This tool helps trainers build balanced teams by analyzing type coverage, stat distribution, and evolution potential.

## Features

- **Team Analysis**
  - Type coverage and weaknesses
  - Stat distribution
  - Duplicate Pokemon detection
  - Evolution stage information

- **Visualization**
  - Team type coverage radar charts
  - Type distribution analysis
  - Statistical summaries

- **Team Improvement Suggestions**
  - Replacement options for duplicate Pokemon
  - Counter suggestions for type weaknesses
  - Balanced stat recommendations
  - Evolution potential information

## Installation

1. Clone the repository:

bash

git clone https://github.com/yourusername/PressureCooker25.git

cd PressureCooker25

2. Install required packages:
bash

pip install pandas numpy matplotlib seaborn

## Usage

Run the main program:

bash

python src/main.py


### Menu Options

1. **Analyze specific Pokemon**: Get detailed information about a single Pokemon
2. **Show type distribution**: View and save type distribution visualization
3. **Compare multiple Pokemon**: Compare stats of multiple Pokemon
4. **Analyze team composition**: Get comprehensive team analysis and suggestions
5. **Exit**: Close the program

### Team Analysis Example

bash

Enter your team of 6 Pokemon (comma-separated):

charizard, blastoise, venusaur, pikachu, snorlax, gengar

📊 Team Analysis Report

🛡️ Defensive Coverage:

Weaknesses: rock, electric

Resistances: fighting, poison, bug, grass, fairy

⚔️ Offensive Coverage:

Types: fire, water, grass, electric, normal, ghost, poison

💡 Improvement Suggestions:

[Suggestions for team improvements will be displayed here]


## Data Sources

- Pokemon data from Generations 1-7
- Includes base stats, types, and evolution information
- Evolution chain data generated from name patterns and stat relationships

## Files

- `main.py`: Main program interface
- `team_analyzer.py`: Core team analysis functionality
- `pokemon.csv`: Pokemon database
- `evolution_chains.json`: Pokemon evolution data

## Notes

- Pokemon names are case-insensitive
- Enter Pokemon names exactly as they appear in the games
- Some Pokemon may have multiple evolution paths
- Base stat totals are used to suggest balanced replacements

## Ownership

This project is owned by Cédric Kruizinga and used for the "Pressure Cooker" assignment.
Cédric Kruizinga - 12/02/2025
