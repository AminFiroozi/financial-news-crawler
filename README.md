# Financial News Crawler

A Python-based tool to collect, parse, and store financial news from specified APIs and sources. The crawler supports filtering by keywords, companies, dates, or categories, and saves results in structured formats such as JSON, CSV, or databases.

## Features

-   Fetch financial news from multiple APIs or sources.
-   Filter news by date, keyword, company, or category.
-   Store results in JSON, CSV, or database formats.
-   Avoid duplicate entries with crawling history tracking.
-   Logging and error handling for reliable operation.
-   Modular and extensible codebase for easy maintenance.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/financial-news-crawler.git
cd financial-news-crawler
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file for API keys:

```env
API_KEY=your_api_key_here
```

## Usage

Run the crawler:

```bash
python src/crawler.py
```

Example with custom parameters:

```bash
python src/crawler.py --source "exampleAPI" --keyword "Tesla" --from_date "2025-01-01" --to_date "2025-09-01"
```

## Project Structure

```
financial-news-crawler/
│
├── src/                    # Source code
│   ├── crawler.py          # Core crawling logic
│   ├── parser.py           # Parse news data
│   ├── storage.py          # Save news to DB/JSON/CSV
│   ├── config.py           # API keys, endpoints, parameters
│   └── utils.py            # Helper functions
│
├── tests/                  # Unit tests
│   └── test_crawler.py
│
├── data/                   # Sample data (optional)
│   └── sample_news.json
│
├── notebooks/              # Optional analysis
│   └── analysis.ipynb
│
├── docs/                   # Optional documentation
│   └── architecture.md
│
├── requirements.txt        # Python dependencies
├── README.md
├── LICENSE
└── .gitignore
```

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push to your branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
