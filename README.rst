[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmete0r%2Fktug-hanyang-pua.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmete0r%2Fktug-hanyang-pua?ref=badge_shield)

ktug-hanyang-pua
================

KTUG Hanyang PUA table reader/writer

This package provides reader/writer utility for files from `KTUG Hanyang PUA table project`_.

Note that this package does not handle HanyangPUA-to-UnicodeJamo conversion itself.

.. _KTUG Hanyang PUA table project: http://faq.ktug.org/faq/HanyangPuaTableProject


- Documentation: https://ktug-hanyang-pua.readthedocs.org


Development environment
-----------------------

To setup development environment::

   virtualenv -p python3.8 .
   bin/pip install -U setuptools pip pip-tools
   make
   make test test-report


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmete0r%2Fktug-hanyang-pua.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmete0r%2Fktug-hanyang-pua?ref=badge_large)