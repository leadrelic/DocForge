# User Guide for DocForge

## Introduction
DocForge is an advanced documentation helper designed to streamline the creation and formatting of text documents in Markdown and LaTeX. It provides a user-friendly interface with features that enhance productivity, such as real-time previews, rich text formatting, and snippet management. This guide will help you navigate the application and utilize its features effectively.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Creating a New Document](#creating-a-new-document)
3. [Using Snippets](#using-snippets)
4. [Formatting Text](#formatting-text)
5. [Previewing Documents](#previewing-documents)
6. [Saving and Downloading](#saving-and-downloading)
7. [Customizing the Application](#customizing-the-application)
8. [Troubleshooting](#troubleshooting)
9. [Contact and Support](#contact-and-support)

## Getting Started
### Installation
1. **Clone the Repository**: Begin by cloning the repository to your local machine:
   ```bash
   git clone https://github.com/leadrelic/DocForge.git
   cd DocForge
   ```

2. **Create a Virtual Environment**: It is recommended to create a virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**: Use the following command to install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

### Launching the Application
- Once the installation is complete, run the application with:
   ```bash
   python DocForge.py
   ```

## Creating a New Document
1. **Text Editor**: Upon launching DocForge, you will be greeted with a text editor on the left side of the window.
2. **Input Your Content**: Start typing your document in the editor. You can enter plain text, lists, and links.
3. **Select Output Format**: Choose between Markdown and LaTeX for your document format from the dropdown menu. This will determine how the text will be formatted and rendered.

## Using Snippets
### Adding Snippets
1. Click the "Add Snippet" button in the toolbar.
2. Enter a name for your snippet in the prompt that appears.
3. Input the content of the snippet in the multi-line text dialog.
4. Click "OK" to save the snippet. It will now appear in the snippet list for future use.

### Editing Snippets
1. Select a snippet from the list by clicking on it.
2. Click the "Edit Snippet" button in the toolbar.
3. Modify the snippet content in the dialog that appears and click "OK" to save changes.

### Deleting Snippets
1. Select a snippet from the list.
2. Click the "Delete Snippet" button in the toolbar.
3. Confirm the deletion in the prompt to remove the snippet from the list.

## Formatting Text
### Rich Text Formatting
- You can apply formatting directly to selected text in the editor:
  - **Bold**: Click the "Bold" button or use Markdown syntax by wrapping text with `**`.
  - **Italic**: Click the "Italic" button or use Markdown syntax by wrapping text with `*`.
  - **Underline**: Click the "Underline" button or use a simple HTML tag like `<u>` for underlining.

### Markdown Formatting
- The following Markdown syntax is supported:
  - Headers: Use `#` for headers (e.g., `# Header 1`, `## Header 2`).
  - Lists: Use `1.` for ordered lists and `-` or `*` for bullet points.
  - Links: Use `[link text](URL)` format for hyperlinks (e.g., `[Google](https://www.google.com)`).

## Previewing Documents
1. Click the "Preview" button to open a new window showing a rendered view of your document based on the selected format (Markdown or LaTeX).
2. As you make changes in the editor, you can refresh the preview window to see the latest version.

## Saving and Downloading
### Downloading Your Document
1. Click the "Download" button to save your formatted document locally.
2. Select the desired file format (Markdown or LaTeX) and choose a location to save the file.
3. The file will be saved with the appropriate extension (.md or .tex) based on your selection.

## Customizing the Application
- While DocForge has a standard look and feel, you can adjust settings like the output format and user preferences as needed. Future versions may include more customizable options.

## Troubleshooting
### Common Issues
- **Application Fails to Start**: Ensure you have Python installed and that all required packages from `requirements.txt` are properly installed.
- **Snippets Not Loading**: Ensure the `snippets.json` file exists in the application directory. It will be created automatically when you add your first snippet.
- **Errors on File Download**: Check your file path permissions to ensure you can save files to the selected directory.

## Contact and Support
For any questions, suggestions, or issues with the application, please reach out to support at leadrelic@gmail.com. Contributions and feedback are always welcome!

