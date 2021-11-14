import typer
import srsly
import pickle
from pathlib import Path
from spacy.util import get_words_and_spaces
from spacy.tokens import Doc, DocBin
import spacy


def main(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_path: Path = typer.Argument(..., dir_okay=False),
):
    nlp = spacy.blank("en")
    training_data = pickle.load(open(input_path, "rb"))
    db = DocBin()
    for text, entities in training_data:
        doc = nlp(text)
        ents = []
        entities_list = entities["entities"]
        for start, end, label in entities_list:
            span = doc.char_span(start, end, label=label)
            ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

if __name__ == "__main__":
    typer.run(main)
    
