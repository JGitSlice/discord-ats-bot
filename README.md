# Discord ATS Resume Analyzer

A Python-powered Discord bot that analyzes resumes against a Job Description (JD), calculates ATS-style scores, identifies matching and missing skills, and provides suggestions to improve resume alignment.

## Overview

The Discord ATS Resume Analyzer helps users evaluate multiple resumes against a selected job description. It generates a weighted ATS score, provides category-wise breakdowns, highlights skill gaps, and recommends learning resources to help candidates improve their resumes.

The project uses a custom ATS scoring model to simulate key aspects of resume screening. Its scores are intended as guidance and do not represent the scoring system of any specific Applicant Tracking System.

## Features

- **Job Description Upload:** Upload a JD in PDF or DOCX format using the `/jd` command.
- **Resume Analysis:** Analyze multiple resumes against the active job description using `/analyze`.
- **ATS Score:** Generate an overall score out of 100 for each resume.
- **Category-wise Scoring:** Evaluate resumes across seven categories.
- **Skill Matching:** Identify skills that match the job description.
- **Skill Gap Analysis:** Highlight missing or insufficiently matched skills.
- **Improvement Suggestions:** Provide recommendations to improve resume alignment with the job requirements.
- **Learning Resources:** Generate Udemy and Coursera search links for relevant skills.
- **Resume Ranking:** Display all analyzed resumes in descending order of ATS score.
- **Status Tracking:** View the active job description, number of analyzed resumes, and ranked results using `/status`.
- **Clear Session:** Reset the active job description and analysis results using `/clear`.

## ATS Scoring Model

The analyzer uses a custom weighted scoring model with seven categories.

| Category | Weight |
|---|---:|
| Skills | 30% |
| Experience | 20% |
| Education | 15% |
| Certifications | 10% |
| Keywords | 10% |
| Projects | 10% |
| Structure | 5% |
| **Total** | **100%** |

The overall score is calculated using these category weights. This is a project-specific scoring model, not a universal ATS standard.

## Tech Stack

- **Language:** Python
- **Bot Platform:** Discord
- **Discord Library:** discord.py
- **Environment Variables:** python-dotenv
- **Document Processing:** PyMuPDF, python-docx
- **Output:** Discord messages and formatted analysis reports

## Project Workflow

1. Upload a job description using `/jd`.
2. Upload one or more resumes using `/analyze`.
3. The bot extracts text from the uploaded documents.
4. The analyzer compares resume content with the active job description.
5. It calculates the overall ATS score and category-wise scores.
6. It identifies matching skills, missing skills, and improvement opportunities.
7. It returns the analysis and learning resources through Discord.
8. Use `/status` to compare and rank analyzed resumes.

## Discord Commands

| Command | Description |
|---|---|
| `/jd` | Upload and set the active job description |
| `/analyze` | Analyze resumes against the active JD |
| `/status` | View the active JD and ranked analysis results |
| `/clear` | Clear the active JD and analysis results |

*Command names and behavior may depend on the current bot implementation.*

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- A Discord account
- A Discord application and bot created in the Discord Developer Portal

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/discord-ats-resume-analyzer.git
cd discord-ats-resume-analyzer
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install discord.py python-dotenv PyMuPDF python-docx
```

If the repository includes a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```
### 4. Create a Discord Bot

Follow these steps to create and configure your Discord bot.

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**, enter a name for your bot, and create the application.
3. Navigate to the **Bot** section in the left sidebar.
4. Create the bot if prompted, then generate or reset its token.
5. Copy the bot token and store it securely. Never share it or commit it to GitHub.
6. Navigate to **OAuth2 → URL Generator**.
7. Under **Scopes**, select:
   - `bot`
   - `applications.commands`
8. Under **Bot Permissions**, select the permissions required by your bot, such as:
   - View Channels
   - Send Messages
   - Attach Files
   - Read Message History
9. Copy the generated URL, open it in your browser, and invite the bot to a Discord server where you have permission to add applications.
10. If your bot uses message content or other privileged gateway intents, configure the required intents under **Bot → Privileged Gateway Intents** and enable the corresponding intents in your Python code.

**Important:** Keep your bot token private. If it is exposed, reset it immediately in the Developer Portal.

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_discord_bot_token
```

Get the bot token from the [Discord Developer Portal](https://discord.com/developers/applications).

**Security:** Never commit your `.env` file or expose your Discord bot token publicly. Add `.env` and `venv/` to `.gitignore`.

### 6. Run the Bot

```bash
python bot.py
```

Once the bot starts successfully, open your Discord server and use its slash commands.

## Example Analysis

An analysis report may contain:

- Resume filename
- Job description used for comparison
- Overall ATS score out of 100
- Category-wise scores
- Matching skills
- Missing skills
- Improvement suggestions
- Relevant learning resources

The `/status` command can display multiple analyzed resumes ranked from the highest score to the lowest score.

## Future Enhancements

- Integrate Amazon S3 for document storage.
- Use Amazon DynamoDB for persistent job descriptions and analysis results.
- Explore AWS Lambda for serverless resume processing.
- Add AWS IAM and Secrets Manager for secure access and credential management.
- Use Amazon CloudWatch for application logs and monitoring.
- Provision AWS infrastructure using Terraform.
- Automate testing and deployment using GitHub Actions.
- Improve semantic matching and resume recommendations.

## Learning Outcomes

This project demonstrates practical experience with:

- Python application development
- Discord bot development and slash commands
- PDF and DOCX text extraction
- Custom scoring and keyword-matching logic
- Resume evaluation and skill-gap analysis
- Environment variable management
- Cloud architecture planning and AWS integration opportunities

## Disclaimer

This project is intended for educational and informational purposes. ATS scores and recommendations are estimates, not hiring decisions. A higher score does not guarantee that a resume will pass an employer's screening system.

## Author

**Jahid Khan**

Computer Science and Engineering | AWS Certified Solutions Architect – Associate | AWS Certified Cloud Practitioner
