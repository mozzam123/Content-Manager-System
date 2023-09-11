#  Content Management System (CMS)


## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [Contributing](#contributing)
- [License](#license)




## About

This Django project is a Content Management System (CMS) API that provides the backend functionality for managing and organizing content. The system caters to two types of users: admin and author. Admin users are pre-seeded into the system, while authors can register and log in using their email addresses.

## Getting Started

Explain how to get started with your project. What are the prerequisites, and how can someone install it?

### Prerequisites

List any software, libraries, or tools that users need to have installed before they can use your project. You can also include version requirements.

- Python 3.x
- Django 3.x
- Djangorestframework

## API Endpoints

The following API endpoints are available:

- **User Registration:** `register` (POST)
- **User Login:** `login` (POST)
- **List All Content:** `getcontent` (GET)
- **Create Content:** `create` (POST)
- **Delete Content:** `delete` (POST)
- **Search Content:** `search` (POST)
<br>

**User Registration**
<br>
**Body:**
{
    "username": "author2",
    "email": "author2@example.com",
    "full_name": "John Doe",
    "password": "Mozzam@123",
    "phone": "1234567890",
    "address": "123 Main St",
    "city": "Your City",
    "state": "Your State",
    "country": "Your Country",
    "pincode": "123456",
    "role": "author"
}


**User Login**
<br>
**Body:** 
{
  "email": "author1@example.com",
  "password": "Mozzam@123"
}


**List All Content**
<br>
**Body:**
{
    "username": "author2@example.com"
}

**Create Content**
<br>
**Body:**
{
    "username": "author2@example.com",
    "content": {
        "title": "third title",
        "body": "third body"
    }
}


**Delete Content**
<br>
**Body:** 
{
    "username": "author2@example.com",
    "content_id": "080f168f-fc16-4e34-b3ad-6ab6dfb29392"
}

**Search Content**
<br>
**Body:**
{
    "query": "author2 through api"
}

### Installation

Provide step-by-step instructions on how to install your project. You can use code blocks if necessary.

```bash
# Clone the repository
git clone https://github.com/mozzam123/Content-Manager-System.git

# Navigate to the project directory
cd cms_project

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows, use "venv\Scripts\activate"

# Install project dependencies
pip install -r requirements.txt ```






