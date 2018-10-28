# Blink v1.1 by https://github.com/harleo

# Suppress false flag pylint warning about click
# pylint: disable=no-value-for-parameter

from selenium import webdriver
import click
import ssl
import os

from selenium.common.exceptions import WebDriverException


def check_ssl(func):
    def wrap(*args, **kwargs):
        if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
            ssl, "_create_unverified_context", None
        ):
            ssl._create_default_https_context = ssl._create_unverified_context
        return func(*args, **kwargs)

    return wrap


def input_handler(input_file):
    if ".txt" in input_file:
        return input_file
    else:
        return input_file + ".txt"


def output_handler(output_folder):
    if not os.path.exists(output_folder):
        print(f"[:] Creating {output_folder} folder...")
        os.makedirs(output_folder)
        return output_folder
    else:
        return output_folder


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-i",
    "--input",
    "input_file",
    type=str,
    required=True,
    help="name of the input file (must be text file format; urls line by line).",
)
@click.option(
    "-o",
    "--output",
    "output_folder",
    type=str,
    default="screenshots",
    show_default=True,
    help="name of the folder to save the screenshots to.",
)
@click.option(
    "-ws",
    "--windowsize",
    "window_size",
    type=str,
    default="1200x600",
    show_default=True,
    help="window size of the screenshot.",
)
@click.option(
    "-to",
    "--timeout",
    "time_out",
    type=int,
    default="10",
    show_default=True,
    help="web page request timeout in seconds.",
)
@click.option(
    "-f",
    "--format",
    "file_format",
    type=str,
    default="png",
    show_default=True,
    help="output file format.",
)
@click.option(
    "-f",
    "--format",
    "file_format",
    default="png",
    show_default=True,
    type=click.Choice(["png", "jpg"]),
    help="set output file format: 'png' or 'jpg'."
)
@check_ssl
def main(input_file, output_folder, window_size, time_out, file_format):
    """ Orchestrator for storing screenshots of web pages """

    output_location = output_handler(output_folder)

    driver_options = get_driver_options(window_size)

    url_list = url_list_from_file(input_file)

    # DeprecationWarning: use options instead of chrome_options driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome(options=driver_options)
    driver.set_page_load_timeout(time_out)

    process_urls(url_list, output_location, driver)

    print(f"[:] Done processing {input_file}")


def process_urls(url_list, output_location, driver):
    """
    Process the list of URLs, visiting each page and saving a screenshot of the page to the target location directory.
    :param url_list: list-like object of pages to visit
    :param output_location: directory to store the screenshots in
    :param driver: driver that is capable of GET'ing a URL and saving the picture of it
    """
    page_counter = 0
    print(f"[:] Processing {len(url_list)} URL(s)")

    for url in url_list:
        page_counter += 1
        print(f"[{page_counter}/{len(url_list)}] Opening {url}")

        try:
            driver.get("http://" + url)
            driver.save_screenshot(output_location + "/" + url + "." + file_format)

        except WebDriverException as wde:
            print(f"[!] Error retrieving web page '{url}'. Exception:\n{wde}")

        except IOError:
            print(f"[!] Couldn't save {url}, skipping...")

    driver.quit()


def url_list_from_file(input_file='example.txt'):
    """
    Read the specified file and return all lines inside the file, as a list of lines.
    :param input_file: path to an input file
    :return: list of lines in the file, e.g. URLs separated by new-line
    """
    return [line.rstrip() for line in open(input_handler(input_file), 'r')]


def get_driver_options(window_size):
    """
    Default driver options, using the specified window size
    :param window_size: the size of the browser window and effectively the screenshots
    :return: options for the driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument(f"window-size={window_size}")
    return options


if __name__ == "__main__":
    main()
