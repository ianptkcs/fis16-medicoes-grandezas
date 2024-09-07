# Experimental Data Analysis and LaTeX Report Generation

This project is designed to process experimental measurement data, perform statistical analysis, and generate LaTeX reports with tables of results.

```
.
├── classes/
│   └── files.py
├── data/
│   ├── medicoes.txt
│   └── massas.txt
├── tools/
│   └── tools.py
├── output/
│   ├── latex/
│   │   ├── medicoes/
│   │   ├── grandezas/
│   │   └── total.tex
│   ├── mock/ (temporary compilation files)
│   └── pdf/ (final PDF outputs)
├── main.py
└── compile_latex.py
```

## Dependencies

-   Python 3.x
-   NumPy
-   LaTeX distribution (e.g., TexLive)

## Setup

1. Ensure you have Python 3.x installed.
2. Install required Python packages:
    ```
    pip install numpy
    ```
3. Make sure you have a LaTeX distribution installed on your system.

## Usage

1. Place your measurement data in `data/medicoes.txt` and `data/massas.txt` following the template in classes/files.py:
   Medicoes:
    ```
    Object | Tool | Tool's Instrumental Error | Unit of Measure |  Measurements 1 -> 10
    ```
    Massas:
    ```
    Object | Tool's Instrumental Error | Measurements 1 -> 10
    ```
2. Run the main script to process data and generate LaTeX files:

    ```
    python main.py
    ```

3. Compile the generated LaTeX files to PDF:
    ```
    python compile_latex.py
    ```

## Main Components

### main.py

This is the primary script that:

-   Reads experimental data
-   Processes measurements and masses
-   Generates LaTeX tables for individual measurements and overall results

```python
import numpy as np
import csv
import os
import math
import tools.tools as t
from classes.files import DadosExperimento

alunos = ['Nelson', 'Patrick', 'Gabriel', 'Ian', 'Henrique']
arquivo_medicoes = csv.reader(open('data/medicoes.txt', 'r'), delimiter='\t')
arquivo_massas = csv.reader(open('data/massas.txt', 'r'), delimiter='\t')

dados_experimento = DadosExperimento()

t.extrair_dados_medicao(dados_experimento, arquivo_medicoes)
t.extrair_dados_massa(dados_experimento, arquivo_massas)
```

### classes/files.py

Defines data structures for storing experimental data:

-   `Medicao`: Represents a measurement
-   `Massa`: Represents a mass measurement
-   `DadosExperimento`: Holds all experimental data

### tools/tools.py

Contains utility functions for data processing and LaTeX generation:

-   Statistical calculations (mean, standard deviation, etc.)
-   LaTeX formatting and table creation

### compile_latex.py

Compiles the generated LaTeX files into PDF format:

-   Uses `pdflatex` to compile `.tex` files
-   Moves resulting PDFs to the output directory

## Output

The project generates:

1. LaTeX files in `output/latex/`
2. Temporary compilation files in `output/mock/`
3. Final PDF reports in `output/pdf/`

## Notes

-   The project is set up to handle measurements for various objects (Cubo, Barbante, Bola, Barrinha, Barra, Cilindro).
-   It calculates and reports measurements, masses, volumes, and densities where applicable.
-   The LaTeX output includes tables with measurements, uncertainties, and derived quantities.

## Future Improvements

-   Add error handling and input validation
-   Implement logging for better debugging
-   Create a configuration file for easy customization of objects and measurements
-   Add visualization capabilities for the processed data

## Authors & Contributors

-   Muxiba
-   Ian Patrick

## License

This project is licensed under the [MIT License](LICENSE).
