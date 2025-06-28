from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Google Generative AI model
# Make sure to set the GOOGLE_API_KEY in your environment or .env file
llm = GoogleGenerativeAI(model="gemini-2.0-flash")

linkedin_template = ChatPromptTemplate.from_messages([
    ("system", "Write only one formal LinkedIn post about the provided content. Make it professional and career-focused."),
    ("user", "{content}")])

facebook_template = ChatPromptTemplate.from_messages([
    ("system", "Write only one informal Facebook post about the provided content. Make it fun, personal, and friendly."),
    ("user", "{content}")])

twitter_template = ChatPromptTemplate.from_messages([
    ("system", "Write only one concise, engaging Twitter post about the provided content. Keep it under 280 characters."),
    ("user", "{content}")])

blog_template = ChatPromptTemplate.from_messages([
    ("system", "Write only one detailed blog post about the provided content. Be informative and provide context, challenges, and lessons learned."),
    ("user", "{content}")])

linkedin_chain = linkedin_template | llm
facebook_chain = facebook_template | llm
twitter_chain = twitter_template | llm
blog_chain = blog_template | llm

def generate_posts(content):
    """
    Generate posts for LinkedIn, Facebook, Twitter, and a blog based on the provided content.
    
    Args:
        content (str): The content to generate posts from.
    
    Returns:
        dict: A dictionary containing the generated posts for each platform.
    """
    linkedin_post = linkedin_chain.invoke({"content": content})
    facebook_post = facebook_chain.invoke({"content": content})
    twitter_post = twitter_chain.invoke({"content": content})
    blog_post = blog_chain.invoke({"content": content})

    return {
        "linkedin": linkedin_post,
        "facebook": facebook_post,
        "twitter":  twitter_post,
        "blog":     blog_post
    }


# Example usage
event_content = "I just completed a marathon and it was an amazing experience!"
posts = generate_posts(event_content)
print("Generated Posts:")
print("LinkedIn: \n\n", posts["linkedin"])
print("Facebook: \n\n", posts["facebook"])
print("Twitter: \n\n", posts["twitter"])
print("Blog: \n\n", posts["blog"])




