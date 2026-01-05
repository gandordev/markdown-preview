// TODO: Convert alerts to pop-ups
var filesToConvert = []


// Input / Drag
const fileInput = document.getElementById("file-input");
fileInput.addEventListener("change", (e) => {
    displayImages(e.target.files);
});

window.addEventListener("dragover", (e) => {
    const fileItems = [...e.dataTransfer.items].filter(
        (item) => item.kind === "file",
    );
    if (fileItems.length > 0) {
        e.preventDefault();

        if (!dropZone.contains(e.target)) {
            e.dataTransfer.dropEffect = "none";
        }
    }
});


// Display images
const preview = document.getElementById("preview");

function displayImages(files) {
    for (const file of files) {
        const li = document.createElement("li");

        if (file.type.startsWith("image/")) {
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.alt = file.name;
            li.appendChild(img);
        }

        li.appendChild(document.createTextNode(file.name));
        preview.appendChild(li);

        filesToConvert.push(file);
    }
}


// Drop / Drag
window.addEventListener("drop", (e) => {
    if ([...e.dataTransfer.items].some((item) => item.kind === "file")) {
        e.preventDefault();
    }
});

const dropZone = document.getElementById("drop-zone");
dropZone.addEventListener("drop", (ev) => {
    ev.preventDefault();
    const files = [...ev.dataTransfer.items]
        .map((item) => item.getAsFile())
        .filter((file) => file);
    displayImages(files);
});
dropZone.addEventListener("dragover", (e) => {
    const fileItems = [...e.dataTransfer.items].filter(
        (item) => item.kind === "file",
    );
    if (fileItems.length > 0) {
        e.preventDefault();
        e.dataTransfer.dropEffect = "copy";
    }
});


// Clear
const clearBtn = document.getElementById("clear-btn");
clearBtn.addEventListener("click", () => {
   deleteFiles();
});

function deleteFiles() {
    for (const img of preview.querySelectorAll("img")) {
        URL.revokeObjectURL(img.src);
    }
    preview.textContent = "";
    filesToConvert = [];
}

// Converter
const sendBtn = document.getElementById("convert-md")
sendBtn.addEventListener("click", () => {
    if (filesToConvert.length <= 0) {
        confirm("Debes incluir al menos un archivo para convertir");
    }

    // Save files as formData
    const formData = new FormData();
    for (const file of filesToConvert) {
        formData.append('files', file);
    }

    // Transform
    convertFiles(formData);

});

async function convertFiles(formData) {
    try {
        // Convert
        const response = await fetch("api/convert", {
            method: "POST",
            body: formData
        });
        const markdowns = await response.json();

        // Check if all files where converted successfully
        if (markdowns["converted"].length === filesToConvert.length) {
            alert("Archivos convertidos correctamente");
        }
        else {
            alert("Algún archivo ha fallado al convertirse");
        }

        // Delete files from queue
        deleteFiles();
    } catch (error) {
        confirm(`Error al convertir el archivo: ${error}`);
    }
}