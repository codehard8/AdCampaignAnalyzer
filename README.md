# AdCampaignAnalyzer

AdCampaignAnalyzer is a Streamlit-based application designed to help kitchen and bathroom remodeling businesses analyze their advertising campaigns. It provides tools to evaluate, compare, and report on various ad metrics to optimize the performance of ad campaigns.

## Features
- **Home Page**: Overview of the application.
- **Search by Metric**: Search and filter ads based on specific metrics.
- **Analysis and Report**: Detailed analysis and performance reports for individual ads.
- **Compare Metrics**: Compare multiple ads against benchmarks.

## Installation
### Clone the repository:
```sh
git clone https://github.com/codehard8/AdCampaignAnalyzer.git
cd AdCampaignAnalyzer
```

### Install the required packages:
```sh
pip install -r requirements.txt
```

### Run the application:
```sh
streamlit run app.py
```

## Modules
### `app.py`
The main entry point of the application that sets up the Streamlit interface and navigation menu.

### `modules/analysis_and_report.py`
Provides functionality to analyze individual ad performance and generate detailed reports, including key metrics summary, performance classification, and visualizations using various chart types (Lollipop, Bar, Spider, Line).

### `modules/benchmarks.py`
Contains benchmark values for key metrics specific to kitchen and bathroom renovation ad campaigns. These benchmarks are used for performance comparisons.

### `modules/compare_metrics.py`
Allows users to compare multiple ads against benchmarks. It provides visualizations to compare different metrics using bar and line charts.

## Usage
1. **Home Page**: Start by navigating to the Home page.
2. **Upload Data**: Upload your dataset in the campaign section to enable analysis and comparisons.
3. **Search by Metric**: Use the "Search by Metric" section to filter ads based on specific metrics.
4. **Analysis and Report**: Navigate to "Analysis and Report" to get detailed insights into individual ad performance.
5. **Compare Metrics**: Use the "Compare Metrics" section to compare multiple ads and visualize their performance against benchmarks.

## Contributing
Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License
This project is licensed under the MIT License.
