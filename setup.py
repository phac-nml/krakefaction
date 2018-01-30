from setuptools import find_packages, setup

setup(
    name='krakefaction',
    version='0.1.0',
    license='Apache-2.0',
    author='Eric Marinier',
    author_email='eric.marinier@canada.ca',
    description='Rarefaction data generation.',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points={
        'console_scripts': [
            'krakefaction = krakefaction.Krakefaction:main',
        ],
    },
)

