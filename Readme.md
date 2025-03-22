# PlayWright-Python Automation Project

This project is designed to automate SauceDemo website using the Playwright
framework and Python.

## Requirements
1. Python 3.10 and above
2. allure installed on your machine: 
[Allure Installation guide](https://allurereport.org/docs/install/)

## Setup
1. Clone the repository
2. Setup a virtual environment (Optional)
3. Install the required packages:
```sh
  pip install -r requirements.txt
```
4. Install playwright browsers (use elevated permissions if needed):
```sh
  playwright install
```

## Configuration

Update the `config.json` file with the appropriate settings for your environment.

## Running the Tests

1.To run the tests cd to tests execute the following command:
```sh
  pytest
```
you can add more playwright arguments to fit your needs for example:
```sh
  pytest --browser=firefox --headed
```
By default, tests will run on chromium based browser and headless.

experiment with different args more information can be found [here](https://playwright.dev/python/docs/test-runners#cli-arguments)

2.To generate an Allure report use the following command:
 ```sh
   allure serve allure-results
 ```

## License

This project is licensed under the MIT License.
