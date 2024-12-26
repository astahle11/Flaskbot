import google.generativeai as genai

genai.configure(api_key="AIzaSyDHx2KDfDXuZB6hbdIi5ti0bShNoCgkXtw")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("How do I make this wait until a request has been received console.print(f'\n> BOT: {response.text}')")
print(response.text)