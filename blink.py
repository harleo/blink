# Blink v1.0 by https://github.com/harleo

# pylint: disable=no-value-for-parameter

from selenium import webdriver
import click
import ssl
import os

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
def main(input_file, window_size, time_out):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=%s" % window_size)

    url_list = [line.rstrip() for line in open(input_handler(input_file), 'r')]

    page_amount = len(url_list)
    page_counter = 0

    print("[:] Processing %s URL(s)" % (page_amount))

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(time_out)

    for url in url_list:
        try:
            page_counter += 1
            print("[%d/%d] Opening %s" % (page_counter, page_amount, url))
            driver.get("https://" + url)
            driver.get_screenshot_as_file("screenshots/" + url + ".png")
        except:
            print("[!] Couldn't save %s, skipping..." % (url))

    driver.quit()
    print("[:] Done processing %s" % input_handler(input_file))

if __name__ == "__main__":
    main()