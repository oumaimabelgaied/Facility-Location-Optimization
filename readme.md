# Facility Location Optimization

An Operations Research project implementing mathematical optimization models for the Facility Location Problem (FLP) using Python and Gurobi.

## Problem Formulations

- **Capacitated Facility Location (CFL):** Determines which facilities to open and how to assign customers while respecting facility capacity constraints.
- **Uncapacitated Facility Location (UFL):** Determines the optimal facility locations and customer assignments without capacity restrictions.

## Features

- Interactive input of facility and customer data
- Facility opening and transportation cost optimization
- Mathematical modeling with Gurobi
- Visualization using Matplotlib and NetworkX
- LP and MPS model export

## Technologies

- Python
- Gurobi Optimizer (`gurobipy`)
- NetworkX
- Matplotlib

## Project Structure

```text
Facility-Location-Optimization/
├── projet/
│   ├── CFL.py
│   ├── UFL.py
│   ├── max.py
│   └── set.py
├── test/
│   ├── trial.py
│   ├── emptymodel.lp
│   └── emptymodel.mps
├── R.O_ Facility location.docx
├── .gitignore
└── README.md
```

## Requirements

- Python 3
- Gurobi Optimizer with a valid license
- gurobipy
- matplotlib
- networkx

Install Python dependencies:

```bash
pip install gurobipy matplotlib networkx
```

## Usage

Run either optimization model:

```bash
python projet/CFL.py
```

```bash
python projet/UFL.py
```

Follow the interactive prompts to enter facility and customer data.

## Academic Context

Developed as part of an Operations Research project at INSAT (Institut National des Sciences Appliquées et de Technologie).