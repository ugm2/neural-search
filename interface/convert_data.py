"""Utilities to convert input document formats to a consistent format for the demo.

Target format:
{
    "id1": 
        {
            "text": "whatever text",
            "tags": []
        },
        ...
}
"""
from curses import meta
import json
import uuid

import pandas as pd


def parse_tags(tags):
    processed_tags = json.loads(tags.replace("'", '"'))
    return list(
        set(
            [tag["text"] for tag in processed_tags]
            + [tag["sem_type"] for tag in processed_tags]
        )
    )


def parse_from_cvs(dataframe_filename, text_field, metadata_fields=[], id_field=None):
    df = pd.read_csv(dataframe_filename)

    documents = {}
    for _, row in df.iterrows():
        doc = {"text": row[text_field]}
        if metadata_fields != []:
            for metadata_field in metadata_fields:
                if metadata_field == "tags":
                    doc[metadata_field] = parse_tags(row[metadata_field])
                else:
                    doc[metadata_field] = row[metadata_field]
        if id_field is not None:
            _id = row[id_field]
        else:
            _id = str(uuid.uuid4())
        documents[_id] = doc
    return documents


def csv_to_json(
    dataframe_filename, json_filename, text_field, metadata_fields, id_field
):
    parsed_content = parse_from_cvs(
        dataframe_filename, text_field, metadata_fields, id_field
    )

    with open(json_filename, "w") as f:
        json.dump(parsed_content, f)


if __name__ == "__main__":
    csv_to_json(
        dataframe_filename="data/passages_coronavirus.csv",
        json_filename="data/coronavirus.json",
        text_field="passage",
        metadata_fields=["tags"],
        id_field=None,
    )
