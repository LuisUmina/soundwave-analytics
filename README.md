# 🎧 SoundWave Analytics

This project simulates a real-world Data Engineering pipeline for a music streaming platform.

It is built to simulate the kind of data infrastructure used by companies like Spotify or Netflix, covering everything from data ingestion and transformation to real-time streaming and visualization — using cloud and modern data engineering tools.

---

## 🎯 Main Goals

- Ingest raw music streaming data into a **Data Lake**
- Build a structured **Data Warehouse** using a star schema
- Orchestrate recurring workflows with **Apache Airflow**
- Stream real-time events with **Kafka**
- Deploy the solution to the **Cloud** (AWS or Azure)
- Create dashboards with **Power BI** or **Tableau**

---

## 🧰 Tech Stack

- **Language:** Python 3.8+
- **Data Lake:** Local / S3 / Azure Blob
- **Data Warehouse:** PostgreSQL / Redshift / Azure Synapse
- **Orchestration:** Apache Airflow
- **Streaming:** Kafka / AWS Kinesis
- **Infrastructure:** Docker, Terraform
- **Visualization:** Power BI / Tableau / Metabase

---

## 📡 Data Sources

This project ingests and processes data from:

- **CSV files**: Users, songs, and play logs (simulating internal logs)
- **Spotify API**: Real-world data from artists and albums

All sources are processed into Parquet format and stored in a structured Data Lake.

---

## 📁 Project Structure

```bash
soundwave-analytics/
├── dags/                      
├── data_lake/                 
│   └── raw/
├── docs/
│   └── architecture.md
├── infra/ 
├── notebooks/
├── scripts/ 
│   └── ingestion/
├── .flake8 
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── venv/             
```

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/LuisUmina/soundwave-analytics.git
cd soundwave-analytics

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run data ingestion scripts
python scripts/ingestion/extract_users.py
python scripts/ingestion/extract_songs.py
python scripts/ingestion/extract_play_logs.py
python scripts/ingestion/extract_spotify.py
```

---

## 💡 Code Quality

### Format code
```bash black scripts/```

### Lint code
```bash flake8 scripts/```

---

---

## 🧩 Data Warehouse Schema

The data warehouse follows a dimensional **Star Schema**, designed for performance and clarity in analytical queries.

- Central fact table: `fact_plays`
- Connected dimensions: users, songs, artists, albums, devices, and dates

📎 [View Star Schema Diagram and Documentation](docs/modeling/DWH_star_schema_v1.md)


---

## 👨‍💻 Author
Made with 💙 by [@LuisUmina](https://github.com/LuisUmina)

## 📬 Contact
- Connect with me on LinkedIn: [Luis Umina](www.linkedin.com/in/luis-umina-navia)
- More projects at [@LuisUmina](https://github.com/LuisUmina)
