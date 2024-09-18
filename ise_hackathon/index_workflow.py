# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License
import asyncio
import os
 
from graphrag.index import run_pipeline, run_pipeline_with_config
from graphrag.index.config import PipelineTextInputConfig, PipelineWorkflowReference
from graphrag.index.input import load_input
 
input_data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "input_data"
)

output_data_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "output_data"
)
 
# Load our dataset once
dataset = asyncio.run(
    load_input(
        PipelineTextInputConfig(
            file_pattern=".*\\.txt$",
            base_dir=input_data_dir,
            encoding="utf-8"
        ),
    )
)
 
async def run_index_workflow():
    """
    Run a pipeline workflow with a custom configuration.

    For the ISE hackathon, we will be using the entity_extraction workflow
    """
    workflows: list[PipelineWorkflowReference] = [
        # This workflow reference here is only necessary
        # because we want to customize the entity_extraction workflow is configured
        # otherwise, it can be omitted, but you're stuck with the default configuration for entity_extraction
        PipelineWorkflowReference(
            name="create_base_extracted_entities",
            config={
                "entity_extract": {
                    "strategy": {
                        "type": "nltk",
                    }
                }
            },
        )
    ]
 
    # Grab the last result from the pipeline, should be our entity extraction
    tables = []
    async for table in run_pipeline(dataset=dataset, workflows=workflows):
        tables.append(table)

    pipeline_result = tables[-1]

    base_extracted_entities = pipeline_result.result["entity_graph"]

    base_extracted_entities = base_extracted_entities[0]

    with open(os.path.join(output_data_dir,"base_extracted_entities.xml"), "w") as f:
        f.write(base_extracted_entities)
    
if __name__ == "__main__":
    asyncio.run(run_index_workflow())
 