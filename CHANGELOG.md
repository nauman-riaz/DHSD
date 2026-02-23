# Changelog

All notable changes to the DHSD dataset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-02-23

### Added

- Initial public release of the DHSD dataset.
- 5,939 handwritten word images from 37 writers.
- CSV annotation file (`data.csv`) with columns: `file_name`, `text`, `writer_id`.
- Full German alphabet coverage including umlauts (ä, ö, ü) and Eszett (ß).
- 80/20 train/test split (stratified by writer).
- Dataset statistics script (`dataset_statistics.py`).
- Documentation: README, LICENSE (CC BY 4.0), CITATION.cff, .zenodo.json, DATASHEET.md.
- SHA-256 checksums for data integrity verification.
