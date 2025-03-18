# X.com Poster

A simple Python application that allows you to post to X.com without opening the website, using the Twitter API v2.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## Features

- Web interface to compose and post tweets
- Command-line interface for quick posting
- Character count validation (280 limit)
- Feedback on successful posts or errors
- No need to open X.com in your browser

## Prerequisites

- Python 3.8 or higher
- Twitter Developer Account with API credentials

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nishantkumar1292/x-poster.git
   cd x-poster
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # On macOS/Linux
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Twitter API credentials:
   ```bash
   cp .env.sample .env
   ```

5. Edit the `.env` file with your actual Twitter API credentials.

## Getting X API Credentials

1. Apply for a Twitter Developer account at https://developer.twitter.com/
2. Create a new project and app
3. Enable User Authentication Settings in your app and configure it with OAuth 2.0
4. Generate API keys and tokens (you need the Bearer Token and OAuth 1.0a tokens)
5. Copy these credentials to your `.env` file

**Note:** X API offers different tiers for API access:
- Free tier: Allows posting up to 1,500 tweets per month
- Basic tier ($100/month): Increases limit to 3,000 tweets per month and adds 10,000 pull requests
- Pro tier ($5,000/month): Offers 300,000 tweets and 1,000,000 pull requests
- Enterprise tier: Custom pricing and features

## Usage

### Web Interface

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to http://localhost:5000

3. Type your post and click "Post" to send it to X.com

### Command Line Interface

You can also post directly from the command line:

1. Using direct command with content:
   ```bash
   ./cli.py "Your post content here"
   ```

2. Or using interactive mode (just run without arguments):
   ```bash
   ./cli.py
   ```
   Then type your post and press Enter twice to submit.

### Linting and Code Quality

The project includes a linting script to check and maintain code quality:

1. To check for linting issues (including missing newlines at end of files):
   ```bash
   ./lint.py
   ```

2. To automatically fix formatting issues where possible:
   ```bash
   ./lint.py --fix
   ```

The linting script checks for:
- Files missing a final newline
- Code style issues using flake8
- Formatting issues using black

## Project Structure

```
.
├── app.py              # Flask web application
├── cli.py              # Command-line interface
├── lint.py             # Linting and code quality script
├── requirements.txt    # Python dependencies
├── .env.sample         # Template for environment variables
├── templates/          # HTML templates
│   └── index.html      # Main web interface
├── LICENSE             # MIT License
└── README.md           # This documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For contributing:
1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Run the linting checks: `./lint.py --fix`
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is designed for personal use. Make sure to comply with X.com's Terms of Service when using this application.