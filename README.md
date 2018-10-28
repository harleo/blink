## Blink

Blink is a simple single or bulk web page screenshotting tool, often used for reconnaissance/archival (OSINT) purposes.

### Requirements

`pipenv install`

If you do not have `pipenv` installed, first install it with `pip3 install pipenv`.

### Usage

```console
Usage: blink.py [OPTIONS]

Options:
  -i, --input TEXT        name of the input file (must be text file format;
                          urls line by line).  [required]
  -o, --output TEXT       name of the folder to save the screenshots to.
                          [default: screenshots]
  -ws, --windowsize TEXT  window size of the screenshot.  [default: 1200x600]
  -to, --timeout INTEGER  web page request timeout in seconds.  [default: 10]
  -h, --help              Show this message and exit.
```

### Example

```console
python3 blink.py -i example -o example -ws 1920x1080 -to 5

[:] Creating example folder...
[:] Processing 1 URL(s)
[1/1] Opening acme.com
[:] Done processing example.txt
```

### Format

Input file parsing supports both separation by new-line, comma, a mix of these and either HTTP, HTTPS, or an invalid variation of these, e.g. 'ttp://' or simply '/'

Example:

```txt
acme.com
google.com
amazon.com

https://acme.com
http://google.com
/amazon.com

acme.com, google.com, amazon.com

https://acme.com,http://google.com   ,  /amazon.com,
```

---

&copy; 2018 Leonid Hartmann