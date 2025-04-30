# Conditon Realtions

Predicts relationships between medical conditons based on shared symptoms and the severity of the symptom. It uses BFS to sort the shorted path of relation and weights to explore symptom-based associations.

## Overview

The `ConditionPredictor` class builds a condition graph from two CSV files:
1. Data on conditons and corresponding symptoms
2. Data on weights associated with the symptoms

## How It Works
1. Each condition is a node
2. Connections formed if there is a shared symptom
3. Users input two conditions from a provided list
4. Shortest path of realtion is returned along with a break down of each step within the path

## License
This is not for resue or distribution.
