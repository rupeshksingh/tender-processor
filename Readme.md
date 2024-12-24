# Tender Document Processor

An intelligent document processing system that automates the completion of tender questionnaires using advanced language models and document processing techniques.

## 🚀 Features

- **Smart Document Processing**: Automatically processes tender questionnaires and generates appropriate responses

- **Excel Integration**: Seamlessly handles Excel-based tender documents while preserving original formatting

- **LLM Integration**: Leverages OpenAI's GPT models for generating context-aware responses

- **User-Friendly Interface**: Interactive Streamlit-based web interface for easy document processing

- **File Management**: Creates working copies of documents to preserve originals

- **Progress Tracking**: Step-by-step process tracking with ability to reset at any point

## 📋 Prerequisites

- Python 3.9+

- OpenAI API key

- Sufficient disk space for document processing

## 🛠️ Installation

1\. Clone the repository:

```bash

git clone https://github.com/rupeshksingh/tender-processor.git

cd tender-processor

```

2\. Create and activate a virtual environment:

```bash

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3\. Install required packages:

```bash

pip install -r requirements.txt

```

4\. Create a `.env` file in the project root:

```env

OPENAI_API_KEY=your_api_key_here

```

## 🏃‍♂️ Running the Application

1\. Start the Streamlit application:

```bash

streamlit run app.py

```

2\. Access the application in your web browser at `http://localhost:8501`

## 📁 Project Structure

```

tender-processor/

├── app.py              # Main Streamlit application

├── excel.py            # Excel processing utilities

├── config.py           # Configuration and settings

├── models.py           # Pydantic models and data structures

├── processors.py       # Core processing logic

├── requirements.txt    # Project dependencies

├── .env               # Environment variables (create this)

└── README.md          # This file

```

## 💻 Usage Guide

1\. **Upload Document**

   - Upload your Excel-based tender document

   - System creates a working copy for processing

2\. **Select Sheets**

   - Choose the instruction sheet containing processing guidelines

   - Select the content sheet containing questions

3\. **Review & Configure**

   - Review extracted questions

   - Configure answer column settings

   - Set starting row for answers

4\. **Process & Download**

   - Review generated answers

   - Save changes to document

   - Download processed document

## 🔧 Configuration

Key configuration options in `config.py`:

```python

OPENAI_API_KEY: str    # Your OpenAI API key

MODEL_NAME: str        # GPT model to use

TEMPERATURE: float     # Response creativity (0.0-1.0)

```

## 🧪 Testing

Run the test suite:

```bash

python -m pytest tests/

```

## 🤝 Contributing

1\. Fork the repository

2\. Create a feature branch (`git checkout -b feature/AmazingFeature`)

3\. Commit changes (`git commit -m 'Add AmazingFeature'`)

4\. Push to branch (`git push origin feature/AmazingFeature`)

5\. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Current Limitations

- **Excel Format**: Currently optimized for a specific tender format with the following structure:

  - Content sheet containing questions with columns:

    - System Id

    - Type

    - Description

    - Answer Type

    - Response Required

  - Instruction sheet containing processing guidelines

- **Language Model**: Requires OpenAI API access

- **File Size**: Optimized for documents up to 10MB

- **Question Types**: Currently handles single-line text, multi-line text, and choice-based questions

## 🔜 Future Enhancements

- Support for additional tender document formats

- Integration with alternative language models

- Batch processing capabilities

- Custom answer templates

- Response validation framework

## 👥 Support

For support, please open an issue in the GitHub repository or contact the maintenance team.

---

Built with ❤️ by Rupesh