# Rumor Spread Simulation (Monte Carlo)

## Overview
This project simulates the spread of a rumor among participants using a Monte Carlo approach. The simulation models how information propagates over time through random pairwise interactions.

## Features
- Simulates rumor spread across 4 rooms
- Uses probabilistic transmission (50% chance)
- Stops spreading after 2 exposures
- Runs multiple simulations to compute averages
- Tracks:
  - % heard at 10, 30, 60 minutes
  - Time to reach 10% and 50%
- Generates graphs and tables

## Technologies
- Python
- pandas
- matplotlib

## How to Run
```bash
pip install -r requirements.txt
python src/simulation.py
