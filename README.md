JS Code Scanner

This is a Python script that uses the Selenium WebDriver to scan a list of URLs containing JavaScript code, and checks for sensitive information such as API keys, credentials, personal data, tokens, or URLs. The script identifies sensitive data using regular expressions defined in the 'patterns' dictionary.

Installation

Clone the repository to your local machine.
Install the required dependencies using pip: pip install -r requirements.txt
Download the latest version of the Firefox WebDriver from here and add it to your PATH environment variable.

Usage

Create a file containing the list of URLs to scan, with one URL per line.
Run the script using the following command: python js_code_scanner.py path/to/url/file.txt.
file.txt should contain all js urls.
The script will output the results of the analysis to a file named 'output.txt'.

Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
