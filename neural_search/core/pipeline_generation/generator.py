# -*- coding: utf-8 -*-
"""
Pipeline Generator Tool
"""

# Copyright Unai Garay Maestre

import json
import os
import logging
from haystack import Pipeline
from PIL import Image

logger = logging.getLogger("Pipeline Generator")
logger.setLevel(os.getenv("LOGGER_LEVEL", logging.ERROR))

pipeline_json_filename = os.environ.get("PIPELINE_JSON_FILENAME", "/pipeline.json")
search_parameters_json_filename = os.environ.get(
    "SEARCH_PARAMETERS_JSON_FILENAME", "/search_parameters.json"
)
index_parameters_json_filename = os.environ.get(
    "INDEX_PARAMETERS_JSON_FILENAME", "/index_parameters.json"
)


class PipelineGenerator:
    """
    Class to generate config files (json) for Haystack Pipelines
    """

    def generate(
        self,
        index_pipeline: Pipeline,
        search_pipeline: Pipeline,
        pipeline_name: str,
        folder: str,
        draw_pipeline: bool = True,
        save_pipeline: bool = True,
    ):
        """Generate config files (json) given index and search pipelines

        Args:
            index_pipeline (Pipeline): Indexing pipeline
            search_pipeline (Pipeline): Searching/Querying pipeline
            pipeline_name (str): Name of the folder that will be created. It should be a meaningful name
            folder (str): Folder where the Pipeline folder and its JSON files will be generated
            draw_pipeline (bool, optional): Whether to draw the pipelines. They will be saved as a pipeline.png. Defaults to True.
            save_pipeline (bool, optional): Whether to save the pipeline (locally). Defaults to True.
        """
        logging.info("Generating config files for Haystack Pipelines...")

        if draw_pipeline or save_pipeline:
            path = os.path.join(folder, pipeline_name)
            logging.info(f"Creating folder '{path}'")
            os.makedirs(path, exist_ok=True)

        if draw_pipeline:
            logging.info("Drawing pipeline graph...")
            search_path = path + "/search_pipeline.png"
            index_path = path + "/indexing_pipeline.png"
            search_pipeline.draw(search_path)
            index_pipeline.draw(index_path)
            self._join_pipelines_images(path, search_path, index_path)

        if save_pipeline:
            logging.info("Saving config files...")
            (
                pipeline,
                search_params,
                indexing_params,
            ) = self._get_pipeline_and_parameters(search_pipeline, index_pipeline)
            self._save_jsons(path, pipeline, search_params, indexing_params)

    def _separate_pipeline_parameters(self, pipeline_json):
        parameters = {}
        for component in pipeline_json["components"]:
            if "params" in component:
                parameters[component["name"]] = {
                    "create_parameters": component["params"]
                }
                del component["params"]
        return pipeline_json, parameters

    def _unite_pipelines(self, search_pipeline, indexing_pipeline):
        pipeline = search_pipeline.copy()
        pipeline["pipelines"].extend(indexing_pipeline["pipelines"])
        pipeline_components_names = [c["name"] for c in pipeline["components"]]
        for indexing_component in indexing_pipeline["components"]:
            if indexing_component["name"] not in pipeline_components_names:
                pipeline["components"].append(indexing_component)
        return pipeline

    def _get_pipeline_and_parameters(self, search_pipeline, indexing_pipeline):
        search_json = search_pipeline.get_config()
        indexing_json = indexing_pipeline.get_config()
        search_pipeline, search_params = self._separate_pipeline_parameters(search_json)
        indexing_pipeline, indexing_params = self._separate_pipeline_parameters(
            indexing_json
        )
        pipeline = self._unite_pipelines(search_pipeline, indexing_pipeline)
        return pipeline, search_params, indexing_params

    def _save_jsons(self, path, pipeline, search_params, indexing_params):
        jsons = [pipeline, search_params, indexing_params]
        filenames = [
            pipeline_json_filename,
            search_parameters_json_filename,
            index_parameters_json_filename,
        ]
        for filename, _json in zip(filenames, jsons):
            with open(path + filename, "w") as f:
                json.dump(_json, f, indent=4)

    def _join_pipelines_images(self, path, path1, path2):
        try:
            images = [Image.open(path1), Image.open(path2)]
            widths, heights = zip(*(i.size for i in images))
            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new(
                "RGB", (total_width, max_height), color=(255, 255, 255, 0)
            )
            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset, 0))
                x_offset += im.size[0]

            new_im.save(path + "/pipeline.png")
        except Exception as e:
            logger.error(e)
        finally:
            os.remove(path1)
            os.remove(path2)


if __name__ == "__main__":
    from neural_search.core.pipeline_generation.pipelines import keyword_search_pipeline

    search_pipeline, index_pipeline = keyword_search_pipeline(
        es_endpoint="127.0.0.1", es_port=9200, index="documents"
    )

    pipeline_generator = PipelineGenerator()
    pipeline_generator.generate(
        index_pipeline=index_pipeline,
        search_pipeline=search_pipeline,
        # Name of the folder that will be created.
        # It should be a meaningful name, like KeywordSearch
        pipeline_name="PipelineTest",
        # Folder where the Pipeline folder and its JSON files will be generated
        folder="test_data/json_pipelines/",
        # Whether to draw the pipelines. They will be saved as a pipeline.png
        draw_pipeline=True,
    )
