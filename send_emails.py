import requests
from bs4 import BeautifulSoup
import smtplib
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='/Users/barkha/HackSharks-devpost')


# User interests (sample data)
user_interests = []

# Function to fetch research papers from IEEE
def fetch_ieee_papers(interests):
    papers = []
    base_url = 'https://ieeexplore.ieee.org'
    search_url = base_url + '/search/searchresult.jsp'
    
    for interest in interests:
        params = {
            'newsearch': 'true',
            'queryText': interest,
            'highlight': True
        }
        
        response = requests.get(search_url, params=params)
        print(response)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for item in soup.find_all('li', class_='List-results-item'):
            title = item.find('h2', class_='title').text.strip()
            authors = [author.text.strip() for author in item.find_all('span', class_='authors')]
            paper = {
                'title': title,
                'authors': authors
            }
            papers.append(paper)
    
    return papers

# Function to fetch research papers from Springer
def fetch_springer_papers(interests):
    papers = []
    base_url = 'https://link.springer.com'
    search_url = base_url + '/search'
    
    for interest in interests:
        params = {
            'query': interest,
            'showAll': 'true'
        }
        
        response = requests.get(search_url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for item in soup.find_all('li', class_='content-item'):
            title = item.find('h2', class_='title').text.strip()
            authors = [author.text.strip() for author in item.find_all('span', class_='authors')]
            paper = {
                'title': title,
                'authors': authors
            }
            papers.append(paper)
    
    return papers

# Function to send an email with the research paper details
def send_email(recipient, papers):
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_password'
    sender = 'your_email@example.com'
    
    subject = 'Research Paper Recommendations'
    body = 'Here are some research papers based on your interests:\n\n'
    
    for paper in papers:
        body += f'Title: {paper["title"]}\n'
        body += f'Authors: {", ".join(paper["authors"])}\n\n'
    
    message = f'Subject: {subject}\n\n{body}'
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, recipient, message)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {str(e)}')
        

# Function to send weekly email recommendations
def send_weekly_email_recommendations():
    with open('user_data.json') as file:
        users = json.load(file)
    # Iterate through all registered users
    for user in users:
        print(user)
        ieee_papers = []
        # Fetch research papers based on user interests
        ieee_papers = fetch_ieee_papers(user['interests'])
        springer_papers = fetch_springer_papers(user['interests'])
        all_papers = ieee_papers + springer_papers
        for paper in papers:
            print(f'Title: {paper["title"]}\n')
            print(f'Authors: {", ".join(paper["authors"])}\n\n')
#         print(all_papers)

        # Send an email to the user with the research paper recommendations
#         send_email(user['email'], all_papers)

# Schedule the weekly email recommendations
# schedule.every().monday.at('9:00').do(send_weekly_email_recommendations)

if __name__ == '__main__':
#     # Start the Flask app
    app.run(debug=True, port=5001)
    send_weekly_email_recommendations()
#     # Start the scheduled task
#     while True:
#         schedule.run_pending()
#         time.sleep(1)