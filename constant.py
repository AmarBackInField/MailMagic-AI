
    # HTML Templates (you might want to move this to constants.py)
HTML_TEMPLATES = {
        "Job Application": {
            "Tech Professional": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
        }
        .highlight {
            font-weight: bold;
            color: #2c3e50;
        }
        .experience-list {
            margin-left: 20px;
        }
        .experience-list li {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <p>Dear Hiring Manager,</p>

    <p>I am writing to express my strong interest in opportunities at <span class="highlight">[COMPANY_NAME]</span>. With my professional experience and skill set, I am confident I can contribute to your team.</p>

    <p>My key experiences and skills include:</p>

    <ul class="experience-list">
        <li><span class="highlight">Professional Experience:</span> Detailed description of your most relevant work experience.</li>
        <li><span class="highlight">Technical Skills:</span> List of your core technical competencies.</li>
        <li><span class="highlight">Key Achievements:</span> Highlight your most significant professional accomplishments.</li>
    </ul>

    <p>I am particularly enthusiastic about the innovative work being done at <span class="highlight">[COMPANY_NAME]</span>. My background aligns well with the potential opportunities at your company.</p>

    <p>Thank you for considering my application. I look forward to discussing how my skills and experience can contribute to your team's success.</p>

    <p>Sincerely,<br>
    [YOUR_NAME]</p>
</body>
</html>
            """,
            "Recent Graduate": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
        }
        .highlight {
            font-weight: bold;
            color: #2c3e50;
        }
        .experience-list {
            margin-left: 20px;
        }
        .experience-list li {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <p>Dear Hiring Manager,</p>

    <p>I am a recent graduate from [UNIVERSITY_NAME], writing to express my interest in opportunities at <span class="highlight">[COMPANY_NAME]</span>. My academic background and internship experiences have prepared me to contribute effectively to your team.</p>

    <p>My academic and professional highlights include:</p>

    <ul class="experience-list">
        <li><span class="highlight">Academic Achievements:</span> Relevant coursework, projects, and academic honors.</li>
        <li><span class="highlight">Internship Experience:</span> Description of internships and key learnings.</li>
        <li><span class="highlight">Skills:</span> Technical and soft skills relevant to the position.</li>
    </ul>

    <p>I am excited about the opportunity to bring my fresh perspective and enthusiasm to <span class="highlight">[COMPANY_NAME]</span>.</p>

    <p>Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team.</p>

    <p>Sincerely,<br>
    [YOUR_NAME]</p>
</body>
</html>
            """
        },
        "Networking": {
            "Professional Outreach": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
        }
        .highlight {
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <p>Dear [NAME],</p>

    <p>I hope this email finds you well. I am reaching out to connect and explore potential opportunities in [INDUSTRY/FIELD].</p>

    <p>My professional background includes:</p>
    <ul>
        <li>Key professional experiences</li>
        <li>Relevant skills and achievements</li>
    </ul>

    <p>I would appreciate the opportunity to connect and learn more about your insights and experiences in [INDUSTRY/FIELD].</p>

    <p>Thank you for your time and consideration.</p>

    <p>Best regards,<br>
    [YOUR_NAME]</p>
</body>
</html>
            """
        }
    }