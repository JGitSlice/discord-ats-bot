import os
import re
import discord
from discord.ext import commands
from discord import app_commands

from jd_parser import extract_pdf_text, extract_docx_text


# ============================================================
# CONFIG
# ============================================================

SERVER_ID = YOUR_SERVER_ID_HERE
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"


# ============================================================
# BOT SETUP
# ============================================================

class ATSBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        guild = discord.Object(id=SERVER_ID)

        self.tree.copy_global_to(guild=guild)

        synced = await self.tree.sync(guild=guild)

        print(f"Synced {len(synced)} command(s) to server")


bot = ATSBot()


# ============================================================
# STORAGE
# ============================================================

# Stores active JD for each Discord user
current_jd = {}

# Stores multiple resume analyses for each Discord user
analyses = {}


# ============================================================
# SKILL DATABASE
# ============================================================

SKILLS = [

    # AWS
    "aws",
    "amazon web services",
    "ec2",
    "s3",
    "rds",
    "aurora",
    "dynamodb",
    "lambda",
    "iam",
    "vpc",
    "cloudfront",
    "route 53",
    "route53",
    "cloudwatch",
    "cloudtrail",
    "sns",
    "sqs",
    "api gateway",
    "elastic load balancer",
    "elb",
    "alb",
    "nlb",
    "auto scaling",
    "autoscaling",
    "ecs",
    "eks",
    "ecr",
    "fargate",
    "elastic beanstalk",
    "lightsail",
    "eventbridge",
    "step functions",
    "secrets manager",
    "systems manager",
    "kms",
    "waf",
    "shield",
    "guardduty",
    "inspector",
    "security hub",
    "organizations",
    "cognito",
    "elasticache",
    "redshift",
    "glue",
    "athena",
    "kinesis",
    "quicksight",
    "opensearch",
    "cloudformation",
    "cdk",

    # Azure
    "azure",
    "microsoft azure",
    "azure vm",
    "azure functions",
    "azure storage",
    "azure devops",
    "azure active directory",
    "microsoft entra id",
    "azure kubernetes service",
    "aks",

    # GCP
    "gcp",
    "google cloud",
    "google cloud platform",
    "compute engine",
    "cloud storage",
    "cloud functions",
    "cloud run",
    "gke",
    "google kubernetes engine",
    "bigquery",

    # DevOps / IaC
    "devops",
    "ci/cd",
    "cicd",
    "continuous integration",
    "continuous delivery",
    "continuous deployment",
    "infrastructure as code",
    "iac",
    "terraform",
    "terraform cloud",
    "terraform modules",
    "terraform state",
    "terragrunt",
    "pulumi",
    "ansible",
    "chef",
    "puppet",

    # Containers
    "docker",
    "docker compose",
    "dockerfile",
    "containerization",
    "containers",
    "kubernetes",
    "k8s",
    "helm",
    "helm charts",
    "openshift",
    "podman",

    # CI/CD tools
    "jenkins",
    "github actions",
    "gitlab ci",
    "gitlab",
    "circleci",
    "travis ci",
    "azure pipelines",
    "argo cd",
    "argocd",
    "spinnaker",

    # Git
    "git",
    "github",
    "gitlab",
    "bitbucket",
    "version control",
    "git branching",
    "pull requests",

    # Operating Systems
    "linux",
    "ubuntu",
    "red hat",
    "rhel",
    "centos",
    "unix",
    "windows server",
    "bash",
    "shell scripting",
    "powershell",

    # Programming
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    ".net",
    "go",
    "golang",
    "ruby",
    "php",
    "scala",
    "rust",

    # Web
    "html",
    "css",
    "react",
    "react.js",
    "angular",
    "vue",
    "node.js",
    "nodejs",
    "express",
    "next.js",
    "nextjs",
    "spring",
    "spring boot",
    "django",
    "flask",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "oracle",
    "sql server",
    "microsoft sql server",
    "mongodb",
    "redis",
    "cassandra",
    "database design",
    "database administration",

    # Networking
    "networking",
    "tcp/ip",
    "tcp",
    "udp",
    "dns",
    "http",
    "https",
    "ssl",
    "tls",
    "vpn",
    "ipsec",
    "firewall",
    "proxy",
    "load balancing",
    "routing",
    "subnetting",
    "ipv4",
    "ipv6",
    "nat",
    "dhcp",
    "cdn",

    # Security
    "cybersecurity",
    "cloud security",
    "network security",
    "application security",
    "identity and access management",
    "authentication",
    "authorization",
    "oauth",
    "oauth2",
    "jwt",
    "encryption",
    "zero trust",
    "devsecops",
    "vulnerability management",
    "penetration testing",
    "security testing",

    # Monitoring
    "monitoring",
    "observability",
    "logging",
    "prometheus",
    "grafana",
    "elk stack",
    "elasticsearch",
    "logstash",
    "kibana",
    "splunk",
    "datadog",
    "new relic",
    "opentelemetry",

    # AI / ML
    "artificial intelligence",
    "ai",
    "machine learning",
    "deep learning",
    "generative ai",
    "genai",
    "llm",
    "large language models",
    "natural language processing",
    "nlp",
    "computer vision",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",

    # Software Engineering
    "software development",
    "software engineering",
    "object oriented programming",
    "oop",
    "data structures",
    "algorithms",
    "rest api",
    "restful api",
    "api development",
    "microservices",
    "distributed systems",
    "system design",
    "design patterns",
    "unit testing",
    "integration testing",
    "test automation",
    "debugging",

    # Agile
    "agile",
    "scrum",
    "kanban",
    "jira",
    "confluence",
    "project management",
    "software development lifecycle",
    "sdlc",

    # Cloud Architecture
    "cloud computing",
    "cloud architecture",
    "cloud migration",
    "high availability",
    "scalability",
    "fault tolerance",
    "disaster recovery",
    "backup",
    "multi-region",
    "multi-az",
    "serverless",
    "event-driven architecture",
    "three-tier architecture",
    "monolithic architecture",
    "microservice architecture"
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    text = normalize_text(text)

    found = []

    for skill in SKILLS:

        # Escape special regex characters
        pattern = re.escape(skill)

        # Word boundary matching
        if re.search(
            rf"(?<!\w){pattern}(?!\w)",
            text
        ):
            found.append(skill)

    return found


# ============================================================
# GENERIC CATEGORY MATCHING
# ============================================================

def keyword_match_score(jd_text, resume_text, keywords):

    jd_text = normalize_text(jd_text)
    resume_text = normalize_text(resume_text)

    jd_found = []

    for keyword in keywords:

        pattern = re.escape(keyword)

        if re.search(
            rf"(?<!\w){pattern}(?!\w)",
            jd_text
        ):
            jd_found.append(keyword)

    if not jd_found:
        return 100

    matched = 0

    for keyword in jd_found:

        pattern = re.escape(keyword)

        if re.search(
            rf"(?<!\w){pattern}(?!\w)",
            resume_text
        ):
            matched += 1

    return round(
        (matched / len(jd_found)) * 100
    )


# ============================================================
# SKILLS COMPARISON
# ============================================================

def compare_skills(jd_text, resume_text):

    jd_skills = set(
        extract_skills(jd_text)
    )

    resume_skills = set(
        extract_skills(resume_text)
    )

    if not jd_skills:

        return {
            "score": 100,
            "matching": [],
            "missing": []
        }

    matching = sorted(
        jd_skills & resume_skills
    )

    missing = sorted(
        jd_skills - resume_skills
    )

    score = round(
        (len(matching) / len(jd_skills)) * 100
    )

    return {
        "score": score,
        "matching": matching,
        "missing": missing
    }


# ============================================================
# EDUCATION COMPARISON
# ============================================================

def compare_education(jd_text, resume_text):

    jd = normalize_text(jd_text)
    resume = normalize_text(resume_text)

    education_keywords = [

        "bachelor",
        "bachelors",
        "b.tech",
        "btech",
        "b.e",
        "be ",
        "computer science",
        "computer engineering",
        "information technology",
        "master",
        "masters",
        "m.tech",
        "mtech",
        "m.e",
        "mba",
        "degree",
        "diploma",
        "phd",
        "ph.d"
    ]

    jd_requirements = []

    for keyword in education_keywords:

        if keyword in jd:
            jd_requirements.append(keyword)

    if not jd_requirements:

        return 100

    matched = 0

    for keyword in set(jd_requirements):

        if keyword in resume:
            matched += 1

    return round(
        (matched / len(set(jd_requirements))) * 100
    )


# ============================================================
# EXPERIENCE COMPARISON
# ============================================================

def compare_experience(jd_text, resume_text):

    jd = normalize_text(jd_text)
    resume = normalize_text(resume_text)

    experience_keywords = [

        "experience",
        "internship",
        "intern",
        "years",
        "year",
        "developer",
        "engineer",
        "administrator",
        "architect",
        "devops",
        "cloud engineer",
        "software engineer",
        "system administrator",
        "responsibilities",
        "work experience"
    ]

    jd_requirements = []

    for keyword in experience_keywords:

        if keyword in jd:
            jd_requirements.append(keyword)

    if not jd_requirements:

        return 100

    matched = 0

    for keyword in set(jd_requirements):

        if keyword in resume:
            matched += 1

    return round(
        (matched / len(set(jd_requirements))) * 100
    )


# ============================================================
# CERTIFICATION COMPARISON
# ============================================================

def compare_certifications(jd_text, resume_text):

    certification_keywords = [

        "certification",
        "certified",
        "aws certified",
        "aws certification",
        "azure certification",
        "azure certified",
        "google cloud certification",
        "gcp certification",
        "oracle certification",
        "oci",
        "comptia",
        "ccna",
        "cka",
        "ckad",
        "terraform associate"
    ]

    return keyword_match_score(
        jd_text,
        resume_text,
        certification_keywords
    )


# ============================================================
# KEYWORDS COMPARISON
# ============================================================

def compare_keywords(jd_text, resume_text):

    jd_text = normalize_text(jd_text)
    resume_text = normalize_text(resume_text)

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#./-]{2,}\b",
        jd_text
    )

    # Remove common words
    stop_words = {

        "the",
        "and",
        "for",
        "with",
        "you",
        "your",
        "are",
        "our",
        "this",
        "that",
        "from",
        "will",
        "have",
        "has",
        "must",
        "should",
        "can",
        "job",
        "role",
        "work",
        "about",
        "into",
        "using",
        "their",
        "they",
        "who",
        "what",
        "where",
        "when",
        "how"
    }

    jd_keywords = set(
        word
        for word in words
        if word not in stop_words
    )

    if not jd_keywords:

        return 100

    matched = 0

    for keyword in jd_keywords:

        if keyword in resume_text:
            matched += 1

    return round(
        (matched / len(jd_keywords)) * 100
    )


