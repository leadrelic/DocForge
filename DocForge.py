import json
import re
import sys
from PyQt6.QtWidgets import (QMainWindow, QTextEdit, QVBoxLayout, QPushButton,
                             QSplitter, QWidget, QListWidget, QInputDialog, QApplication,
                             QComboBox, QLabel, QFileDialog, QToolBar, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class DocHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocForge - Advanced Documentation Helper")
        self.setGeometry(100, 100, 1200, 700)  # Set initial window size
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c2c2c;  /* Dark gray background for the main window */
                color: #ecf0f1;              /* Light text color */
            }
            QTextEdit {
                background-color: #353535;  /* Slightly lighter dark background for text areas */
                color: #ecf0f1;              /* Light text color */
                font-family: Consolas;
                font-size: 14px;
                border: 1px solid #b0b0b0;
                padding: 10px;
            }
            QPushButton {
                background-color: #555555;   /* Dark gray button background */
                color: #ecf0f1;              /* Light text color for better contrast */
                border: none;
                border-radius: 5px;
                padding: 5px;                /* Adjusted padding */
                margin: 2px;                 /* Reduced margin for compactness */
                font-size: 12px;             /* Smaller font size */
            }
            QPushButton:hover {
                background-color: #666666;   /* Lighter gray on hover */
            }
            QComboBox {
                background-color: #444444;   /* Dark gray background */
                color: white;
                padding: 8px;                /* Adjust padding */
                border: none;
                border-radius: 5px;
                font-size: 12px;             /* Smaller font size */
            }
            QListWidget {
                background-color: #353535;    /* Darker background */
                color: #ecf0f1;               /* Light text color */
                border: 1px solid #b0b0b0;
                padding: 5px;
            }
            QLabel {
                font-weight: bold;
                color: #ecf0f1;
            }
        """)

        # Load Snippets
        self.snippets = self.load_snippets()

        # Editor Widgets
        self.editor = QTextEdit(self)
        self.formatted_editor = QTextEdit(self)
        self.formatted_editor.setReadOnly(True)  # Make the formatted editor read-only

        # Snippet List
        self.snippet_list = QListWidget(self)
        self.snippet_list.addItems(self.snippets.keys())
        self.snippet_list.itemDoubleClicked.connect(self.insert_snippet)

        # Toolbar
        self.create_toolbar()

        # Buttons and Format Selection
        self.format_selection = QComboBox(self)
        self.format_selection.addItems(["Markdown", "LaTeX"])

        # Layout for the right panel
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Snippets", self))
        layout.addWidget(self.snippet_list)
        layout.addWidget(QLabel("Output Format", self))
        layout.addWidget(self.format_selection)

        # Add buttons for actions
        self.add_snippet_button = QPushButton("Add Snippet", self)
        self.add_snippet_button.clicked.connect(self.add_snippet)
        layout.addWidget(self.add_snippet_button)

        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.generate_formatted_text)
        layout.addWidget(self.generate_button)

        self.preview_button = QPushButton("Preview", self)
        self.preview_button.clicked.connect(self.preview_document)
        layout.addWidget(self.preview_button)

        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.download_formatted_text)
        layout.addWidget(self.download_button)

        layout.addStretch()  # Push everything to the top

        snippet_widget = QWidget()
        snippet_widget.setLayout(layout)

        # Splitter between the editor and formatted preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.formatted_editor)
        splitter.addWidget(snippet_widget)
        splitter.setSizes([600, 600, 300])

        self.setCentralWidget(splitter)

    def create_toolbar(self):
        toolbar = QToolBar(self)
        toolbar.setStyleSheet("QToolBar { background-color: #2c2c2c; }")  # Dark gray toolbar
        self.addToolBar(toolbar)

        # Add buttons directly instead of using QAction
        edit_button = QPushButton("Edit Snippet")
        edit_button.clicked.connect(self.edit_snippet)
        edit_button.setIcon(QIcon.fromTheme("document-edit"))  # Set an icon
        edit_button.setFixedHeight(30)  # Set a fixed height for buttons
        edit_button.setStyleSheet("color: #ecf0f1;")  # Set text color for visibility
        toolbar.addWidget(edit_button)

        delete_button = QPushButton("Delete Snippet")
        delete_button.clicked.connect(self.delete_snippet)
        delete_button.setIcon(QIcon.fromTheme("edit-delete"))  # Set an icon
        delete_button.setFixedHeight(30)  # Set a fixed height for buttons
        delete_button.setStyleSheet("color: #ecf0f1;")  # Set text color for visibility
        toolbar.addWidget(delete_button)

        toolbar.addSeparator()  # Add a separator

        bold_button = QPushButton("Bold")
        bold_button.clicked.connect(lambda: self.apply_format("bold"))
        bold_button.setIcon(QIcon.fromTheme("format-text-bold"))  # Set an icon
        bold_button.setFixedHeight(30)  # Set a fixed height for buttons
        bold_button.setStyleSheet("color: #ecf0f1;")  # Set text color for visibility
        toolbar.addWidget(bold_button)

        italic_button = QPushButton("Italic")
        italic_button.clicked.connect(lambda: self.apply_format("italic"))
        italic_button.setIcon(QIcon.fromTheme("format-text-italic"))  # Set an icon
        italic_button.setFixedHeight(30)  # Set a fixed height for buttons
        italic_button.setStyleSheet("color: #ecf0f1;")  # Set text color for visibility
        toolbar.addWidget(italic_button)

        underline_button = QPushButton("Underline")
        underline_button.clicked.connect(lambda: self.apply_format("underline"))
        underline_button.setIcon(QIcon.fromTheme("format-text-underline"))  # Set an icon
        underline_button.setFixedHeight(30)  # Set a fixed height for buttons
        underline_button.setStyleSheet("color: #ecf0f1;")  # Set text color for visibility
        toolbar.addWidget(underline_button)

    def load_snippets(self):
        try:
            with open("snippets.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_snippets(self):
        with open("snippets.json", "w") as file:
            json.dump(self.snippets, file, indent=4)

    def add_snippet(self):
        name, ok = QInputDialog.getText(self, "Snippet Name", "Enter the name of the snippet:")
        if ok and name:
            snippet_content, ok = QInputDialog.getMultiLineText(self, "Snippet Content", "Enter the snippet:")
            if ok:
                self.snippets[name] = snippet_content
                self.snippet_list.addItem(name)
                self.save_snippets()

    def edit_snippet(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            name = current_item.text()
            snippet_content = self.snippets[name]
            updated_content, ok = QInputDialog.getMultiLineText(self, "Edit Snippet", "Edit the snippet:", snippet_content)
            if ok:
                self.snippets[name] = updated_content
                current_item.setText(name)  # Update the display name
                self.save_snippets()

    def delete_snippet(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            name = current_item.text()
            confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete the snippet '{name}'?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                del self.snippets[name]
                self.snippet_list.takeItem(self.snippet_list.row(current_item))
                self.save_snippets()

    def insert_snippet(self, item):
        snippet = self.snippets.get(item.text(), "")
        self.editor.insertPlainText(snippet)

    def apply_format(self, format_type):
        """Apply text formatting to the selected text."""
        cursor = self.editor.textCursor()
        if format_type == "bold":
            cursor.insertText(f"**{cursor.selectedText()}**")  # Markdown bold
        elif format_type == "italic":
            cursor.insertText(f"*{cursor.selectedText()}*")  # Markdown italic
        elif format_type == "underline":
            cursor.insertText(f"<u>{cursor.selectedText()}</u>")  # Simple underline HTML tag (for Markdown)

    def format_to_markdown(self, text):
        """Automatically convert plain text to basic Markdown."""
        formatted = text

        # Convert lines with all uppercase words to headers
        lines = formatted.splitlines()
        for i, line in enumerate(lines):
            if line.isupper():
                lines[i] = f"# {line.capitalize()}"  # Convert to a Markdown header
            elif line.startswith("1. ") or line.startswith("2. "):  # Detect ordered lists
                lines[i] = f"{line}"
            elif line.startswith("- ") or line.startswith("* "):  # Detect bullet points
                lines[i] = f"* {line[2:].strip()}"
        formatted = "\n".join(lines)

        # Convert URLs to Markdown links automatically
        formatted = re.sub(r'((http[s]?://)?(www\.)?\S+\.\S+)', r'[\1](http://\1)', formatted)

        # Separate paragraphs with double newlines for Markdown
        formatted = formatted.replace("\n", "\n\n")

        return formatted

    def format_to_latex(self, text):
        """Automatically convert plain text to basic LaTeX."""
        formatted = text

        # Convert lines with all uppercase words to sections
        lines = formatted.splitlines()
        in_list = False
        for i, line in enumerate(lines):
            if line.isupper():
                lines[i] = f"\\section{{{line.capitalize()}}}"
            elif line.startswith("1. ") or line.startswith("2. "):  # Detect ordered lists
                if not in_list:
                    lines[i] = "\\begin{enumerate}\n\\item " + line[3:].strip()
                    in_list = True
                else:
                    lines[i] = "\\item " + line[3:].strip()
            elif line.startswith("- ") or line.startswith("* "):  # Detect bullet points
                if not in_list:
                    lines[i] = "\\begin{itemize}\n\\item " + line[2:].strip()
                    in_list = True
                else:
                    lines[i] = "\\item " + line[2:].strip()
            elif in_list:
                lines[i - 1] += "\n\\end{itemize}" if "* " in line else "\n\\end{enumerate}"
                in_list = False
        formatted = "\n".join(lines)

        # Convert URLs to LaTeX links automatically
        formatted = re.sub(r'((http[s]?://)?(www\.)?\S+\.\S+)', r'\\href{http://\1}{\1}', formatted)

        # Use \newline for line breaks in paragraphs
        formatted = formatted.replace("\n", " \\newline\n")

        return formatted

    def generate_formatted_text(self):
        """Generate formatted text and display it in the formatted editor."""
        text = self.editor.toPlainText()
        format_choice = self.format_selection.currentText()

        if format_choice == "Markdown":
            formatted_text = self.format_to_markdown(text)
        else:  # Assume LaTeX
            formatted_text = self.format_to_latex(text)

        # Display the formatted text in the right editor
        self.formatted_editor.setPlainText(formatted_text)

    def preview_document(self):
        """Preview the document in the selected format."""
        formatted_text = self.formatted_editor.toPlainText()
        format_choice = self.format_selection.currentText()

        # Create a preview window with the formatted text
        preview_window = QMainWindow(self)
        preview_window.setWindowTitle(f"Preview - {format_choice}")
        preview_editor = QTextEdit(preview_window)
        preview_editor.setReadOnly(True)
        preview_editor.setPlainText(formatted_text)
        preview_window.setCentralWidget(preview_editor)
        preview_window.resize(600, 400)
        preview_window.show()

    def download_formatted_text(self):
        """Download the formatted text as a file."""
        formatted_text = self.formatted_editor.toPlainText()
        format_choice = self.format_selection.currentText()

        # Set the default file extension based on format
        extension = "md" if format_choice == "Markdown" else "tex"
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", f"document.{extension}",
                                                     f"Text Files (*.{extension});;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(formatted_text)


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DocHelper()
    window.show()
    sys.exit(app.exec())
