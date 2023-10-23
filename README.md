# Pishoe Chatbot Solution

Pishoe is a chatbot solution developed by a team of four students. It utilizes HTML, CSS, JavaScript, SASS, FastAPI, and the RASA framework to provide an interactive and conversational user experience.

## Author Team

- Nguyễn Mạnh Duy (duym171003@gmail.com)
- Vũ Tuấn Nam (vutuannam39@gmail.com)
- Đào Xuân Trí (TriDX.B21CN721@stu.ptit.edu.vn)
- Cù Xuân Hoà (cuhoa36@gmail.com)

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with Pishoe, you'll need to install the required dependencies. You can do this using pip and the `requirements.txt` file provided:

```bash
pip install -r requirements.txt
```

## Getting Started

Before running the chatbot, ensure you have completed the installation step. Once the dependencies are installed, you can follow these steps to start the chatbot:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/ddev17/Pishoe
   ```

2. Change directory to the project folder:

   ```bash
   cd Pishoe
   ```

3. Start the FastAPI server:

   ```bash
   python main.py
   ```

4. Run the RASA framework:

   ```bash
   rasa run -m models --enable-api --cors "*"
   rasa run actions
   ```

Now, Pishoe is up and running, and you can interact with the chatbot via a web interface.

## Project Structure

The project structure is organized as follows:
- **models**: RASA NLU and Core models.
- **main.py**: The FastAPI application.
- **config.yml**: Configuration file for RASA.
- **requirements.txt**: List of project dependencies.
- **README.md**: This documentation.

## Usage

Describe how users can interact with Pishoe and any additional information on the chatbot's features or functionality.

## Contributing

We welcome contributions to Pishoe! To contribute to the project, follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

Please follow the project's code of conduct and contribution guidelines, if any.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this project as long as you adhere to the terms of the license.
