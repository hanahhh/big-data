from setuptools import setup, find_packages

try:
    from pypandoc import convert_file
    read_md = lambda f: convert_file(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

INSTALL_REQUIRES = (
    ['pandas>=0.19.2', 'numpy>=1.20.2', 'requests>=2.3.0', 'wrapt>=1.10.0', 'lxml>=4.3.0', 'pypandoc>=1.4', 'plotly>=4.2.1', 'bs4>=0.0.1']
)

DESCRIPTION = 'Viet Nam stock market'

setup(
      description=DESCRIPTION,
      packages=find_packages(exclude = ['contrib', 'docs', 'tests*']),
      classifiers=[
        'Development Status :: 0 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Trader/Investor/Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Financial/Stock Market',
      ],
      keywords = 'data',
      install_requires=INSTALL_REQUIRES,
      zip_safe=False,
     )