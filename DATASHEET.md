# Datasheet for DHSD — German Handwriting Street-name Dataset

_Following the framework proposed by [Gebru et al. (2021)](https://arxiv.org/abs/1803.09010)._

---

## Motivation

### For what purpose was the dataset created?

The dataset was created to support research in **Handwritten Text Recognition (HTR)** for the **German language**. Existing HTR datasets lack sufficient coverage of the full German alphabet, especially special characters such as ä, ö, ü, and ß. DHSD was designed to fill this gap.

### Who created the dataset and on behalf of which entity?

The dataset was created by **Nauman Riaz, Saifullah Saifullah, Stefan Agne, Andreas Dengel, and Sheraz Ahmed** at the **German Research Center for Artificial Intelligence (DFKI)** and **RPTU Kaiserslautern-Landau** as part of the StylusAI research project.

### Who funded the creation of the dataset?

<!-- TODO: Add funding information if applicable -->
Not applicable / self-funded.

---

## Composition

### What do the instances that comprise the dataset represent?

Each instance is a **handwritten word image** (PNG, 256×64 pixels, RGBA) paired with its ground-truth text transcription and writer ID.

### How many instances are there in total?

**5,939** handwritten word images.

### Does the dataset contain all possible instances or is it a sample?

It is a **curated sample**. Words were selected from the OpenStreetMap database to ensure every letter of the German alphabet is represented at least once.

### What data does each instance consist of?

- A **PNG image** (256×64 pixels, RGBA) of a single handwritten word.
- A **text label** (the ground-truth transcription).
- A **writer ID** (integer, anonymised).

### Is there a label or target associated with each instance?

Yes. Each image is annotated with its ground-truth transcription (the text of the word) in `data.csv`.

### Is any information missing from individual instances?

No. All instances have an image, text label, and writer ID.

### Are relationships between individual instances made explicit?

Yes. Instances are grouped by writer via the `writer_id` column and the directory structure (`german_hw_data/writerN/`).

### Are there recommended data splits?

Yes. The dataset is split **80% training / 20% testing**, stratified by writer ID. The split logic is provided in `dataset_statistics.py`.

### Are there any errors, sources of noise, or redundancies in the dataset?

Some images may exhibit natural variations in writing quality (e.g., ink thickness, alignment). These are inherent to handwriting datasets and are not considered errors.

### Is the dataset self-contained, or does it link to or otherwise rely on external resources?

The dataset is **self-contained**. The geographic names are sourced from OpenStreetMap but the image data and annotations require no external dependencies.

### Does the dataset contain data that might be considered confidential?

No. The dataset contains only images of handwritten geographic names and anonymised writer IDs.

### Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?

No. All content consists of geographic place names (cities and streets in Germany).

---

## Collection Process

### How was the data associated with each instance acquired?

- **Word selection**: City and street names were extracted from the OpenStreetMap (OSM) database. Words were curated to ensure full German alphabet coverage.
- **Handwriting collection**: 37 individuals wrote the selected words by hand on paper/forms.
- **Digitisation**: Handwritten samples were scanned or photographed and cropped to 256×64 pixel PNG images.

### What mechanisms or procedures were used to collect the data?

Writers were given printed word lists and asked to write each word by hand. The resulting handwritten pages were digitised and segmented into individual word images.

### If the dataset is a sample from a larger set, what was the sampling strategy?

Words were selected from OpenStreetMap to maximise alphabet coverage. Not all OSM entries were used — only those that contributed to full German alphabet representation.

### Who was involved in the data collection process and how were they compensated?

37 individuals contributed handwriting samples. <!-- TODO: Add compensation details if applicable -->

### Over what timeframe was the data collected?

<!-- TODO: Add the data collection timeframe -->

### Were any ethical review processes conducted?

All writers provided **informed consent** for their handwriting to be included in a publicly available dataset.

---

## Preprocessing / Cleaning / Labelling

### Was any preprocessing/cleaning/labelling of the data done?

- Images were cropped and resized to a uniform **256×64 pixel** resolution.
- Each image was manually annotated with the corresponding ground-truth text.
- Writer IDs were assigned to group images by contributor.

### Was the "raw" data saved in addition to the preprocessed/cleaned/labelled data?

<!-- TODO: Specify if raw scans are preserved -->

### Is the software that was used to preprocess/clean/label the data available?

<!-- TODO: Link to any preprocessing scripts if applicable -->

---

## Uses

### Has the dataset been used for any tasks already?

Yes. The dataset was used for training and evaluating Handwritten Text Recognition (HTR) models as described in the accompanying publication.

### Is there a repository that links to any or all papers or systems that use this dataset?

<!-- TODO: Add link to paper/repository after publication -->

### What (other) tasks could the dataset be used for?

- Writer identification / verification
- Handwriting style analysis
- Data augmentation research for HTR
- German character segmentation research
- Transfer learning for low-resource HTR languages

### Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labelled that might impact future uses?

The words are exclusively geographic names (cities, streets). Models trained solely on this dataset may not generalise well to other text domains (e.g., free-form sentences, numbers).

### Are there tasks for which the dataset should not be used?

The dataset should not be used for re-identifying writers or for any purpose that violates the privacy of contributors.

---

## Distribution

### Will the dataset be distributed to third parties outside of the entity on behalf of which the dataset was created?

Yes. The dataset is publicly available on Zenodo under the **CC BY 4.0** license.

### How will the dataset be distributed?

As a ZIP archive on [Zenodo](https://zenodo.org/).

### When will the dataset be distributed?

February 2026 (version 1.0.0).

### Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)?

Yes. The dataset is distributed under the **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)** license.

### Have any third parties imposed IP-based or other restrictions on the data associated with the instances?

Geographic names are sourced from OpenStreetMap, which is licensed under the [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/). Attribution to OpenStreetMap contributors is required.

---

## Maintenance

### Who will be supporting/hosting/maintaining the dataset?

**Nauman Riaz** and collaborators at DFKI will maintain the dataset. It will be archived on Zenodo for long-term preservation.

### How can the owner/curator/manager of the dataset be contacted?

Via the Zenodo record page or by opening an issue on the associated code repository.

### Will the dataset be updated?

Future versions may include additional writers or word categories. Updates will be versioned and documented in `CHANGELOG.md`.

### If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances?

Writers may request removal of their contributions. In such cases, a new version will be released with the affected data removed.

### Will older versions of the dataset continue to be supported/hosted/maintained?

Yes. All versions will remain available on Zenodo with distinct DOIs.

### If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?

Yes. See `CONTRIBUTING.md` for contribution guidelines.
