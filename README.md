# PressureCooker25
Pressure Cooker assignment - Group 25

# Pokemon Evolution Advisor

A Python program that helps trainers make informed decisions about evolving their Pokemon by analyzing stats, types, and providing strategic recommendations.

## Features

- Detailed stat analysis of Pokemon evolution chains
- Visual representation of stats across evolution stages
- Strategic recommendations based on stat changes
- Support for branching evolutions (like Eevee)
- Type change analysis
- Complete evolution chain visualization

## Files Structure

### `src/main.py`
The main program file that:
- Handles user input
- Processes Pokemon data
- Generates stat analysis
- Creates visualizations
- Provides evolution recommendations

### `src/evolution_chains.py`
Contains the evolution chain data and utility functions:
- Defines Pokemon evolution relationships
- Handles special cases (branching evolutions)
- Provides evolution chain lookup functions

### `src/pokemon.csv`
The Pokemon database containing:
- Base stats (HP, Attack, Defense, etc.)
- Type information
- Generation data
- Pokedex numbers

### `src/evolution_stats.png`
Generated visualization showing:
- Base stats for each evolution stage
- Stat changes between forms
- Type information
- Complete evolution chain

## Requirements

python
pandas
matplotlib

## python src/main.py

1. Enter a Pokemon name when prompted

2. The program will:
   - Display a stat analysis
   - Generate a visualization (`evolution_stats.png`)
   - Provide strategic recommendations

3. Type 'quit' to exit the program

## Visualization Guide

The generated graph shows:
- Base stats as the bottom bar segment
- Evolution stat increases as stacked segments
- Numerical values for each stat
- Type information for each form
- Complete evolution chain in the title