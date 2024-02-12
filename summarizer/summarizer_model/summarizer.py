import os
import click
from transformers import pipeline


def summarize_model(file):

    with open(file, 'r') as _f:
        phase = _f.read()

    model = pipeline("text2text-generation", model="t5-base")
    phase_summarized = model('Summarize: {}'.format(phase))
    print(phase_summarized)

@click.command()
@click.argument('file')
def main(file):
    summarize_model(file)
    

if __name__=='__main__':
    main()