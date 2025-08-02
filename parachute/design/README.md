
# Parachute Gore & 3D Model Generator

This tool helps generate printable gore patterns and a 3D mesh model for hemispherical parachutes, primarily for use in rocket recovery systems.

---

# Features

-Gore Generator: Creates scalable, printable gore patterns based on diameter and number of panels.
-3D Model Generator: Produces a 3D `.STL` mesh of the parachute for simulations, visual checks, or import into CAD.
-Seam Allowance: Option to include seam allowance in pattern generation.
-Spill Hole: Customizable central spill hole diameter.



# Project Structure

```

parachute/
├── gore\_generator.py           # Main script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── outputs/                    # Generated files (PDF + STL)


````



# Requirements

Install the required Python libraries:

```bash
pip install -r requirements.txt
````

If you want to install manually:

```
pip install numpy matplotlib trimesh
```



# How to Run

Run the script using:

```
python generate_gore.py
```

You will be prompted to input:

Diameter of parachute (in meters)
Number of gores (panels)
Seam allowance (in cm)
Spill hole diameter (in cm)

The script will generate:

 `gore_*.pdf` – Gore pattern for printing
 `parachute_*.stl` – 3D parachute mesh


# Output

All generated files are saved to the `outputs/` directory automatically.

You can import the `.stl` file into Fusion 360, SolidWorks, or other CAD software for visualization or validation.
The PDF gore can be printed and used for cutting fabric panels.



# Notes

This tool assumes a simple hemispherical parachute geometry.
STL mesh is inflated slightly to mimic deployed shape (non-rigid).
Seam allowance is visualized as dashed lines.
Gores are symmetric and printable on pages (depending on dimensions).


# Future Improvements
Config file input support (JSON)
CLI arguments support
Auto-scaling gore PDF to fit pages better
Optional mesh inflation preview toggle

