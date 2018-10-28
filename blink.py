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
    help="webpage request timeout in seconds.",
)
@check_ssl
def main(input_file, output_folder, window_size, time_out):
    output_location = output_handler(output_folder)

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=%s" % window_size)

    url_list = [line.rstrip() for line in open(input_handler(input_file), 'r')]

    page_amount = len(url_list)
    page_counter = 0

    print(f"[:] Processing {page_amount} URL(s)")

    # DeprecationWarning: use options instead of chrome_options driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(time_out)

    for url in url_list:
        try:
            page_counter += 1
            print(f"[{page_counter}/{page_amount}] Opening {url}")
            driver.get("https://" + url)
            driver.save_screenshot(output_location + "/" + url + ".png")

        except WebDriverException as wde:
            print(f"[!] Error retrieving web page '{url}'. Exception:\n{wde}")

        except IOError:
            print(f"[!] Couldn't save {url}, skipping...")

    driver.quit()
    print(f"[:] Done processing {input_file}")


if __name__ == "__main__":
    main()
