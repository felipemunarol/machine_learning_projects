from setuptools import setup, find_packages

setup(
    name='jformat',
    version='0.0.1',
    install_requires=["click", "colorama"],
    entry_points="""
    [console_scripts]
    jformat=jformat.code_03:main
    """,
    author="Felipe Munaro",
    author_email="felipemunarolima@gmail.com",
    packages=find_packages()
)