# ============================================================
# PROJECT COMPARISON
# ============================================================

def compare_projects(jd_text, resume_text):

    jd = normalize_text(jd_text)
    resume = normalize_text(resume_text)

    project_keywords = [

        "project",
        "projects",
        "built",
        "developed",
        "implemented",
        "designed",
        "deployed",
        "application",
        "system",
        "architecture",
        "platform",
        "website",
        "api",
        "automation",
        "infrastructure"
    ]

    jd_requirements = []

    for keyword in project_keywords:

        if keyword in jd:
            jd_requirements.append(keyword)

    if not jd_requirements:

        return 100

    matched = 0

    for keyword in set(jd_requirements):

        if keyword in resume:
            matched += 1

    return round(
        (matched / len(set(jd_requirements))) * 100
    )


# ============================================================
# RESUME STRUCTURE
# ============================================================

def compare_structure(resume_text):

    text = normalize_text(resume_text)

    sections = {

        "education": [
            "education",
            "academic"
        ],

        "experience": [
            "experience",
            "work experience",
            "internship"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "projects": [
            "projects",
            "project"
        ],

        "certifications": [
            "certifications",
            "certification"
        ],

        "summary": [
            "summary",
            "objective",
            "profile"
        ]
    }

    found_sections = 0

    for section_keywords in sections.values():

        found = False

        for keyword in section_keywords:

            if keyword in text:

                found = True
                break

        if found:
            found_sections += 1

    score = round(
        (found_sections / len(sections)) * 100
    )

    return score


# ============================================================
# OVERALL ATS SCORE
# ============================================================

def calculate_overall_score(scores):

    weights = {

        "skills": 30,
        "experience": 20,
        "education": 15,
        "certifications": 10,
        "keywords": 10,
        "projects": 10,
        "structure": 5
    }

    total = (

        scores["skills"] *
        weights["skills"] / 100

        +

        scores["experience"] *
        weights["experience"] / 100

        +

        scores["education"] *
        weights["education"] / 100

        +

        scores["certifications"] *
        weights["certifications"] / 100

        +

        scores["keywords"] *
        weights["keywords"] / 100

        +

        scores["projects"] *
        weights["projects"] / 100

        +

        scores["structure"] *
        weights["structure"] / 100
    )

    return round(total)


# ============================================================
# LEARNING RESOURCE LINKS
# ============================================================

def create_learning_links(missing_skills):

    if not missing_skills:

        return "No major missing skills detected."

    # Limit links so Discord message does not become too large
    skills = missing_skills[:8]

    lines = []

    for skill in skills:

        query = skill.replace(
            " ",
            "+"
        )

        udemy_url = (
            "https://www.udemy.com/courses/search/?q="
            + query
        )

        coursera_url = (
            "https://www.coursera.org/search?query="
            + query
        )

        lines.append(
            f"**{skill.title()}**\n"
            f"• Udemy: {udemy_url}\n"
            f"• Coursera: {coursera_url}"
        )

    return "\n\n".join(lines)


# ============================================================
# RESUME SUGGESTIONS
# ============================================================

def generate_suggestions(
    missing_skills,
    scores
):

    suggestions = []

    # Skills
    if scores["skills"] < 70:

        if missing_skills:

            missing_text = ", ".join(
                skill.title()
                for skill in missing_skills[:8]
            )

            suggestions.append(
                "Add relevant experience or projects "
                f"demonstrating: {missing_text}."
            )

        suggestions.append(
            "Include important JD skills in your Skills "
            "section when you genuinely have those skills."
        )

    # Experience
    if scores["experience"] < 70:

        suggestions.append(
            "Highlight internships, work experience, "
            "responsibilities, and technologies that are "
            "relevant to the JD."
        )

    # Education
    if scores["education"] < 70:

        suggestions.append(
            "Clearly mention your degree, specialization, "
            "college/university, and graduation year."
        )

    # Certifications
    if scores["certifications"] < 70:

        suggestions.append(
            "Add relevant professional certifications "
            "that match the technologies or requirements "
            "in the JD."
        )

    # Keywords
    if scores["keywords"] < 70:

        suggestions.append(
            "Use relevant terminology from the JD naturally "
            "throughout your resume where it accurately "
            "describes your experience."
        )

    # Projects
    if scores["projects"] < 70:

        suggestions.append(
            "Add projects that demonstrate technologies "
            "and responsibilities mentioned in the JD."
        )

    # Structure
    if scores["structure"] < 70:

        suggestions.append(
            "Use clear sections such as Summary, Skills, "
            "Education, Experience, Projects, and Certifications."
        )

    # General suggestions
    suggestions.append(
        "Add measurable results to important projects "
        "and work experience whenever possible."
    )

    suggestions.append(
        "Keep the resume concise, consistent, and "
        "easy for ATS software to parse."
    )

    return suggestions


# ============================================================
# HELLO COMMAND
# ============================================================

@bot.tree.command(
    name="hello",
    description="Check if the ATS bot is working"
)
async def hello(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        "ATS Resume Analyzer is online!"
    )


# ============================================================
# JD COMMAND
# ============================================================

@bot.tree.command(
    name="jd",
    description="Upload a Job Description PDF or DOCX"
)
@app_commands.describe(
    file="Upload your Job Description as PDF or DOCX"
)
async def jd(
    interaction: discord.Interaction,
    file: discord.Attachment
):

    filename = file.filename.lower()

    # Check file type
    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):

        await interaction.response.send_message(
            "Please upload a PDF or DOCX file."
        )

        return

    # Check file size
    if file.size > 10 * 1024 * 1024:

        await interaction.response.send_message(
            "File is too large. Maximum size is 10 MB."
        )

        return

    os.makedirs(
        "data",
        exist_ok=True
    )

    file_path = os.path.join(
        "data",
        file.filename
    )

    await file.save(file_path)

    try:

        # Extract JD text
        if filename.endswith(".pdf"):

            jd_text = extract_pdf_text(
                file_path
            )

        else:

            jd_text = extract_docx_text(
                file_path
            )

        # Check extraction
        if not jd_text.strip():

            await interaction.response.send_message(
                "I couldn't extract any text from this file."
            )

            return

        # Store active JD
        current_jd[
            interaction.user.id
        ] = {

            "filename": file.filename,

            "text": jd_text
        }

        # Reset old analyses when a new JD is uploaded
        analyses[
            interaction.user.id
        ] = []

        await interaction.response.send_message(

            f"## Job Description Uploaded\n\n"

            f"**File:** {file.filename}\n"

            f"**Extracted:** "
            f"{len(jd_text)} characters\n\n"

            f"Your JD is now **active**.\n\n"

            f"Upload a resume using "
            f"`/analyze`."
        )

    except Exception as e:

        await interaction.response.send_message(
            f"Error processing file: `{e}`"
        )


