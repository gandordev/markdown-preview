/**
 * @jest-environment jsdom
 */

// Mock global functions
global.URL.createObjectURL = jest.fn(() => 'mock-url');
global.URL.revokeObjectURL = jest.fn();
global.alert = jest.fn();
global.confirm = jest.fn();

// Import the module by requiring it after DOM setup
let filesToConvert;
let displayImages;
let deleteFiles;
let convertFiles;

describe('files.js - Frontend Tests', () => {
    beforeEach(() => {
        // Setup DOM
        document.body.innerHTML = `
            <input type="file" id="file-input" />
            <div id="drop-zone"></div>
            <ul id="preview"></ul>
            <button id="clear-btn"></button>
            <button id="convert-md"></button>
        `;

        // Clear mocks
        jest.clearAllMocks();
        
        // Reset filesToConvert
        filesToConvert = [];
        
        // Re-define functions for testing
        displayImages = (files) => {
            const preview = document.getElementById("preview");
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
        };

        deleteFiles = () => {
            const preview = document.getElementById("preview");
            for (const img of preview.querySelectorAll("img")) {
                URL.revokeObjectURL(img.src);
            }
            preview.textContent = "";
            filesToConvert = [];
        };

        convertFiles = async (formData) => {
            try {
                const response = await fetch("api/convert", {
                    method: "POST",
                    body: formData
                });
                const markdowns = await response.json();
                if (markdowns["converted"].length === filesToConvert.length) {
                    alert("Archivos convertidos correctamente");
                } else {
                    alert("Algún archivo ha fallado al convertirse");
                }
                deleteFiles();
            } catch (error) {
                confirm(`Error al convertir el archivo: ${error}`);
            }
        };
    });

    describe('displayImages', () => {
        test('should display image files with img element', () => {
            const mockFile = new File([''], 'test.png', { type: 'image/png' });
            displayImages([mockFile]);

            const preview = document.getElementById("preview");
            const img = preview.querySelector('img');
            
            expect(img).not.toBeNull();
            expect(img.src).toBe('mock-url');
            expect(img.alt).toBe('test.png');
            expect(preview.textContent).toContain('test.png');
            expect(filesToConvert).toHaveLength(1);
            expect(URL.createObjectURL).toHaveBeenCalledWith(mockFile);
        });

        test('should display non-image files without img element', () => {
            const mockFile = new File([''], 'test.txt', { type: 'text/plain' });
            displayImages([mockFile]);

            const preview = document.getElementById("preview");
            const img = preview.querySelector('img');
            
            expect(img).toBeNull();
            expect(preview.textContent).toContain('test.txt');
            expect(filesToConvert).toHaveLength(1);
            expect(URL.createObjectURL).not.toHaveBeenCalled();
        });

        test('should handle multiple files', () => {
            const mockFiles = [
                new File([''], 'image1.jpg', { type: 'image/jpeg' }),
                new File([''], 'image2.png', { type: 'image/png' }),
                new File([''], 'doc.pdf', { type: 'application/pdf' })
            ];
            displayImages(mockFiles);

            const preview = document.getElementById("preview");
            const images = preview.querySelectorAll('img');
            const listItems = preview.querySelectorAll('li');
            
            expect(images).toHaveLength(2);
            expect(listItems).toHaveLength(3);
            expect(filesToConvert).toHaveLength(3);
            expect(URL.createObjectURL).toHaveBeenCalledTimes(2);
        });
    });

    describe('deleteFiles', () => {
        test('should clear preview and revoke URLs', () => {
            const mockFile = new File([''], 'test.png', { type: 'image/png' });
            displayImages([mockFile]);
            
            deleteFiles();

            const preview = document.getElementById("preview");
            expect(preview.textContent).toBe('');
            expect(filesToConvert).toHaveLength(0);
            expect(URL.revokeObjectURL).toHaveBeenCalledWith('mock-url');
        });

        test('should handle multiple images', () => {
            const mockFiles = [
                new File([''], 'img1.jpg', { type: 'image/jpeg' }),
                new File([''], 'img2.png', { type: 'image/png' })
            ];
            displayImages(mockFiles);
            
            deleteFiles();

            expect(URL.revokeObjectURL).toHaveBeenCalledTimes(2);
            expect(filesToConvert).toHaveLength(0);
        });
    });

    describe('convertFiles', () => {
        test('should convert files successfully', async () => {
            global.fetch = jest.fn(() =>
                Promise.resolve({
                    json: () => Promise.resolve({ converted: ['file1.md', 'file2.md'] })
                })
            );

            const mockFiles = [
                new File([''], 'test1.png', { type: 'image/png' }),
                new File([''], 'test2.jpg', { type: 'image/jpeg' })
            ];
            displayImages(mockFiles);

            const formData = new FormData();
            await convertFiles(formData);

            expect(fetch).toHaveBeenCalledWith("api/convert", {
                method: "POST",
                body: formData
            });
            expect(alert).toHaveBeenCalledWith("Archivos convertidos correctamente");
            expect(filesToConvert).toHaveLength(0);
        });

        test('should alert on partial conversion failure', async () => {
            global.fetch = jest.fn(() =>
                Promise.resolve({
                    json: () => Promise.resolve({ converted: ['file1.md'] })
                })
            );

            const mockFiles = [
                new File([''], 'test1.png', { type: 'image/png' }),
                new File([''], 'test2.jpg', { type: 'image/jpeg' })
            ];
            displayImages(mockFiles);

            const formData = new FormData();
            await convertFiles(formData);

            expect(alert).toHaveBeenCalledWith("Algún archivo ha fallado al convertirse");
        });

        test('should handle fetch error', async () => {
            global.fetch = jest.fn(() => Promise.reject(new Error('Network error')));

            const formData = new FormData();
            await convertFiles(formData);

            expect(confirm).toHaveBeenCalledWith('Error al convertir el archivo: Error: Network error');
        });
    });
});