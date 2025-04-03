# ToolUniverse Architecture Guide

This document provides an in-depth overview of the ToolUniverse architecture, highlighting how it wraps various biomedical APIs and explaining the design patterns used to create a unified interface for accessing biomedical data.

## Overview

ToolUniverse is a comprehensive collection of 214+ biomedical tools designed for use by Agentic AI systems. It serves as a critical component of TxAgent, providing access to a vast array of biomedical knowledge from trusted sources including:

- FDA Drug Label data for all US FDA-approved drugs since 1939
- OpenTargets for target-disease associations and drug mechanisms
- Monarch Initiative for phenotype-disease relationships

The library provides a consistent interface for querying these diverse data sources, allowing AI systems to seamlessly access biomedical information without needing to understand the complexities of each individual API.

## Core Architecture

ToolUniverse follows a hierarchical class structure that allows for code reuse while accommodating the specific requirements of different API types:

```
BaseTool
   ├── GraphQLTool
   │      ├── OpentargetTool
   │      ├── OpentargetGeneticsTool
   │      └── OpentargetToolDrugNameMatch
   │
   ├── RESTfulTool (extends GraphQLTool)
   │      ├── MonarchTool
   │      └── MonarchDiseasesForMultiplePhenoTool
   │
   └── FDATool
          ├── FDADrugLabelTool
          ├── FDADrugLabelSearchTool
          ├── FDADrugLabelSearchIDTool
          └── FDADrugLabelGetDrugGenericNameTool
```

### Key Components

1. **ToolUniverse**: The main class that loads, manages, and executes tools. It serves as the primary entry point for interacting with the library.

2. **BaseTool**: The abstract base class for all tools, defining the common interface.

3. **GraphQLTool**: Extends BaseTool with functionality specific to GraphQL APIs, including query validation and execution.

4. **RESTfulTool**: Extends GraphQLTool (reusing some of its functionality) to provide REST API specific implementations.

5. **FDATool**: Extends BaseTool with functionality specific to FDA's OpenFDA APIs.

## API Integration Approach

ToolUniverse wraps external APIs using a consistent pattern:

1. **Configuration-Based Tool Definition**: Each tool is defined by a JSON configuration that specifies its name, description, parameters, and API-specific details.

2. **Type-Specific Handler Classes**: Different API types (GraphQL, REST, etc.) are handled by specialized classes that know how to properly format requests and parse responses.

3. **Unified Interface**: All tools expose a consistent `run` method that takes standardized arguments and returns results in a consistent format.

4. **Error Handling**: API-specific errors are caught and translated into a consistent format for the calling application.

5. **Caching**: Tools that have been instantiated are cached to improve performance when they are called again.

## Data Sources

### 1. FDA Drug Label Data

**Endpoint**: `https://api.fda.gov/drug/label.json`

**Description**: Provides comprehensive information about FDA-approved drug products, including indications, contraindications, adverse reactions, and more.

**Data Coverage**: All US FDA-approved drugs since 1939, with detailed information from their official drug labels.

**Example Tools**:
- `get_drug_names_by_abuse_info`: Retrieve drug names based on abuse information
- `get_abuse_info_by_drug_name`: Retrieve abuse information for a specific drug
- `get_warnings_by_drug_name`: Retrieve warning information for a specific drug

**API Approach**: Uses REST API queries with field filtering and full-text search capabilities. The FDA API is wrapped with specialized handling for extracting nested fields and filtering results based on keywords.

### 2. OpenTargets Platform

**Endpoint**: `https://api.platform.opentargets.org/api/v4/graphql`

**Description**: Provides evidence-based information on the associations between targets (genes/proteins) and diseases, as well as information about drugs that modulate these targets.

**Data Coverage**: Comprehensive database of target-disease associations with supporting evidence types and data on drugs that interact with these targets.

**Example Tools**:
- `get_associated_targets_by_disease_efoId`: Find targets associated with a specific disease
- `get_associated_diseases_phenotypes_by_target_ensemblID`: Find diseases associated with a specific target
- `get_drug_indications_by_chemblId`: Fetch indications for a given drug

**API Approach**: Uses GraphQL for efficient, precise data retrieval. ToolUniverse implements query validation against the schema and handles the complexities of GraphQL query construction.

### 3. Monarch Initiative

**Endpoint**: `https://api.monarchinitiative.org/v3/api`

**Description**: Provides phenotype-disease associations, allowing for cross-species comparison and integration of model organism data with human disease data.

**Data Coverage**: Extensive phenotype and disease ontologies with relationships between phenotypic features and diseases across species.

**Example Tools**:
- `get_joint_associated_diseases_by_HPO_ID_list`: Retrieve diseases associated with a list of phenotypes
- `get_phenotype_by_HPO_ID`: Retrieve a phenotype by its HPO ID
- `get_HPO_ID_by_phenotype`: Retrieve the HPO ID of a phenotype

**API Approach**: Uses a RESTful API with various endpoints for different types of queries. ToolUniverse provides specialized tools for common query patterns.

## Tool Management

Tools are defined in JSON files located in the `data` directory:
- `opentarget_tools.json`
- `fda_drug_labeling_tools.json`
- `special_tools.json`
- `monarch_tools.json`

These files are loaded by the `ToolUniverse` class when it is initialized, making all defined tools available for use.

## Command Line Interface

ToolUniverse includes a CLI tool (`tooluniverse_cli.py`) that provides easy access to the library's functionality:

- **list**: View all available tools, with options to filter by category and control output format
- **search**: Find tools matching specific criteria in their name or description
- **call**: Execute a specific tool with provided arguments
- **info**: Get detailed information about a specific tool

The CLI categorizes tools into three main categories:
- **FDA Drug Label Tools**: Tools for accessing FDA drug label data
- **OpenTarget Tools**: Tools for accessing target, disease, and drug relationship data
- **Monarch Tools**: Tools for accessing phenotype and disease ontology data

## Function Call Execution Flow

When a tool is called:

1. The `run` method of the `ToolUniverse` class is called with a function call specification.
2. The specification is parsed and validated against the tool's defined parameters.
3. If the tool hasn't been instantiated before, an appropriate instance is created based on the tool type.
4. The tool's `run` method is called with the provided arguments.
5. The tool makes the appropriate API call, processes the response, and returns it in a standardized format.

## Advanced Features

1. **Tool Categories**: Tools are organized into categories based on their data source and purpose, making it easier to discover relevant tools.

2. **Case-Insensitive Search**: The CLI supports case-insensitive search and filtering for better usability.

3. **Nested JSON Output**: Output can be formatted as nested JSON objects for more structured data representation.

4. **Verbose Control**: Users can control the verbosity of output, showing or hiding details about the tool loading process.

5. **Cross-API Tool Integration**: Some tools, like `OpentargetToolDrugNameMatch`, integrate with other tools (like `FDADrugLabelGetDrugGenericNameTool`) to provide enhanced functionality.

## Conclusion

ToolUniverse provides a powerful abstraction layer over multiple biomedical APIs, making it easier for AI systems to access and utilize biomedical data from various trusted sources. Its well-structured architecture allows for easy extension with new data sources and tools in the future.
