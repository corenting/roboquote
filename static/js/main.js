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

function setStopLoading(isError) {
    // Enable submit button
    const submitButtonElement = document.getElementById("form-submit");
    submitButtonElement.disabled = true;

    // Hide loading div
    const loadingDivElement = document.getElementById("loading");
    loadingDivElement.style.display = "none";

    // Handle error div
    const errorDivElement = document.getElementById("error");
    errorDivElement.style.display = isError ? "block" : "none";

    if (!isError) {
        // Show result div
        const resultDivElement = document.getElementById("result");
        resultDivElement.style.display = "block";
    }
}

htmx.on("htmx:beforeRequest", function (evt) {

    const path = evt.detail.requestConfig.path;
    // We only want to intercept calls to /generate
    if (path != "/generate/") {
        return
    }

    evt.preventDefault();

    // Build URL for picture
    const searchParams = new URLSearchParams(evt.detail.requestConfig.parameters);
    const url = path + "?" + searchParams;

    // Set picture URL
    setStartLoading();
    const pictureResultElement = document.getElementById("result-image");
    pictureResultElement.src = url;

    pictureResultElement.addEventListener('load', function () {
        setStopLoading(isError = false)
    });
    pictureResultElement.addEventListener('error', function () {
        setStopLoading(isError = true)
    });
});
