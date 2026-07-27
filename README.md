# Customer-Complaint-AI
# SmartComplaint AI

### AI-Powered Customer Complaint Classification and Management System

SmartComplaint AI is an intelligent web-based complaint management system designed to automate the process of analysing, classifying, prioritising, routing, and tracking customer complaints.

The system combines **Natural Language Processing (NLP)** and **BERT-based text classification** with a Flask web application and MySQL database. It provides dedicated interfaces for **customers, employees, and administrators**, creating an end-to-end complaint management workflow.

---

## Overview

Traditional complaint management systems often require employees to manually read complaints, identify their category, determine urgency, and forward them to the appropriate department.

SmartComplaint AI aims to automate this process.

A customer can submit a complaint in natural language, such as:

> "My payment was deducted twice, but my order is still showing unpaid."

The system processes the complaint and generates structured information such as:

```text
Relevance   : Relevant
Category    : Payment & Billing
Sentiment   : Negative
Priority    : High
Department  : Billing Department
Status      : Pending
```

The complaint can then be reviewed by administrators, assigned to an employee, updated during resolution, and tracked by the customer.

---

## Key Features

### Customer Module

- Customer registration and authentication
- Submit complaints in natural language
- Automatic complaint analysis
- Track submitted complaints
- View complaint status
- View predicted category
- View sentiment and priority
- View assigned department
- View administrator responses

### Employee Module

- Role-based employee authentication
- Department-based complaint access
- View assigned complaints
- Update complaint progress
- Manage complaint resolution

### Administrator Module

- Centralised complaint management dashboard
- View complaints from all customers
- Review AI-generated complaint analysis
- Assign complaints to employees
- Update complaint status
- Provide responses to customers
- Monitor complaint statistics
- View analytical charts and complaint trends

---

## AI and NLP Components

### Natural Language Processing

Customer complaints are generally submitted as **unstructured textual data**.

For example:

```text
money deducted but order still showing unpaid
```

and:

```text
I completed the transaction successfully,
but the system has not confirmed my payment.
```

Although the writing styles are different, both complaints may describe a similar issue.

Natural Language Processing allows SmartComplaint AI to process and analyse this textual information before classification.

---

## BERT-Based Complaint Classification

**BERT (Bidirectional Encoder Representations from Transformers)** is a transformer-based language model capable of representing words according to their surrounding context.

The complaint classification pipeline is designed as:

```text
Customer Complaint
        |
        v
Text Processing
        |
        v
BERT Tokenisation
        |
        v
BERT Model
        |
        v
Contextual Text Representation
        |
        v
Classification Layer
        |
        v
Predicted Complaint Category
```

Unlike a simple keyword-based classifier, a trained BERT classifier can learn contextual patterns within complaint text.

For example:

```text
"My card was charged but the order failed."
```

can be classified as:

```text
Payment & Billing
```

even when the user does not explicitly use the word "billing".

---

## Complaint Categories

SmartComplaint AI supports complaint classification across multiple customer-service domains.

| Category | Example |
|---|---|
| Payment & Billing | Payment deducted twice or incorrect billing |
| Refund & Cancellation | Refund pending or cancellation problem |
| Delivery & Shipping | Delayed or missing delivery |
| Product Quality | Damaged, defective, or incorrect product |
| Technical Issues | Website, application, or system errors |
| Account & Login | Login, password, or account access problems |
| Customer Service | Poor support or staff behaviour |
| Fraud & Security | Unauthorised transactions or suspicious activity |
| Other | Genuine complaints outside the primary categories |

---

## Relevance Detection

Not every text submitted through a complaint form is necessarily a customer complaint.

For example:

```text
Who won yesterday's cricket match?
```

should not be classified as a Payment, Delivery, or Technical complaint.

SmartComplaint AI can distinguish between:

```text
Relevant Complaint
        |
        v
Continue AI Analysis
```

and:

```text
Irrelevant Input
        |
        v
Out of Scope
```

This prevents unrelated input from being treated as a genuine customer complaint.

---

## Sentiment Analysis

The system analyses the emotional tone of customer complaints.

Possible sentiment outputs include:

```text
Positive
Neutral
Negative
```

Example:

```text
"The support employee was rude and did not solve my problem."

Sentiment: Negative
```

Sentiment information can help administrators understand the customer's level of dissatisfaction.

---

## Priority Detection

Complaints can also be assigned a priority level based on their content and urgency.

```text
Low
Medium
High
Urgent
```

For example:

```text
"Someone accessed my account and made an
unauthorised transaction."
```

may receive a higher priority than a minor profile-related issue.

---

## Intelligent Department Routing

After classification, the system can route complaints to an appropriate department.

```text
Payment & Billing
        |
        v
Billing Department


Delivery & Shipping
        |
        v
Logistics Department


Technical Issues
        |
        v
Technical Support


Fraud & Security
        |
        v
Security Department
```

This helps reduce manual complaint sorting and forwarding.

---

## System Architecture

