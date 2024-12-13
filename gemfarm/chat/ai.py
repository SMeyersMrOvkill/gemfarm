import google.generativeai as genai
from flask import current_app
import logging

logger = logging.getLogger(__name__)

# Initialize Gemini model
def init_ai():
    api_key = current_app.config['GOOGLE_API_KEY']
    if not api_key:
        logger.error("GOOGLE_API_KEY not found in environment variables")
        raise ValueError("GOOGLE_API_KEY is required")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        logger.info("Gemini API configured successfully")
        return model, chat
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {str(e)}")
        raise

# Movement function declarations
move_tool = genai.types.Tool(
    function_declarations=[
        genai.types.FunctionDeclaration(
            name="move",
            description="Move the character in a given direction.",
            parameters={
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "description": "The direction to move (north, south, east, or west)",
                        "enum": ["north", "south", "east", "west"]
                    }
                },
                "required": ["direction"]
            }
        )
    ]
)

def get_ai_response(user_input):
    """Generate AI response using Gemini"""
    model, chat = init_ai()
    
    game_context = """
    You are an AI controlling a character in a 2D game, analyzing messages to determine intent and provide appropriate responses.
    
    For each message, first determine the intent and mark it with @intent at the start of a line:
    - If the user wants to move, respond with "@intent move;" followed by your response
    - If the user wants to chat or ask questions, respond with "@intent chat;" followed by your response
    
    When moving:
    - Use cardinal directions (north, south, east, west)
    - Convert user input like "right"->east, "left"->west, "up"->north, "down"->south
    - Use the move function for actual movement
    - Always provide a conversational response along with movement
    
    Examples:
    User: "go right"
    Response: 
    @intent move;
    I'll head east! *moves purposefully*
    
    User: "hello there!"
    Response:
    @intent chat;
    Hey! Nice to meet you! I'm ready for some adventure!
    
    Remember:
    - Always start your response with an @intent line
    - Keep responses brief and in character
    - Use natural, conversational language
    - For movement, always include both the movement command AND a response
    """

    # Include conversation history in the prompt
    history_prompt = "\nPrevious messages:\n" + "\n".join(f"User: {msg}" for msg in chat.history) if chat.history else ""
    full_prompt = f"{game_context}{history_prompt}\n\nNew message: {user_input}\n\nYour response:"
    
    try:
        response = chat.send_message(
            full_prompt,
            tools=[move_tool],
            generation_config={"temperature": 0.7}
        )
        
        # Process the response to extract intent and content
        text_content = []
        movement = None
        intent = None
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                # Handle text content
                if hasattr(part, 'text') and part.text:
                    lines = part.text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('@intent'):
                            intent = line.replace('@intent', '').strip().rstrip(';').strip()
                        elif line:  # Add non-empty lines that aren't intent markers
                            text_content.append(line)
                
                # Handle function calls for movement
                if hasattr(part, 'function_call'):
                    function_call = part.function_call
                    if function_call.name == "move":
                        try:
                            movement = function_call.args.get("direction")
                        except Exception as e:
                            logger.error(f"Error extracting direction from function call: {e}")
        
        # If no movement was explicitly specified via function call but intent is move,
        # try to extract direction from the text
        if intent == 'move' and not movement:
            directions = {
                'north': 'north', 'south': 'south', 'east': 'east', 'west': 'west',
                'up': 'north', 'down': 'south', 'right': 'east', 'left': 'west'
            }
            
            message_text = ' '.join(text_content)
            for word, direction in directions.items():
                if word in message_text.lower():
                    movement = direction
                    break

        # Generate the chat message
        # Remove any remaining @intent lines and empty lines
        text_content = [line for line in text_content if line and not line.startswith('@intent')]
        message = ' '.join(text_content) if text_content else "I'm moving!"
        
        # If no movement was explicitly specified via function call but intent is move,
        # try to extract direction from the text
        if intent == 'move' and not movement:
            directions = {
                'north': 'north', 'south': 'south', 'east': 'east', 'west': 'west',
                'up': 'north', 'down': 'south', 'right': 'east', 'left': 'west'
            }
            
            for word, direction in directions.items():
                if word in message.lower():
                    movement = direction
                    break
        
        # Update chat history based on intent
        if intent == 'move' and movement:
            chat.history.append(f"// LAST ACTION WAS MOVE\n\n{message}")
        else:
            chat.history.append(message)
            
        return {
            'message': message.strip(),
            'movement': movement,
            'intent': intent,
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f'Error processing Gemini response: {str(e)}')
        raise
