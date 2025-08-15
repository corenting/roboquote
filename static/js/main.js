function setStartLoading() {
	const submitButtonElement = document.getElementById("form-submit");
	submitButtonElement.disabled = true;

	// Show loading div
	const loadingDivElement = document.getElementById("loading");
	loadingDivElement.style.display = "block";

	// Hide result div
	const resultDivElement = document.getElementById("result");
	resultDivElement.style.display = "none";

	// Hide error div
	const errorDivElement = document.getElementById("error");
	errorDivElement.style.display = "none";
}

function setStopLoading(isError, errorMsg = "Unknown error 😢") {
	// Enable submit button
	const submitButtonElement = document.getElementById("form-submit");
	submitButtonElement.disabled = false;

	// Hide loading div
	const loadingDivElement = document.getElementById("loading");
	loadingDivElement.style.display = "none";

	// Handle error div
	const errorDivElement = document.getElementById("error");
	const errorDetailsElement = document.getElementById("error-details");
	errorDivElement.style.display = isError ? "block" : "none";
	errorDetailsElement.innerText = errorMsg;

	// Result div
	const resultDivElement = document.getElementById("result");
	resultDivElement.style.display = isError ? "none" : "block";
}

function onGenerateError(error) {
	setStopLoading(true, error);
}

function handleGeneration(background, text_model, quote_language, blur) {
	setStartLoading();

	// Get HTML elements
	const pictureResultElement = document.getElementById("result-image");
	const captionResultElement = document.getElementById("result-caption");

	// Build query params
	const queryParams = {};
	if (background) {
		queryParams.background = background;
	}
	if (text_model) {
		queryParams.text_model = text_model;
	}
	if (quote_language) {
		queryParams.quote_language = quote_language;
	}
	if (blur) {
		queryParams.blur = blur;
	}

	// Build URL
	let url = "/generate/";
	if (Object.keys(queryParams).length > 0) {
		const searchParams = new URLSearchParams(queryParams);
		url += `?${searchParams}`;
	}

	// Fetch image
	fetch(url)
		.then((response) => {
			if (response.ok) {
				response.blob().then((myBlob) => {
					setStopLoading(false);
					const objectURL = URL.createObjectURL(myBlob);
					pictureResultElement.src = objectURL;

					// Picture credits
					const pictureCredits = JSON.parse(
						response.headers.get("x-image-credits"),
					);

					// Generation information
					const generationInfo = JSON.parse(
						response.headers.get("x-generation-parameters"),
					);

					// Build name
					let name = "";
					if (pictureCredits.first_name != null) {
						name = pictureCredits.first_name;
					}
					if (pictureCredits.last_name != null) {
						name += ` ${pictureCredits.first_name}`;
					}

					captionResultElement.innerHTML = `Background picture by <a href='${pictureCredits.url}'>${name} on Unsplash</a>.<br />
					Generated with ${generationInfo.model_used} on ${generationInfo.api_used}.
					`;
				});
			} else {
				response
					.json()
					.then((json) => {
						onGenerateError(json.error);
					})
					.catch((_) => {
						onGenerateError("Unknown error");
					});
			}
		})
		.catch(() => {
			onGenerateError("Unknown error");
		});
}

// biome-ignore lint/correctness/noUnusedVariables: used in template
function onGenerateClick(evt) {
	evt.preventDefault();

	// Get parameters
	const formParameters = Object.fromEntries(new FormData(evt.target));
	const background = formParameters.background;
	const textModel = formParameters.text_model;
	const quoteLanguage = formParameters.quote_language;
	const blur = formParameters.blur;

	try {
		handleGeneration(background, textModel, quoteLanguage, blur);
	} catch (error) {
		console.log("Error during generation", error);
	}

	return false;
}
