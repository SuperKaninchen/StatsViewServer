from setuptools import setup, find_packages

setup(
    name = 'statsviewer_SuperKaninchen',
    version = '0.0.1',
    install_requires = [
        "flask", "rrdtool", "psutil", "argparse"
    ],
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'statsviewer = statsviewer_SuperKaninchen.statsviewer:main'
        ]
    }
)