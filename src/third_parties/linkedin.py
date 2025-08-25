def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    if mock:
        return {
            "name": "Pankaj Jaiswal",
            "location": "Noida",
            "company": "LinkedIn",
            "position": "Software Engineer",
            "summary": "I work at Fiserv as a Software Engineer.",
            "skills": [
                "Python",
                "Django",
                "SQL",
                "Redis",
                "MongoDB",
                "Docker",
                "Kubernetes",
            ],
            "education": [{}],
        }


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/pankajjaiswal/"
        ),
    )
