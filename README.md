
# Wind Temperature Visualizer

A Streamlit-based web application for visualizing wind and temperature data from EPW (EnergyPlus Weather) files. This tool provides interactive charts and analysis for weather data visualization and analysis.

## Features

- Interactive wind and temperature data visualization
- Support for EPW weather file format
- Real-time data filtering and analysis
- Responsive web interface built with Streamlit
- Comprehensive weather data insights

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wind-temperature-visualizer.git
cd wind-temperature-visualizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/wind_temp_visualizer.py
```

## Usage

1. Launch the application using the command above
2. Upload your EPW weather data file
3. Explore the interactive visualizations
4. Filter and analyze the data as needed

## File Structure

```
wind-temperature-visualizer/
├── src/                    # Source code
├── scripts/               # Installation and utility scripts
├── docs/                  # Documentation
├── examples/              # Sample EPW files and usage examples
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── README.md             # This file
```

## Dependencies

- streamlit: Web application framework
- pandas: Data manipulation and analysis
- plotly: Interactive plotting library
- pvlib: Solar position and irradiance modeling
- numpy: Numerical computing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
