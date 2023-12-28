import re, argparse, random, colorama

from selenium import webdriver

from selenium.common.exceptions import TimeoutException, WebDriverException

from datetime import datetime

from colorama import Fore, Style

colorama.init(autoreset=True)

green = Fore.GREEN

magenta = Fore.MAGENTA

cyan = Fore.CYAN

mixed = Fore.RED + Fore.BLUE

red = Fore.RED

blue = Fore.BLUE

yellow = Fore.YELLOW

white = Fore.WHITE

colors = [magenta, cyan, mixed, red, blue, yellow, white]

random_color = random.choice(colors)

bold = Style.BRIGHT

parser = argparse.ArgumentParser(
    description=f"{bold}{random_color}JSScanner is a tool designed to efficiently scan to find Sensitive Files like API keys, Emails, Phone No, URLs etc....."
)

parser.add_argument(
    '-l', '--list', metavar='list', type=str, required=True, help=f"[{bold}{random_color}INFO]: {bold}{random_color}List of JS URLs."
)

parser.add_argument(
    '-o', '--output', metavar='output', type=str, default="JsScanner.txt",
    help=f"[{bold}{random_color}INFO]: {bold}{random_color}File to save our output."
)

args = parser.parse_args()

list_file_path = args.list

output_file_path = args.output


def check_dependencies():
    
    try:
        
        import selenium
        
    except ImportError:
        
        print("Please install the 'selenium' package using 'pip install selenium'.")
        
        sys.exit(1)

    try:
        
        import colorama
        
    except ImportError:
        
        print("Please install the 'colorama' package using 'pip install colorama'.")
        
        sys.exit(1)


def process_js_url(driver, js_url, output_lines):
    
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


def main():
    
    banner()
    
    check_dependencies()

    # Create a new instance of the Firefox driver
    options = webdriver.FirefoxOptions()
    
    options.headless = True
    
    driver = webdriver.Firefox(options=options)

    # Read the file containing JS URLs
    with open(list_file_path) as f:
        
        js_urls = f.read().splitlines()

    output_lines = []

    for js_url in js_urls:
        
        process_js_url(driver, js_url, output_lines)

    # Save the output to a file
    with open(output_file_path, 'w') as f:
        
        f.writelines(output_lines)

    # Close the driver
    driver.quit()


if __name__ == "__main__":
    
   # Define the regex patterns
     patterns = {
    'api_key': re.compile(r'[A-Za-z0-9]{32}'),
    'creds': re.compile(r'(?:password|passwd|pwd|user|key|username|usr|email|e-mail|mail)\s*=\s*[\'"]?([A-Za-z0-9@#$%^&*()_+-]+)'),
    'personal_data': re.compile(r'(?:name|email|phone)\s*=\s*[\'"]?([^\'" >]+)'),
    'token': re.compile(r'[A-Za-z0-9-_]{64}'),
    'url': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
    'custom_pattern': re.compile(r'(?i)((access_key|access_token|admin_pass|admin_user|algolia_admin_key|algolia_api_key|alias_pass|alicloud_access_key|amazon_secret_access_key|amazonaws|ansible_vault_password|aos_key|api_key|api_key_secret|api_key_sid|api_secret|api.googlemaps AIza|apidocs|apikey|apiSecret|app_debug|app_id|app_key|app_log_level|app_secret|appkey|appkeysecret|application_key|appsecret|appspot|auth_token|authorizationToken|authsecret|aws_access|aws_access_key_id|aws_bucket|aws_key|aws_secret|aws_secret_key|aws_token|AWSSecretKey|b2_app_key|bashrc password|bintray_apikey|bintray_gpg_password|bintray_key|bintraykey|bluemix_api_key|bluemix_pass|browserstack_access_key|bucket_password|bucketeer_aws_access_key_id|bucketeer_aws_secret_access_key|built_branch_deploy_key|bx_password|cache_driver|cache_s3_secret_key|cattle_access_key|cattle_secret_key|certificate_password|ci_deploy_password|client_secret|client_zpk_secret_key|clojars_password|cloud_api_key|cloud_watch_aws_access_key|cloudant_password|cloudflare_api_key|cloudflare_auth_key|cloudinary_api_secret|cloudinary_name|codecov_token|config|conn.login|connectionstring|consumer_key|consumer_secret|credentials|cypress_record_key|database_password|database_schema_test|datadog_api_key|datadog_app_key|db_password|db_server|db_username|dbpasswd|dbpassword|dbuser|deploy_password|digitalocean_ssh_key_body|digitalocean_ssh_key_ids|docker_hub_password|docker_key|docker_pass|docker_passwd|docker_password|dockerhub_password|dockerhubpassword|dot-files|dotfiles|droplet_travis_password|dynamoaccesskeyid|dynamosecretaccesskey|elastica_host|elastica_port|elasticsearch_password|encryption_key|encryption_password|env.heroku_api_key|env.sonatype_password|eureka.awssecretkey)[a-z0-9_ .\-,]{0,25})(=|>|:=|\|\|:|<=|=>|:).{0,5}['\"]([0-9a-zA-Z\-_=]{8,64})['\"]')
    }

    main()
