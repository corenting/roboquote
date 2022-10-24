# roboquote

Generate random "inspirational" quotes pictures by using the [BLOOM language model](https://huggingface.co/bigscience/bloom) through the Hugging Face Inference API.

## Examples

<img src="https://github.com/corenting/roboquote/raw/master/doc/examples/1.jpg" width="500">
<img src="https://github.com/corenting/roboquote/raw/master/doc/examples/2.jpg" width="500">
<img src="https://github.com/corenting/roboquote/raw/master/doc/examples/3.jpg" width="500">

## How it works

1. A background is picked from [Unsplash](unsplash.com), either randomly or by giving roboquote a search query.
2. The model is prompted to give an "inspirational" quote for the given background search query.
3. The quote is inserted on the picture which is then saved.

## Usage

1. Install the project with [poetry](https://python-poetry.org/) by doing `poetry install`.
2. Set an environment variable `HUGGING_FACE_API_TOKEN` with your Hugging Face Inference API token. The project uses [environs](https://github.com/sloria/environs) so you can also put the variable in a [env file](https://github.com/sloria/environs#reading-env-files).
3. Run `poetry run python main.py my_file.jpg` to generate a new random picture.

See `poetry run python main.py --help` for the available options.

## Credits

- [atomicparade](https://github.com/atomicparade) for the [code used to do the text auto wrapping](https://github.com/atomicparade/pil_autowrap/blob/main/pil_autowrap/pil_autowrap.py)
- [BigScience Workshop](https://huggingface.co/bigscience/) for the bloom model used
- [Hugging Face](https://huggingface.co/) for the inference API
- [Unsplash](unsplash.com)] for the background pictures.
