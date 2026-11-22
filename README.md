<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:0d9488&height=180&section=header&text=CSV+SQLite+Loader&fontSize=42&fontColor=ffffff&animation=fadeIn)
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=21&pause=1000&color=14B8A6&center=true&vCenter=true&width=650&lines=Load+CSV+data+into+SQLite+with+type+inference" alt="Project title"/>
[![License](https://img.shields.io/github/license/CyberLoop-dev/csv-sqlite-loader?style=for-the-badge)](LICENSE)
[![Language](https://img.shields.io/github/languages/top/CyberLoop-dev/csv-sqlite-loader?style=for-the-badge)](https://github.com/CyberLoop-dev/csv-sqlite-loader)
[![Stars](https://img.shields.io/github/stars/CyberLoop-dev/csv-sqlite-loader?style=for-the-badge)](https://github.com/CyberLoop-dev/csv-sqlite-loader/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/CyberLoop-dev/csv-sqlite-loader?style=for-the-badge)](https://github.com/CyberLoop-dev/csv-sqlite-loader/commits/main)
<img src="assets/mark.svg" width="112" alt="CSV SQLite Loader mark"/>
</div>

## 🧭 Overview
A dependency-free Python CLI that imports a CSV file into a local SQLite database. It infers INTEGER, REAL, or TEXT column types, converts empty cells to NULL, and quotes identifiers safely.

## ✨ Features
- 📥 Loads CSV headers and rows into a SQLite table.
- 🧮 Infers a practical SQLite affinity for each column.
- 🔒 Uses parameterized inserts and quoted identifiers.
- 🧪 Supports safe table replacement with an explicit flag and includes tests.

## 🖥️ Demo
No hosted demo is published. Import a local CSV using the command below.

## 🚀 Quick Start
```bash
python main.py sample.csv data.db --table records
```
Use `--replace` to replace an existing table. Run tests with `python -m unittest discover -s tests -v`.

## 🧰 Tech Stack
Python 3.10+ standard library: csv, sqlite3, argparse, and unittest. No third-party dependencies.

## 🗂️ Folder Structure
```text
csv-sqlite-loader/
├── main.py
├── tests/
├── assets/
├── .github/workflows/
└── pyproject.toml
```

## 🛣️ Roadmap
- [x] CSV import with type inference.
- [x] Empty-cell NULL conversion and safe identifiers.
- [ ] Add configurable type overrides and batch-size controls.

## 🤝 Contributing
Contributions are welcome. Preserve safe SQL handling and add fixtures for new CSV edge cases.

## 📄 License
MIT — see [LICENSE](LICENSE).

<div align="center">
![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:0d9488,100:0f172a&height=110&section=footer)
</div>
