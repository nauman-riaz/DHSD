# Contributing to DHSD

Thank you for your interest in contributing to the German Handwriting Street-name Dataset (DHSD)!

## How to Contribute

### Reporting Issues

If you find errors in annotations, corrupted images, or other data quality issues, please open an issue on the repository with:

- A description of the problem
- The affected file(s) (e.g., `german_hw_data/writer5/5_42.png`)
- Expected vs. actual annotation (if applicable)

### Adding New Handwriting Samples

If you would like to contribute additional handwriting samples:

1. **Contact the maintainer** first to discuss the contribution.
2. Write the provided word list by hand on the supplied template.
3. Ensure your handwriting is legible and follows the provided guidelines.
4. Submit scanned/photographed images in PNG format.

### Requirements for New Contributions

- Images must be **256 × 64 pixels**, **PNG format**, **RGBA** colour mode.
- Each image must contain exactly **one word**.
- Corresponding annotations must be provided in CSV format (`file_name,text,writer_id`).
- Contributors must provide **informed consent** for their handwriting to be publicly released under the **CC BY 4.0** license.

### Code Contributions

If you would like to contribute code (e.g., improvements to `dataset_statistics.py` or new analysis scripts):

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-improvement`).
3. Commit your changes with clear messages.
4. Submit a pull request.

## Code of Conduct

Please be respectful and constructive in all interactions. We are committed to providing a welcoming and inclusive environment for everyone.

## License

By contributing to this dataset, you agree that your contributions will be licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.