```text
                         CUSTOMER
                            |
                            v
                   Submit Complaint
                            |
                            v
                   Relevance Detection
                            |
                 +----------+----------+
                 |                     |
             Relevant              Irrelevant
                 |                     |
                 v                     v
          NLP Text Processing      Out of Scope
                 |
                 v
        Complaint Classification
                 |
                 v
        +--------+---------+
        |        |         |
        v        v         v
     Category Sentiment Priority
        |
        v
     Department
       Routing
        |
        v
   ADMIN DASHBOARD
        |
        v
 Employee Assignment
        |
        v
 Complaint Processing
        |
        v
      Resolution
        |
        v
 Customer Tracking
```

---

## Technology Stack

| Area | Technologies |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Database | MySQL |
| NLP | Natural Language Processing |
| Language Model | BERT |
| Machine Learning | Text Classification |
| Frontend | HTML5, CSS3, JavaScript |
| Visualisation | Chart.js |
| Version Control | Git |
| Repository Hosting | GitHub |

---

## Project Structure

```text
Customer-Complaint-AI/
|
|-- dataset/
|   `-- complaints.csv
|
|-- model/
|   |-- saved_model/
|   |-- predict.py
|   `-- train_model.py
|
|-- static/
|   |-- css/
|   |   `-- style.css
|   |
|   |-- images/
|   |
|   `-- js/
|       `-- script.js
|
|-- templates/
|   |-- admin_dashboard.html
|   |-- customer_dashboard.html
|   |-- employee_dashboard.html
|   |-- index.html
|   |-- login.html
|   |-- register.html
|   |-- submit_complaint.html
|   `-- track_complaint.html
|
|-- app.py
|-- config.py
|-- create_admin.py
|-- init_db.py
|-- requirements.txt
|-- .gitignore
`-- README.md
```

---

## Application Workflow

### 1. Customer Registration

A new customer creates an account and signs in to the application.

### 2. Complaint Submission

The customer enters a complaint subject and detailed description.

### 3. AI Analysis

The submitted complaint is analysed to determine its:

- Relevance
- Category
- Confidence
- Sentiment
- Priority
- Department

### 4. Complaint Storage

Complaint information and AI-generated results are stored in the MySQL database.

### 5. Administrative Review

The administrator can review complaints and assign them to employees.

### 6. Employee Processing

Assigned employees can work on complaints and update their progress.

### 7. Complaint Tracking

Customers can monitor complaint status and administrator responses through the tracking interface.

---

## Dashboard Analytics

The administrator dashboard provides analytical information including:

- Total complaints
- Pending complaints
- Complaints in progress
- Resolved complaints
- Category distribution
- Complaint status distribution
- Priority distribution
- Customer sentiment distribution
- Department workload
- Complaint trends
- Resolution rate

These visualisations help administrators understand complaint patterns and operational workload.

---

## Screenshots

Add application screenshots inside:

```text
static/images/
```

Example:

```markdown
![Home Page](static/images/home.png)

![Customer Dashboard](static/images/customer-dashboard.png)

![Admin Dashboard](static/images/admin-dashboard.png)

![Complaint Tracking](static/images/track-complaint.png)
```

---

## Installation and Setup

### Prerequisites

Make sure the following are installed:

- Python 3.x
- MySQL
- Git
- pip

---

### 1. Clone the Repository

```bash
git clone https://github.com/Sneha9369/Customer-Complaint-AI.git
```

Move into the project directory:

```bash
cd Customer-Complaint-AI
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory.

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=customer_complaint_ai
DB_PORT=3306

SECRET_KEY=YOUR_SECRET_KEY
```

> Never commit the `.env` file or database credentials to a public repository.

---

### 5. Initialise the Database

Configure MySQL and run the database initialisation script used by the project.

```bash
python init_db.py
```

If required, create the administrator account:

```bash
python create_admin.py
```

---

### 6. Run the Application

```bash
python app.py
```

Open the local Flask application in your browser.

---

## Security Practices

The project includes basic application security practices such as:

- Password hashing
- Session-based authentication
- Role-based access control
- Environment variables for database credentials
- `.env` exclusion through `.gitignore`
- Separate customer, employee, and administrator access

---

## Future Enhancements

Possible future improvements include:

- Fine-tuning BERT on a larger real-world complaint dataset
- Multilingual complaint classification
- Hindi and Hinglish complaint support
- Automatic complaint summarisation
- AI-generated response suggestions
- Email notifications
- Real-time status notifications
- Complaint resolution-time prediction
- Advanced administrative analytics
- REST API support
- Cloud deployment
- Mobile application integration

---

## Project Objective

The primary objective of SmartComplaint AI is to reduce the manual effort involved in complaint management by using Artificial Intelligence to assist with:

**understanding → classification → prioritisation → routing → tracking → resolution**

This creates a more structured and efficient complaint-handling workflow.

---

## Author

**Sneha**

B.Tech Computer Science & Engineering  
Specialisation: Data Science

GitHub: [@Sneha9369](https://github.com/Sneha9369)

---

## Repository

[Customer-Complaint-AI](https://github.com/Sneha9369/Customer-Complaint-AI)

---

## Contributing

Suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.

---

## Support

If you find this project useful, consider giving the repository a star.
