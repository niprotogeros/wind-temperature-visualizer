
#!/usr/bin/env python3
"""Setup script for wind-temperature-visualizer."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='wind-temperature-visualizer',
    version='0.1.0',
    author='Wind Temperature Visualizer Team',
    author_email='',
    description='A Streamlit application for visualizing wind speed vs temperature from EPW weather data files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/wind-temperature-visualizer',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=22.0',
            'flake8>=4.0',
            'isort>=5.0',
            'pre-commit>=2.0',
            'mypy>=0.900',
        ],
    },
    entry_points={
        'console_scripts': [
            'wind-temp-visualizer=wind_temp_visualizer:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords='weather, visualization, streamlit, epw, wind, temperature',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/wind-temperature-visualizer/issues',
        'Source': 'https://github.com/yourusername/wind-temperature-visualizer',
        'Documentation': 'https://github.com/yourusername/wind-temperature-visualizer/blob/main/README.md',
    },
)
