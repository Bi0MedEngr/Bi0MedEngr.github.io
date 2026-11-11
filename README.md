# Bench Tools

The launcher page for the bench tools: **https://bi0medengr.github.io/**

Every tool is one self-contained HTML page: no account, no install, nothing sent anywhere, and it works offline once opened. Most have a **Show the math** view with the equations and your numbers, and every model is tested against independent textbook or closed-form answers before release. On an iPad or phone: open a tool, then Share → Add to Home Screen.

### Motion and mechanisms

| | Tool | What it does |
|---|---|---|
| <img src="docs/icons/motion-bench.svg" width="40" alt=""> | **[Motion Bench](https://bi0medengr.github.io/motion-bench/)**<br>[source](https://github.com/Bi0MedEngr/motion-bench) | Planar linkage and mechanism simulator. Draw links, pins, sliders, springs, dampers and cams, drive them, and get motion, joint forces, motor torque, bar diagrams and frequency response. |
| <img src="docs/icons/kinematics-bench.svg" width="40" alt=""> | **[Kinematics Bench](https://bi0medengr.github.io/kinematics-bench/)**<br>[source](https://github.com/Bi0MedEngr/kinematics-bench) | Projectiles with air drag, ramps with friction, roller-coaster tracks you shape by hand, large-swing pendulums and collisions, with energy bookkeeping. |

### Structures and machine design

| | Tool | What it does |
|---|---|---|
| <img src="docs/icons/beam-bench.svg" width="40" alt=""> | **[Beam Bench](https://bi0medengr.github.io/beam-bench/)**<br>[source](https://github.com/Bi0MedEngr/beam-bench) | Shear, moment, axial force and deflection diagrams for beams and 2D frames, determinate or indeterminate, with the hand calculation written out. |
| <img src="docs/icons/spring-bench.svg" width="40" alt=""> | **[Spring Bench](https://bi0medengr.github.io/spring-bench/)**<br>[source](https://github.com/Bi0MedEngr/spring-bench) | Compression, extension and torsion spring design: rate, corrected stresses, solid height, buckling, surge and fatigue, with a pass/fail checklist and McMaster-Carr import. |
| <img src="docs/icons/solid-bench.svg" width="40" alt=""> | **[Solid Bench](https://bi0medengr.github.io/solid-bench/)**<br>[source](https://github.com/Bi0MedEngr/solid-bench) | A basic 3D modeler: sketch, extrude, revolve, join and cut, with exact mass properties. Imports STL, 3MF and OBJ; exports STL. |

### Heat, magnetism and electronics

| | Tool | What it does |
|---|---|---|
| <img src="docs/icons/thermo-bench.svg" width="40" alt=""> | **[Thermo Bench](https://bi0medengr.github.io/thermo-bench/)**<br>[source](https://github.com/Bi0MedEngr/thermo-bench) | Gas power cycles on P-v and T-s diagrams, a psychrometric chart, heat exchanger rating and sizing, and heater warm-up under thermostat or PI control. |
| <img src="docs/icons/magnet-bench.svg" width="40" alt=""> | **[Magnet Bench](https://bi0medengr.github.io/magnet-bench/)**<br>[source](https://github.com/Bi0MedEngr/magnet-bench) | Exact fields and flux lines of coils and magnets, the forces between them, electromagnets with saturation, eddy-current braking and skin depth. |
| <img src="docs/icons/amp-bench.svg" width="40" alt=""> | **[Amp Bench](https://bi0medengr.github.io/amp-bench/)**<br>[source](https://github.com/Bi0MedEngr/amp-bench) | Plan an audio amplifier before buying parts: power and SPL, tube load lines, class AB and class D output stages, power supplies and output transformers. |

## How this site is built

- `tools.json` is the list: name, group, accent colors, blurb and labs for each tool. Add a tool there.
- `refresh.py` copies each tool's icon and takes light and dark preview shots from the sibling tool folders (needs Playwright).
- `build.py` writes the site to `docs/` (GitHub Pages serves that folder), this README and the profile README.
- `tests/browser_test.py` checks the page in light, dark, iPad and phone widths.
- The site's offline service worker answers only for the launcher's own files, so it never gets in the way of the tools under `/<tool>/`.
- Fonts: IBM Plex, SIL Open Font License (`fonts/OFL.txt`).
