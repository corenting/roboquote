# roboquote

Generate random "inspirational" quotes images by using an AI text generation model.

The following models can be used:
- [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) through [GroqCloud API](https://console.groq.com/playground)
- [deepseek-ai/DeepSeek-R1-Distill-Llama-70B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B) through [GroqCloud API](https://console.groq.com/playground)
- [meta-llama/Llama-3.3-70B](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md) through [GroqCloud API](https://console.groq.com/playground)

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
    - `GROQ_CLOUD_API_KEY` (**required**): your GroqCloud API key for their API
    - `LOG_LEVEL` (optional, default is `WARNING`): log level of the application
    - `WEB_DEBUG` (optional, default is `False`): if you want to run the web app in debug mode (should not be required)

### CLI usage

Run `poetry run python main.py my_file.jpg` to generate a new random image.

See `poetry run python main.py --help` for the available options.

### Web usage

The web version is a [Starlette](https://pypi.org/project/starlette/) application (`roboquote.web.app:app`).

It can be launched quickly locally with [uvicorn](https://pypi.org/project/uvicorn/) through the `make run-web` command.

## Credits

- [atomicparade](https://github.com/atomicparade) for the [code used to do the text auto wrapping](https://github.com/atomicparade/pil_autowrap/blob/main/pil_autowrap/pil_autowrap.py)
- [Google Fonts](https://fonts.google.com/) for the fonts used in the pictures
- [Unsplash](unsplash.com) for the background images
- The authors and providers of the AI models listed above