# ============================================================
# ANALYZE COMMAND
# ============================================================

@bot.tree.command(
    name="analyze",
    description="Analyze a resume against the active Job Description"
)
@app_commands.describe(
    file="Upload your resume as PDF or DOCX"
)
async def analyze(
    interaction: discord.Interaction,
    file: discord.Attachment
):

    user_id = interaction.user.id

    # Check active JD
    if user_id not in current_jd:

        await interaction.response.send_message(

            "No active Job Description found.\n\n"

            "Please upload a JD first using `/jd`."
        )

        return

    filename = file.filename.lower()

    # Check file type
    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):

        await interaction.response.send_message(
            "Please upload your resume as PDF or DOCX."
        )

        return

    # Check file size
    if file.size > 10 * 1024 * 1024:

        await interaction.response.send_message(
            "Resume is too large. Maximum size is 10 MB."
        )

        return

    os.makedirs(
        "data",
        exist_ok=True
    )

    file_path = os.path.join(
        "data",
        file.filename
    )

    await file.save(file_path)

    try:

        # Extract resume text
        if filename.endswith(".pdf"):

            resume_text = extract_pdf_text(
                file_path
            )

        else:

            resume_text = extract_docx_text(
                file_path
            )

        # Check extraction
        if not resume_text.strip():

            await interaction.response.send_message(
                "I couldn't extract any text from the resume."
            )

            return

        # Get JD
        jd_info = current_jd[user_id]

        jd_text = jd_info["text"]
        jd_filename = jd_info["filename"]

        # ====================================================
        # CATEGORY COMPARISON
        # ====================================================

        skill_result = compare_skills(
            jd_text,
            resume_text
        )

        skills_score = skill_result[
            "score"
        ]

        matching = skill_result[
            "matching"
        ]

        missing = skill_result[
            "missing"
        ]

        education_score = compare_education(
            jd_text,
            resume_text
        )

        experience_score = compare_experience(
            jd_text,
            resume_text
        )

        certification_score = compare_certifications(
            jd_text,
            resume_text
        )

        keyword_score = compare_keywords(
            jd_text,
            resume_text
        )

        project_score = compare_projects(
            jd_text,
            resume_text
        )

        structure_score = compare_structure(
            resume_text
        )

        # ====================================================
        # SCORE DICTIONARY
        # ====================================================

        scores = {

            "skills": skills_score,

            "experience": experience_score,

            "education": education_score,

            "certifications": certification_score,

            "keywords": keyword_score,

            "projects": project_score,

            "structure": structure_score
        }

        # ====================================================
        # OVERALL SCORE
        # ====================================================

        overall_score = calculate_overall_score(
            scores
        )

        # ====================================================
        # SUGGESTIONS
        # ====================================================

        suggestions = generate_suggestions(
            missing,
            scores
        )

        # ====================================================
        # LEARNING RESOURCES
        # ====================================================

        learning_resources = create_learning_links(
            missing
        )

        # ====================================================
        # STORE ANALYSIS
        # ====================================================

        if user_id not in analyses:

            analyses[user_id] = []

        analyses[user_id].append({

            "resume": file.filename,

            "score": overall_score,

            "category_scores": scores,

            "matching": matching,

            "missing": missing
        })

        # ====================================================
        # FORMAT MATCHING SKILLS
        # ====================================================

        if matching:

            matching_text = ", ".join(

                skill.title()
                for skill in matching
            )

        else:

            matching_text = (
                "None detected"
            )

        # ====================================================
        # FORMAT MISSING SKILLS
        # ====================================================

        if missing:

            missing_text = ", ".join(

                skill.title()
                for skill in missing
            )

        else:

            missing_text = (
                "None detected"
            )

        # ====================================================
        # FORMAT SUGGESTIONS
        # ====================================================

        suggestions_text = "\n".join(

            f"• {item}"
            for item in suggestions
        )

        # ====================================================
        # SEND RESULT
        # ====================================================

        # ====================================================
        # SEND RESULT - ONE DISCORD MESSAGE
        # ====================================================

        if matching:
            matching_text = ", ".join(
                skill.title() for skill in matching
            )
        else:
            matching_text = "None detected"


        if missing:
            missing_text = ", ".join(
                skill.title() for skill in missing
            )
        else:
            missing_text = "None detected"


        # Keep the most important skills within the message limit
        matching_text = matching_text[:400]

        missing_text = missing_text[:400]


        # Keep suggestions compact
        suggestions_text = "\n".join(
            f"• {item}" for item in suggestions
        )


        # Compact learning resources
        if missing:

            resource_lines = []

            for skill in missing[:3]:

                query = skill.replace(" ", "+")

                udemy_url = (
                    "https://www.udemy.com/courses/search/?q="
                    + query
                )

                coursera_url = (
                    "https://www.coursera.org/search?query="
                    + query
                )

                resource_lines.append(
                    f"• **{skill.title()}**: "
                    f"[Udemy]({udemy_url}) | "
                    f"[Coursera]({coursera_url})"
                )

            learning_resources = "\n".join(
                resource_lines
            )

        else:

            learning_resources = "No major missing skills detected."


        # ====================================================
        # BUILD ONE MESSAGE
        # ====================================================

        message = (
            f"## Resume ATS Analysis\n\n"

            f"**Resume:** {file.filename}\n"
            f"**Current Active JD:** {jd_filename}\n"
            f"**Overall ATS Score:** **{overall_score}/100**\n\n"

            f"### ATS Category Breakdown\n"
            f"• Skills: **{skills_score}%**\n"
            f"• Experience: **{experience_score}%**\n"
            f"• Education: **{education_score}%**\n"
            f"• Certifications: **{certification_score}%**\n"
            f"• Keywords: **{keyword_score}%**\n"
            f"• Projects: **{project_score}%**\n"
            f"• Structure: **{structure_score}%**\n\n"

            f"### Matching Skills\n"
            f"{matching_text}\n\n"

            f"### Missing / Lacking Skills\n"
            f"{missing_text}\n\n"

            f"### Resume Suggestions\n"
            f"{suggestions_text}\n\n"

            f"### Learning Resources\n"
            f"{learning_resources}"
        )


        # ====================================================
        # FINAL SAFETY LIMIT
        # ====================================================

        if len(message) > 2000:

            message = message[:1990] + "\n..."


        # ====================================================
        # SEND ONLY ONE MESSAGE
        # ====================================================

        await interaction.response.send_message(
            message
        )

    except Exception as e:

        await interaction.response.send_message(
            f"Error analyzing resume: `{e}`"
        )


