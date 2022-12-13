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

	// Build URL for image
	const queryParams = {};
	if (background) {
		queryParams["background"] = background;
	}
	var url = "/generate/";
	if (queryParams.length > 0) {
		const searchParams = new URLSearchParams(queryParams);
		url += `?${searchParams}`;
	}

	// Fetch image
	fetch(url)
		.then((response) => {
			if (response.ok) {
				response.blob().then((myBlob) => {
					setStopLoading(false);
					var objectURL = URL.createObjectURL(myBlob);
					pictureResultElement.src = objectURL;
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
	const background = formParameters["background"]
		? formParameters["background"]
		: null;

	try {
		handleGeneration(background);
	} catch (error) {
		console.log("Error during generation", error);
	}

	return false;
}
