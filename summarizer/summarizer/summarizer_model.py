import os   # libraty to interact with the operational system
import click    # library to command line usage
from transformers import pipeline   # libraty to load machine learning models pre-trained

# Ignore some tensorflow low level mensages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"


def summarize_model(file):

    with open(file, 'r') as _f:
        phase = _f.read()

    model = pipeline("text2text-generation", model="t5-base")
    phase_summarized = model('Summarize: {}'.format(phase))
    click.echo("Summarization process finished")
    click.echo("-"*100)
    phase_summarized_text = phase_summarized[0]["generated_text"]
    click.echo("Summarized text from -> {}".format(file))
    click.echo(phase_summarized_text)
    # TODO: persist the output
    # with open(file, 'w') aSs _f:


@click.command()
@click.argument('file')
def main(file):
    summarize_model(file)
    

if __name__=='__main__':
    main()