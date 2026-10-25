// ===============================
// PDF UPLOAD
// ===============================

const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const message = document.getElementById("message");

const askButton = document.getElementById("askButton");
const questionInput = document.getElementById("questionInput");


form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const file = fileInput.files[0];

    if (!file) {
        message.innerText = "Please select a PDF";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);


    try {

        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Upload failed");
        }

        // Show upload success message
        message.innerText = result.message;

        // Change textarea placeholder
        questionInput.placeholder = "Ask your question...";

    }
    catch (error) {

        message.innerText = "Upload failed: " + error.message;

    }
});


// ===============================
// ASK QUESTION
// ===============================

const answerDiv = document.getElementById("answer");
const sourcesDiv = document.getElementById("sources");


askButton.addEventListener("click", async function () {

    const question = questionInput.value.trim();

    if (!question) {
        answerDiv.innerText = "Please enter a question.";
        return;
    }

    answerDiv.innerText = "Generating answer...";
    sourcesDiv.innerHTML = "";

    try {

        const response = await fetch("http://127.0.0.1:8000/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Something went wrong");
        }

        // Display answer
        answerDiv.innerText = "Answer : " + result.answer;


        // Display sources
        sourcesDiv.innerHTML = "<h3>Sources (from the PDF provided)</h3>";

        result.sources.forEach((source, index) => {

            const sourceElement = document.createElement("p");

            sourceElement.innerText =
                "Source " + (index + 1) + ": " + source;

            sourcesDiv.appendChild(sourceElement);
        });

    }
    catch (error) {

        answerDiv.innerText = "Error: " + error.message;

    }
});

// ===============================
// Upload Status
// ===============================

const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");

uploadBtn.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select a PDF file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    uploadStatus.textContent = "Uploading...";

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            uploadStatus.textContent =
                `${result.message} !`;
        } else {
            uploadStatus.textContent =
                `Upload failed: ${result.detail}`;
        }

    } catch (error) {
        uploadStatus.textContent =
            "Upload failed: " + error.message;
    }
});