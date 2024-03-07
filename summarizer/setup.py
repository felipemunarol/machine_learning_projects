from setuptools import setup, find_packages

setup(
    name='summarizer',
    version='0.0.1',
    install_requires=["click", "transformers"],
    author= 'Felipe Munaro',
    author_email='felipemunaro@gmail.com',
    # scripts="""
    # [console_scripts]
    # summarizer=summarizer.summarizer_model:main
    # """,
    packages=find_packages()
)