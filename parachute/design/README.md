# Parachute Gore & 3D Model Generator

This tool generates printable gore patterns and a 3D mesh model for hemispherical parachutes, primarily intended for rocket recovery systems.

## Features

- Gore pattern generator with customizable diameter and panel count  
- 3D STL mesh output for simulation or CAD  
- Seam allowance and spill hole customization  

## Project Structure

parachute/
├── design/
│ ├── generate_gore.py
│ ├── requirements.txt
│ ├── README.md
│ └── outputs/



## Requirements

```
pip install -r requirements.txt

```
Or install dependencies manually:

```
pip install numpy matplotlib trimesh

```

Usage

Run the generator:

```
python generate_gore.py

```
You will be prompted for parachute diameter, number of gores, seam allowance, and spill hole size.

Output
Printable gore pattern PDFs (gore_*.pdf)

3D mesh STL files (parachute_*.stl)
Saved in outputs/.

Notes
Assumes hemispherical parachute geometry

STL mesh inflated to mimic deployed shape

Seam allowances shown as dashed lines

Future Improvements
JSON config support

CLI argument parsing

Auto-scale PDFs for better printing

Mesh inflation preview toggle