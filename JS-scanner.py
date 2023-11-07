import re
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException

print('''


░░░░░██╗░██████╗░░░░██████╗░█████╗░░█████╗░███╗░░██╗███╗░░██╗███████╗██████╗░
░░░░░██║██╔════╝░░░██╔════╝██╔══██╗██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗
░░░░░██║╚█████╗░░░░╚█████╗░██║░░╚═╝███████║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
██╗░░██║░╚═══██╗░░░░╚═══██╗██║░░██╗██╔══██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
╚█████╔╝██████╔╝██╗██████╔╝╚█████╔╝██║░░██║██║░╚███║██║░╚███║███████╗██║░░██║
░╚════╝░╚═════╝░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝

        Author   : Aashish💕💕  
                                              
        Github   : https://github.com/aashish36
        
        Just wait things takes time.................
        
        Output will be stored in current folder😎😎
        
''')

# Define the regex patterns
patterns = {
    'api_key': re.compile(r'[A-Za-z0-9]{32}'),
    'creds': re.compile(r'(?:password|passwd|pwd|user|username|usr|email|e-mail|mail)\s*=\s*[\'"]?([A-Za-z0-9@#$%^&*()_+-]+)'),
    'personal_data': re.compile(r'(?:name|email|phone)\s*=\s*[\'"]?([^\'" >]+)'),
    'token': re.compile(r'[A-Za-z0-9-_]{64}'),
    'url': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
}

# Get the file path argument from the command line
if len(sys.argv) < 2:
    print("Please provide the path to the file containing JS URLs")
    sys.exit(1)

js_file_path = sys.argv[1]

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# Read the file containing JS URLs
with open(js_file_path) as f:
    js_urls = f.read().splitlines()

output_lines = []

for js_url in js_urls:
    output_lines.append(f'Processing JS URL: {js_url}\n')

    try:
        # Navigate to the JavaScript file
        driver.set_page_load_timeout(10)
        driver.get(js_url)

        # Retrieve the contents of the file
        javascript_code = driver.execute_script("return document.documentElement.innerText")

        # Check for sensitive data in the file
        matches = [pattern.findall(javascript_code) for pattern in patterns.values()]

        if any(matches):
            output_lines.append("Sensitive data found:\n")
            for pattern_name in patterns:
                pattern = patterns.get(pattern_name)
                pattern_matches = pattern.findall(javascript_code)
                if pattern_matches:
                    output_lines.append(f'{pattern_name.upper()} Found:')
                    for match in pattern_matches:
                        output_lines.append(f'- {match}')
                    output_lines.append('')
        else:
            output_lines.append("No sensitive data found.\n")

    except TimeoutException:
        output_lines.append("Timeout error occurred while loading the URL.\n")
    except WebDriverException:
        output_lines.append("WebDriver error occurred while processing the URL.\n")

# Save the output to a file
with open('output.txt', 'w') as f:
    f.write('\n'.join(output_lines))

# Close the driver
driver.quit()
