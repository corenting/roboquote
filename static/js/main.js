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

function handleGeneration(background) {
	setStartLoading();

	// Get HTML elements
	const pictureResultElement = document.getElementById("result-image");
	const captionResultElement = document.getElementById("result-caption");

	// Build URL for image
	const queryParams = {};
	if (background) {
		queryParams["background"] = background;
	}
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

					// Credits
					const pictureCredits = JSON.parse(
						response.headers.get("x-image-credits"),
					);
					console.log(pictureCredits);
					captionResultElement.innerHTML = `Background picture by <a href='${pictureCredits.url}'>${pictureCredits.first_name} ${pictureCredits.last_name} on Unsplash</a>.`;
				});
			} else {
				response.json().then((json) => {
					onGenerateError(json["error"]);
				});
			}
		})
		.catch(() => {
			onGenerateError("Unknown error");
		});
}

function onGenerateClick(evt) {
	evt.preventDefault();

	// Get parameters
	const formParameters = Object.fromEntries(new FormData(evt.target));
	const background = formParameters["background"] || null;

	try {
		handleGeneration(background);
	} catch (error) {
		console.log("Error during generation", error);
	}

	return false;
}
