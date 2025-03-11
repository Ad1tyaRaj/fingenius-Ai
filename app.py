from flask import Flask, render_template, request, jsonify
from team_app import web_agent, finance_agent, agent_team
from phi.model.groq import Groq
from dotenv import load_dotenv
import os
import re
import markdown

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

app = Flask(__name__)

def format_markdown_to_html(response_str):
    """Convert markdown response to HTML with special handling for tables"""
    # Convert response to string if it's not already
    if hasattr(response_str, 'content'):
        response_str = response_str.content
    
    # Process markdown to HTML
    html = markdown.markdown(response_str, extensions=['tables'])
    
    # Add Tailwind CSS classes to tables
    html = html.replace('<table>', '<table class="min-w-full divide-y divide-gray-200">')
    html = html.replace('<thead>', '<thead class="bg-gray-50">')
    html = html.replace('<th>', '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">')
    html = html.replace('<tbody>', '<tbody class="bg-white divide-y divide-gray-200">')
    html = html.replace('<tr>', '<tr class="hover:bg-gray-50">')
    html = html.replace('<td>', '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">')
    
    # Add classes to paragraphs
    html = html.replace('<p>', '<p class="mb-4 text-gray-700">')
    
    # Add classes to headings
    html = html.replace('<h1>', '<h1 class="text-2xl font-bold text-gray-800 mb-4">')
    html = html.replace('<h2>', '<h2 class="text-xl font-bold text-gray-800 mb-3">')
    html = html.replace('<h3>', '<h3 class="text-lg font-bold text-gray-800 mb-2">')
    
    return html

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        agent_type = data.get('agent_type', 'team')
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Please provide a prompt'}), 400
        
        # Select the appropriate agent based on the agent_type
        if agent_type == 'web':
            response = web_agent.run(prompt)
        elif agent_type == 'finance':
            # For finance agent, check if we have a ticker
            ticker = data.get('ticker', '')
            if ticker:
                prompt = f"{prompt} for {ticker}"
            response = finance_agent.run(prompt)
        else:  # Default to team agent
            response = agent_team.run(prompt)
        
        # Format the response
        formatted_response = format_markdown_to_html(response)
        
        return jsonify({
            'success': True,
            'response': formatted_response
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 