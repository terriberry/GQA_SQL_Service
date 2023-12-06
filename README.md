# GQA_SQL_Service

## Installation

Install the LangChain CLI if you haven't yet

```bash
pip install -U langchain-cli
```

## Adding packages

```bash
# adding packages from 
# https://github.com/langchain-ai/langchain/tree/master/templates
langchain app add $PROJECT_NAME

# adding custom GitHub repo packages
langchain app add --repo $OWNER/$REPO
# or with whole git string (supports other git providers):
# langchain app add git+https://github.com/hwchase17/chain-of-verification

# with a custom api mount point (defaults to `/{package_name}`)
langchain app add $PROJECT_NAME --api_path=/my/custom/path/rag
```

Note: you remove packages by their api path

```bash
langchain app remove my/custom/path/rag
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
LangSmith is currently in private beta, you can sign up [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Launch LangServe

```bash
langchain serve
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t my-langserve-app
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 my-langserve-app
```

## Creating a new AI Service package
[Here](https://github.com/langchain-ai/langchain/blob/master/templates/README.md) is a link that explains how to create a Langchain package.

The Langchain package has no functionality as of yet. The functionality can be added by adding a package inside the `/packages` folder.

This can be done using Poetry. Poetry is a dependency managment and packaging tool for Python. We will use Poetry to create a Python package of the AI service. [Here](https://python-poetry.org/docs/) is the official doc from Poetry.


Head into the `/packages` folder and run the following command to create a new Poetry package:

```shell
poetry new <package_name>
```

Add the following dependencies into the `pyproject.toml` file inside the created package. The `pyproject.toml` is used to tell the host that is running the package to install the packages listed inside:

```shell
[tool.poetry.group.dev.dependencies]
langchain-cli = ">=0.0.15"
fastapi = "^0.104.0"
sse-starlette = "^1.6.5"

[tool.langserve]
export_module = "<name of package>.chain"
export_attr = "chain"
```

Add the dependency for the newly created package inside the `pyproject.toml` of the main service package:

```shell
<name of package> = {path = "packages\\<name of package>", develop = true}
```

Import the chain package into the `server.py`:

```shell
from <package_name>.chain import chain as <choose a name>

add_routes(app, <chosen name>, path="\<endpoint name>")
```