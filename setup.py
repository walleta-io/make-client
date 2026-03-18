from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open('make/__version__.py', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name='make-client',
    version=about['__version__'],
    description='Minimal Python client for the make.com API v2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'make-client=make.__main__:main',
        ],
    },
)
