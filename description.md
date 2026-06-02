# Project Documentation: Advertising Data Warehouse

## 1. Description of the Domain and Process

### Domain: Digital Advertising Performance

The domain of this project is **Digital Marketing Analytics**. In the current digital economy, companies deploy advertising content across multiple platforms (such as Facebook and Instagram) to reach specific demographics. Managing these campaigns generates vast amounts of fragmented data that must be synthesized to understand marketing efficiency.

### Process Covered

The Data Warehouse covers the end-to-end lifecycle of digital advertisements:

1. **Campaign Planning**: Defining budgets, durations, and seasonal themes (e.g., "Summer Launch" vs. "Winter Promo").
2. **Ad Placement**: Distributing specific creative assets (Videos, Stories, Carousels) targeted at specific audience segments (by age, gender, and interests).
3. **User Engagement**: Tracking real-time interactions from users, ranging from passive views (**Impressions**) to active engagement (**Clicks**, **Likes**, **Shares**) and final conversions (**Purchases**).
4. **Audience Demographics**: Mapping these interactions back to user profiles (country, age group, specific interests) to see who is actually responding to the ads.

### Motivation for Building the Data Warehouse (DW)

The primary goal is to transform raw transactional logs into **Actionable Business Intelligence**. The specific motivations are:

* **Centralization**: Consolidating data from separate sources (Campaign spreadsheets, Ad platform exports, and User databases) into a single "Single Source of Truth."
* **ROI Analysis**: Calculating the **Return on Ad Spend (ROAS)** by comparing campaign budgets against the resulting purchase events.
* **Audience Optimization**: Identifying "high-value" demographics to refine future targeting and reduce wasted ad spend.
* **Temporal Trends**: Analyzing how ad performance fluctuates by time of day or day of the week to optimize scheduling (e.g., "Do users click more on Friday evenings?").
* **Query Performance**: Moving from a normalized operational structure to a **Star Schema** specifically designed for fast analytical queries and aggregations in BI tools.

---

## 2. Description of Used Technologies

To build this solution on a **Linux environment**, a robust and open-source stack has been selected:

### Database & Storage

* **SQLite**: Chosen as the core RDBMS. It is native to Linux, requires no server setup (serverless), and stores the entire database in a single portable file. It is perfect for a lightweight yet powerful Data Warehouse.
* **SQL (Structured Query Language)**: Used for creating the schema, performing data transformations (DML), and extracting insights.

### Platform & OS

* **Linux (Ubuntu/Debian/Fedora)**: The host operating system. Its native support for SQLite and its ability to host BI tools via Docker or local services makes it the ideal environment for data engineering.
* **CSV Files**: Used as the initial data source format for easy extraction and portability.

### Business Intelligence (BI) & Visualization

* **Metabase** (Recommended): An open-source BI tool that runs on Linux (as a `.jar` or Docker container). It connects natively to SQLite and allows for the creation of interactive dashboards without requiring deep coding knowledge.
* **Alternative: Apache Superset**: A high-performance visualization engine frequently used in Linux environments for more complex data explorations and large-scale dashboards.

### Data Processing (ETL)

* **Python (Optional but Recommended)**: Using libraries like `pandas` or `sqlite3` on Linux to automate the cleaning, joining, and loading of the CSV files into the SQLite Star Schema.
* **Cron (Linux Task Scheduler)**: Can be used to automate the update of the Data Warehouse if the source CSVs are updated regularly.