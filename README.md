# ML4Good Project

This project aims to help you learn any concepts, by asking you to explain it and checking your understanding. It uses Gradio as an interface to interact with the Anthropic API. Built with Python, a blanket, and a mug of tea.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

This project uses Poetry for dependency management. To set up the project, follow these steps:

1. Make sure you have Poetry installed. If not, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).

2. Clone the repository:
   ```
   git clone https://github.com/yourusername/ml4good.git
   cd ml4good
   ```

3. Install the dependencies:
   ```
   poetry install
   ```

## Configuration

The project configuration, including the concept list and LLM choice, is managed through the `ml4good/config.py` file. You can override it with your specific configuration before running the project.

## Usage

To run the Gradio interface:

1. Activate the Poetry environment:
   ```
   poetry shell
   ```

2. Run the main script:
   ```
   gradio ml4good/main.py
   ```

3. Open your web browser and navigate to the URL provided in the console output (typically `http://127.0.0.1:7860`).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.