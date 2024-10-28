from crewai import Crew
from typing import List
from pydantic import BaseModel
from newsfeed_crew.crew import BlogPostCrew

print("Kickoff the BlogPost Crew")
inputs = {
    'topic': 'Exploring the latest trends in AI across different industries as of October 2024',
    'goal': 'The goal of this blog post is to provide a comprehensive overview of the current state of artificial intelligence. It will delve into the latest trends impacting various industries, analyze significant advancements, and discuss potential future developments.' 
}
output = (
    BlogPostCrew()
        .crew()
        .kickoff(inputs=inputs))
        
# Print results
print("\n\n########################")
print("## Here is the result")
print("########################\n")
print("Title:\n")
print(output.title)
print("\nContent:\n")
print(output.content)