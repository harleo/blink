import os

import blink


class TestBlink:

    def test_url_list_from_file_one_url(self):
        one_url_path = os.path.join(os.path.dirname(__file__), 'resources', 'one-url.txt')
        urls = blink.url_list_from_file(one_url_path)

        assert 1 == len(urls)
        assert 'acme.com' == urls[0]

    def test_url_list_from_file_multiple_urls(self):
        multiple_url_path = os.path.join(os.path.dirname(__file__), 'resources', 'multiple-urls.txt')
        urls = blink.url_list_from_file(multiple_url_path)

        assert len(urls) == 3
        assert 'acme.com' == urls[0]
        assert 'google.com' == urls[1]
        assert 'amazon.com' == urls[2]

    def test_url_list_from_file_multiple_urls_mixed_format(self):
        multiple_url_path = os.path.join(os.path.dirname(__file__), 'resources', 'multiple-urls-mixed-format.txt')
        urls = blink.url_list_from_file(multiple_url_path)

        expected_urls = [
            'acme.com', 'google.com', 'amazon.com', 'acme.com', 'google.com', 'amazon.com',
            'acme.com', 'google.com', 'amazon.com', 'acme.com', 'google.com', 'amazon.com'
        ]

        assert 12 == len(urls)
        assert expected_urls == urls

    def test_can_get_driver_options(self):
        opts_1 = blink.get_driver_options('800x600')
        opts_2 = blink.get_driver_options('1337x42')

        assert 'window-size=800x600' in opts_1.arguments
        assert 'window-size=1337x42' in opts_2.arguments
