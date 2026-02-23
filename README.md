# Deutscher Handschriften-Datensatz (DHSD) — German Handwriting Street-name Dataset

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

The **Deutscher Handschriften-Datensatz (DHSD) — German Handwriting Street-name Dataset** is a novel handwritten text recognition (HTR) dataset for the German language. It contains **5,939 handwritten word images** contributed by **37 writers**, each providing an average of **~160 words**. All words are names of cities and streets in Germany, extracted from the [OpenStreetMap (OSM)](https://www.openstreetmap.org/) database. The words were carefully selected to ensure that **every letter of the German alphabet** — including umlauts (ä, ö, ü) and the Eszett (ß) — is represented.

## Dataset Statistics

| Property | Value |
|---|---|
| Total images | 5,939 |
| Total writers | 37 |
| Unique words | 5,085 |
| Image format | PNG (RGBA) |
| Image resolution | 256 × 64 pixels |
| Avg. words per writer | 160.5 |
| Min words per writer | 123 |
| Max words per writer | 165 |
| Avg. word length (chars) | 15.3 |
| Total size (uncompressed) | ~79 MB |
| Annotation format | CSV |

## Motivation

Handwritten text recognition for German is under-served compared to English. Existing datasets lack sufficient coverage of the full German alphabet, especially special characters such as ä, ö, ü, and ß. DHSD was created to fill this gap by providing a curated, writer-diverse dataset with guaranteed full-alphabet coverage, making it suitable for training and benchmarking HTR systems for the German language.

## Directory Structure

```
DHSD/
├── README.md                  # This file
├── LICENSE                    # CC BY 4.0 license
├── CITATION.cff               # Machine-readable citation metadata
├── .zenodo.json               # Zenodo upload metadata
├── DATASHEET.md               # Datasheet for the dataset (Gebru et al.)
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── checksums.sha256           # SHA-256 checksums for data integrity
├── data.csv                   # Annotations (file_name, text, writer_id)
├── train.csv                  # Training split (80%, stratified by writer)
├── test.csv                   # Testing split (20%, stratified by writer)
├── dataset_statistics.py      # Script to generate dataset statistics
└── german_hw_data/            # Handwritten word images
    ├── writer1/
    │   ├── 1_0.png
    │   ├── 1_1.png
    │   └── ...
    ├── writer2/
    │   └── ...
    └── writer37/
        └── ...
```

## Annotations

All annotations are stored in `data.csv` with the following columns:

| Column | Type | Description |
|---|---|---|
| `file_name` | string | Relative path to the image file (e.g., `german_hw_data/writer1/1_0.png`) |
| `text` | string | The ground-truth transcription of the handwritten word |
| `writer_id` | integer | Unique identifier for the writer (1–37) |

### Example rows

```csv
file_name,text,writer_id
german_hw_data/writer1/1_0.png,Königshain-Wiederau,1
german_hw_data/writer1/1_1.png,Söllingen,1
german_hw_data/writer1/1_2.png,Gülitz-Reetz,1
```

## Train / Test Split

The dataset is split into **training (80%)** and **testing (20%)** subsets. A reproducible splitting script is provided in `dataset_statistics.py`, which uses stratified splitting by writer ID.

| Split | Samples | Percentage |
|---|---|---|
| Training | 4,745 | 79.9% |
| Testing | 1,194 | 20.1% |

## Getting Started

### Download

Download the dataset from Zenodo:

```bash
# Replace XXXXXXX with the actual Zenodo DOI
wget https://zenodo.org/record/XXXXXXX/files/DHSD.zip
unzip DHSD.zip
```

### Quick Usage (Python)

```python
import pandas as pd
from PIL import Image

# Load annotations
df = pd.read_csv("data.csv")
print(f"Total samples: {len(df)}")
print(f"Total writers: {df['writer_id'].nunique()}")

# Display a sample
sample = df.iloc[0]
img = Image.open(sample["file_name"])
print(f"Text: {sample['text']}, Writer: {sample['writer_id']}")
img.show()
```

### Generate Statistics

```bash
python dataset_statistics.py
```

## Data Collection Process

1. **Word Selection**: City and street names were extracted from the OpenStreetMap (OSM) database. Words were curated to ensure every letter of the German alphabet (including ä, ö, ü, ß) is represented.
2. **Handwriting Collection**: 37 individuals wrote the selected words by hand.
3. **Digitisation**: Handwritten samples were scanned/photographed and cropped to 256×64 pixel PNG images.
4. **Annotation**: Each image was annotated with its ground-truth text and writer ID, stored in `data.csv`.

## Ethical Considerations

- All writers provided informed consent for their handwriting to be included in this publicly available dataset.
- No personally identifiable information (PII) is included beyond anonymised writer IDs.
- The dataset contains only geographic names (cities, streets) and does not include sensitive or offensive content.

## Citation

If you use this dataset in your research, please cite it as:

```bibtex
@dataset{dhsd2026,
  title        = {{DHSD} -- {German} Handwriting Street-name Dataset},
  author       = {Riaz, Nauman and Saifullah, Saifullah and Agne, Stefan and Dengel, Andreas and Ahmed, Sheraz},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX},
  note         = {Version 1.0.0}
}
```

See also [CITATION.cff](CITATION.cff) for a machine-readable citation file.

## License

This dataset is released under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license. You are free to share and adapt the material for any purpose, provided you give appropriate credit.

## Associated Paper

This dataset was introduced in the following paper:

> Nauman Riaz, Saifullah Saifullah, Stefan Agne, Andreas Dengel, and Sheraz Ahmed.  
> **StylusAI: Stylistic Adaptation for Robust German Handwritten Text Generation.**  
> In: *Document Analysis and Recognition – ICDAR 2024*. Springer Nature Switzerland, 2024, pp. 429–444.  
> DOI: [10.1007/978-3-031-70536-6_26](https://doi.org/10.1007/978-3-031-70536-6_26)

## Acknowledgements

- Geographic names sourced from [OpenStreetMap](https://www.openstreetmap.org/) © OpenStreetMap contributors, licensed under [ODbL](https://opendatacommons.org/licenses/odbl/).
- We thank all 37 writers who contributed their handwriting samples.
- This work was conducted at the German Research Center for Artificial Intelligence (DFKI), Kaiserslautern.

## Contact

For questions, issues, or feedback, please open an issue on the repository or contact the dataset maintainer.

## Version History

See [CHANGELOG.md](CHANGELOG.md) for a complete version history.
