# JS Code Scanner

[Tool link](https://github.com/aashishsec/JS.Scanner)

## Introduction

- JSScanner is a Python tool that uses Selenium to scan JavaScript files for sensitive information.
  
- It reads a list of JavaScript file URLs, loads each URL in a headless Firefox browser, extracts the JavaScript code, and searches for predefined patterns indicative of sensitive information using regular expressions.

-  Works in all platforms.
  
## Features

- Scans JavaScript files for sensitive data.
  
- Supports the detection of API keys, credentials, personal data, tokens, and URLs.
  
- Headless browser mode for improved performance.
  
## Installation

- Clone the repository to your local machine.
  
- Install the required dependencies using pip: pip install -r requirements.txt.
  
- Download the latest version of the Firefox WebDriver from here and add it to your PATH environment variable.


```bash
git clone https://github.com/aashish36/JSScanner.git

cd JSScanner

pip install -r requirements.txt

```

## Usage

- Create a file containing the list of URLs to scan, with one URL per line.file.txt should contain all js urls.

- The script will output the results of the analysis to a file named 'output.txt'.

- Run the script using the following command: 

``` bash
python3 JS-scanner.py path/to/url/file.txt

```

## Contributing

- Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.


