
# Flask Vulnerable App: Setup and Exploitation Guide

This guide walks you through setting up a vulnerable Flask application, running it on your local machine, and exploiting the email body injection vulnerability to understand how such issues work in real-world scenarios. **Use this guide only in a controlled environment for educational purposes.**

---

## Prerequisites

1. **Python 3 Installed**: Make sure Python 3 is installed on your system.
   - Check with:
     ```bash
     python3 --version
     ```
   - Download from [python.org](https://www.python.org/downloads/) if necessary.

2. **Docker Installed**: Ensure Docker is installed on your system.
   - Check Docker version:
     ```bash
     docker --version
     ```

3. **Basic Command Line Knowledge**: Ability to navigate and run commands in the terminal.

---

## Setting Up the Application
### Step 1: Clone the following github repo
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

### Step 2: Configure Email Settings
Set Up Gmail App Password:

- Enable 2-Step Verification for your Google account [here](https://myaccount.google.com/security?gar=WzEyMF0&hl=en&utm_source=OGB&utm_medium=act&rapt=AEjHL4OCmGVPvwn45kqsLYG3RhKkyUhFCoEA77ZTeGYPs8_PzGNh1EPqwUzpW5ZXB9UOqEYHVHxH96-NmX-kkH6SCbt4azKW2UkjsTEBsojtE2N_Bw-n-bc)
- Generate an App Password [here](https://myaccount.google.com/apppasswords?continue=https://myaccount.google.com/security?gar%3DWzEyMF0%26hl%3Den%26utm_source%3DOGB%26utm_medium%3Dact%26rapt%3DAEjHL4OCmGVPvwn45kqsLYG3RhKkyUhFCoEA77ZTeGYPs8_PzGNh1EPqwUzpW5ZXB9UOqEYHVHxH96-NmX-kkH6SCbt4azKW2UkjsTEBsojtE2N_Bw-n-bc&rapt=AEjHL4N3nzWjhYvrOZIz3nB_uUxzvdUus3QhRUOtC_UMyb_THHlkLM64orrxgBYArLicCYZ6LG36WwJXNRh90-1cbsImhTtJ0LAo31mix19DZHFyXmt846E).
- Replace the placeholders in send_email:
  - your-email@gmail.com : Your Gmail address.
  - your-app-password : The App Password you generated.


### Step 3: Modify the config.yaml file with the credentials 

``` yaml
email:
  from_email: "xxx@gmail.com" # replace with your email address
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  smtp_password: "xxxxxxx" # replace with your password
```
### Step 4: Building and Running with Docker

1. **Build the Docker Image**:
   ```bash
   sudo docker build -t email-body-injection .
   ```

2. **Run the Container**:
   ```bash
   sudo docker run -p 5000:5000 email-body-injection
   ```

3. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

4. **Stop the Application**:
   Press `Ctrl+C` in the terminal running the container or stop it using:
   ```bash
   sudo docker stop $(sudo docker ps -q --filter ancestor=email-body-injection)
   ```

---

## Exploiting the Vulnerability

### Payload for Exploitation

After entering the victim's email address in the appropriate field, use the following payload in the **Custom Message field** to exploit the vulnerability:

```html
I am inviting you to join me!<br><br>
<a href="https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran" style="color: white; background-color: #007bff; padding: 10px 15px; text-decoration: none; border-radius: 5px;">Click here to join!</a>
<p style='color: #777;'>If you have any questions, feel free to contact our support team.</p>
<!--
```

### Steps to Exploit

1. On the `/` page, enter:
   - **Friend's Email**: A test email you can access.
   - **Custom Message**: Paste the payload above.

2. Submit the form.

3. Check the email received by the recipient:
   - The malicious button will appear.
   - Legitimate content will be hidden due to the (<!--) comment.

---
# Impact

This vulnerability demonstrates the potential risks associated with improper input sanitization in web applications, specifically within email generation. The key impacts include:

1. **Phishing and Social Engineering**:  
   - Attackers can inject malicious links, buttons, or deceptive content into emails sent through the application. These emails appear legitimate, making it easier for attackers to trick recipients into interacting with the content, potentially exposing them to phishing scams or malware.

2. **Enterprise Reputation Damage**:  
   - Since the emails are sent from the organization's email account, exploitation of this vulnerability can tarnish the organization’s credibility. Attackers can inject harmful or inappropriate content, such as terrorist propaganda, political messages, or adult content, into the emails. Recipients may associate this malicious content with the organization, leading to severe loss of trust, significant brand damage, and potential financial and legal repercussions.

3. **Facilitation of XSS and CSRF Attacks**:  
   - The vulnerability simplifies the exploitation of cross-site scripting (XSS) and cross-site request forgery (CSRF) attacks. By injecting malicious payloads or links directly into the email's buttons or other HTML elements, attackers can bypass other security mechanisms and directly exploit recipients who interact with the email. 

# Mitigation
To effectively address the email body injection vulnerability and reduce associated risks, implement the following enhanced measures:

1. **Input Validation**:

- Enforce strict validation rules for all user inputs before they are processed or included in any application logic.
- Use a whitelist approach to allow only expected and safe characters based on the context (e.g., alphanumeric characters for names, specific formats for email addresses). Reject inputs that contain suspicious characters, such as <, >, or script.
- Implement server-side validation to ensure that malicious inputs bypassing client-side checks are still caught.

2. **Output Sanitization**:

- Before including user-provided data in emails, sanitize the content to remove any potentially dangerous HTML or JavaScript.
- Utilize trusted libraries such as **Bleach** for Python, which automatically escapes or removes unsafe tags and attributes.
- Always encode special characters (e.g., &, <, >, ") in user inputs to their corresponding HTML entities to prevent them from being interpreted as HTML or JavaScript.

3. **Use a Secure Email Template System**:

- Design emails using predefined, server-side templates that only include placeholders for safe, sanitized dynamic content.
- Templates should limit customization to trusted variables (e.g., recipient name or a plain-text message) and disallow direct injection of raw HTML or scripts from user inputs.
- If any user-provided content must be included in an email, ensure it is both validated and sanitized before being inserted into the template.

## Key Takeaways

- This app demonstrates the dangers of unsanitized user inputs in email generation.
- Real-world attackers could use such vulnerabilities for phishing or social engineering.
- Always sanitize user inputs and escape output properly.

---

**Disclaimer**: This guide is intended solely for educational purposes within controlled environments. Unauthorized testing or exploitation of vulnerabilities is illegal and may result in severe consequences. Always obtain explicit permission before testing applications you do not own.