# Case Crafter
## Project Description
Case Crafter is an AI tool designed to automate the creation of therapy case notes, saving therapists time and ensuring consistency. After sessions, therapists upload audio recordings, which are transcribed using speech-to-text technology, capturing all key details without manual effort. The platform also includes sentiment analysis to assess emotional tones, offering insights into client progress.

## Installation
1. Clone the repository: `git clone https://github.com/sanchloe/case-crafter.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file.

## Usage
To start the application, run:
```bash
uvicorn src.main:app --reload
```
Access the API at: http://localhost:8000/.

## Features
1. Speech to text
2. Accurate content generation using Llama model
3. Integration with a database for efficient task management

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.