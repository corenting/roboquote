# roboquote

Generate random "inspirational" quotes images by using an AI text generation model through the Hugging Face Inference API.

The following models can be used:
- [bigscience/bloom](https://huggingface.co/bigscience/bloom)
- [mistralai/Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)

## Examples

<img src="https://github.com/corenting/roboquote/raw/master/doc/examples/1.jpg" width="500">
<img src="https://github.com/corenting/roboquote/raw/master/doc/examples/2.jpg" width="500">
<img src="https://github.com/corenting/roboquote/raw/master/doc/examples/3.jpg" width="500">

## How it works

1. A background is picked from [Unsplash](unsplash.com), either randomly or by giving roboquote a search query.
2. The model is prompted to give an "inspirational" quote for the given background search query.
3. The quote is inserted on the image which is then saved.

## Usage

### Installation
1. Install the project with [poetry](https://python-poetry.org/) by doing `poetry install`.
2. Set environment variables for configuration (the project uses [environs](https://github.com/sloria/environs) so you can also put the variable in a [env file](https://github.com/sloria/environs#reading-env-files)):
    - `HUGGING_FACE_API_TOKEN` (**required**): your Hugging Face Inference API token.
    - `LOG_LEVEL` (optional, default is `WARNING`): log level of the application
    - `WEB_DEBUG` (optional, default is `False`): if you want to run the web app in debug mode (should not be required)
    - `HIDE_HUGGING

### CLI usage

Run `poetry run python main.py my_file.jpg` to generate a new random image.

See `poetry run python main.py --help` for the available options.

### Web usage

The web version is a [Starlette](https://pypi.org/project/starlette/) application (`roboquote.web.app:app`).

It can be launched quickly locally with [uvicorn](https://pypi.org/project/uvicorn/) through the `make run-web` command.

## Credits

- [atomicparade](https://github.com/atomicparade) for the [code used to do the text auto wrapping](https://github.com/atomicparade/pil_autowrap/blob/main/pil_autowrap/pil_autowrap.py)
- [BigScience Workshop](https://huggingface.co/bigscience/) for the BLOOM model used
- [Hugging Face](https://huggingface.co/) for the inference API
- [Mistral AI](https://mistral.ai/) for the Mistral-7B-Instruct-v0.1 model used
- [Unsplash](unsplash.com) for the background images.
