import re
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import colorama
import argparse


from colorama import Fore, Back, Style
colorama.init(autoreset=True)
green = Fore.GREEN
magenta = Fore.MAGENTA
cyan = Fore.CYAN
mixed = Fore.RED + Fore.BLUE
red = Fore.RED
blue = Fore.BLUE
yellow = Fore.YELLOW
white = Fore.WHITE
colors = [magenta,cyan,mixed,red,blue,yellow, white]
random_color = random.choice(colors)
bold = Style.BRIGHT


parser=argparse.ArgumentParser(description=f"{bold}{random_color}JSScanner is a tool designed to efficiently scan to find Sensitive Files like API keys, Emails, Phone No, URLs etc.....")
parser.add_argument('-l','--list',metavar='list',type=str,required=True,help=f"[{bold}{random_color}INFO]: {bold}{random_color}List of JS URLs.")
parser.add_argument('-o','--output',metavar='output',type=str,default="output.txt",help=f"[{bold}{random_color}INFO]: {bold}{random_color}File to save our output.")
args=parser.parse_args()
list=args.list
output=args.output


def banner():

    print(f'''{bold}{random_color}


░░░░░██╗░██████╗░░░░██████╗░█████╗░░█████╗░███╗░░██╗███╗░░██╗███████╗██████╗░
░░░░░██║██╔════╝░░░██╔════╝██╔══██╗██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗
░░░░░██║╚█████╗░░░░╚█████╗░██║░░╚═╝███████║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
██╗░░██║░╚═══██╗░░░░╚═══██╗██║░░██╗██╔══██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
╚█████╔╝██████╔╝██╗██████╔╝╚█████╔╝██║░░██║██║░╚███║██║░╚███║███████╗██║░░██║
░╚════╝░╚═════╝░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝

        Author   : Aashish💕💕  
                                              
        Github   : https://github.com/aashis36
        
''')


# Define the regex patterns
patterns = {
    'api_key': re.compile(r'[A-Za-z0-9]{32}'),
    'creds': re.compile(r'(?:password|passwd|pwd|user|key|username|usr|email|e-mail|mail)\s*=\s*[\'"]?([A-Za-z0-9@#$%^&*()_+-]+)'),
    'personal_data': re.compile(r'(?:name|email|phone)\s*=\s*[\'"]?([^\'" >]+)'),
    'token': re.compile(r'[A-Za-z0-9-_]{64}'),
    'url': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
}

js_file_path = list

banner()

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()



# Read the file containing JS URLs
with open(js_file_path) as f:
    js_urls = f.read().splitlines()

output_lines = []

for js_url in js_urls:

    output_lines.append(f'Processing JS URL: {js_url}\n')

    print(f'{bold}{random_color}Processing JS URL: {js_url}\n')

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
            print(f"{bold}{random_color}Sensitive data found:\n")
            for pattern_name in patterns:
                pattern = patterns.get(pattern_name)
                pattern_matches = pattern.findall(javascript_code)
                if pattern_matches:
                    output_lines.append(f'{pattern_name.upper()} Found:')
                    print(f'{bold}{random_color}{pattern_name.upper()} Found:')
                    for match in pattern_matches:
                        output_lines.append(f'- {match}')
                        print(f'{bold}{random_color}- {match}')
                    output_lines.append('')
                    print('')
        else:
            output_lines.append("No sensitive data found.\n")
            print(f"{bold}{random_color}No sensitive data found.\n")

    except TimeoutException:
        output_lines.append("Timeout error occurred while loading the URL.\n")
    except WebDriverException:
        output_lines.append("WebDriver error occurred while processing the URL.\n")

# Save the output to a file
with open('output.txt', 'w') as f:
    f.write('\n'.join(output_lines))

# Close the driver
driver.quit()