# ============================================================
# STATUS COMMAND
# ============================================================

@bot.tree.command(
    name="status",
    description="Show the currently active Job Description"
)
async def status(
    interaction: discord.Interaction
):

    user_id = interaction.user.id

    if user_id not in current_jd:

        await interaction.response.send_message(
            "No Job Description is currently active."
        )

        return

    jd_info = current_jd[
        user_id
    ]

    user_analyses = analyses.get(user_id, [])

    resume_count = len(user_analyses)

    all_resumes = sorted(
        user_analyses,
        key=lambda x: x["score"],
        reverse=True
    )

    user_analyses = analyses.get(user_id, [])

    top_resume = None

    if user_analyses:
        top_resume = max(
            user_analyses,
            key=lambda x: x["score"]
        )

    if all_resumes:

        resume_list = "\n".join(
            f"**{index}.** {resume['resume']} — "
            f"**{resume['score']}/100**"
            for index, resume in enumerate(all_resumes, start=1)
        )

    else:

        resume_list = "No resumes analyzed yet."


    await interaction.response.send_message(

        f"## Active Job Description\n\n"

        f"**File:** "
        f"{jd_info['filename']}\n"

        f"**Characters:** "
        f"{len(jd_info['text'])}\n"

        f"**Resumes Analyzed:** "
        f"{resume_count}\n\n"

        f"### All Resumes\n"
        f"{resume_list}\n\n"

        f"Upload another resume using `/analyze`."
    )


# ============================================================
# CLEAR COMMAND
# ============================================================

@bot.tree.command(
    name="clear",
    description="Clear the active JD and resume analyses"
)
async def clear(
    interaction: discord.Interaction
):

    user_id = interaction.user.id

    current_jd.pop(
        user_id,
        None
    )

    analyses.pop(
        user_id,
        None
    )

    await interaction.response.send_message(

        "Your active JD and resume analyses "
        "have been cleared."
    )


# ============================================================
# BOT READY
# ============================================================

@bot.event
async def on_ready():

    print(
        f"Bot logged in as {bot.user}"
    )


# ============================================================
# START BOT
# ============================================================

bot.run(BOT_TOKEN)