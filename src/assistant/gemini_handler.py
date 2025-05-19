import google.generativeai as genai
from pathlib import Path
import PIL.Image
import os # For environment variables, a good practice for API keys

# It's good practice to load API keys from environment variables
# Or pass it directly as you are doing.
# For this example, I'll keep your direct pass-through but add a note.
# API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiHandler:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key must be provided.")
        self.configure_gemini(api_key)
        
        # --- Model Names ---
        # Recommended general text model:
        self.text_model_name = 'gemini-1.5-pro-latest'
        # Recommended vision-capable model (gemini-1.5-pro-latest is also vision capable)
        # Or use 'gemini-1.5-flash-latest' for faster/cheaper vision tasks
        self.vision_model_name = 'gemini-1.5-pro-latest' # or 'gemini-1.5-flash-latest'

        try:
            # List available models (optional, for debugging)
            print("Available models for generateContent:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
            print("-" * 20)
            
            # Initialize the primary model (for text and potentially vision)
            self.model = genai.GenerativeModel(
                self.text_model_name,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
                # You can also add generation_config here, e.g.:
                # generation_config=genai.types.GenerationConfig(
                #     candidate_count=1,
                #     temperature=0.7,
                # )
            )
            
            # Initialize a separate model for vision if you want to use a different one (e.g., flash)
            # If self.text_model_name is already vision capable (like 1.5-pro), you can reuse self.model
            if self.text_model_name == self.vision_model_name:
                self.vision_model = self.model
            else:
                self.vision_model = genai.GenerativeModel(self.vision_model_name)

            # Initialize chat
            self.chat = self.model.start_chat(history=[])
            print(f"Successfully initialized model: {self.text_model_name}")
            if self.text_model_name != self.vision_model_name:
                 print(f"Successfully initialized vision model: {self.vision_model_name}")

        except Exception as e:
            print(f"Model initialization error: {str(e)}")
            # This error could be due to incorrect API key, model not available for the key,
            # network issues, or issues with the safety settings structure.
            raise

    def configure_gemini(self, api_key):
        genai.configure(api_key=api_key)

    # Note: The google-generativeai library's generate_content is synchronous.
    # If you use this in an asyncio application, it will block.
    # For true async, you'd typically use asyncio.to_thread or if the library offers an async version.
    async def get_response(self, prompt: str):
        try:
            # For single turn, use generate_content. For conversational, use self.chat.send_message
            response = await self.model.generate_content_async(prompt) # Using async version
            # response = self.model.generate_content(prompt) # Synchronous version
            return response.text
        except Exception as e:
            print(f"Generation error in get_response: {str(e)}")
            # Check response.prompt_feedback for blockages
            try:
                if response and response.prompt_feedback:
                    print(f"Prompt Feedback: {response.prompt_feedback}")
            except Exception: # response object might not exist if initial call failed
                pass
            return "I encountered an error during generation. Please try again."

    async def send_chat_message(self, message: str):
        try:
            response = await self.chat.send_message_async(message) # Using async version
            # response = self.chat.send_message(message) # Synchronous version
            return response.text
        except Exception as e:
            print(f"Chat error: {str(e)}")
            try:
                if response and response.prompt_feedback:
                    print(f"Prompt Feedback: {response.prompt_feedback}")
            except Exception:
                pass
            return "I encountered an error in chat. Please try again."

    async def generate_code(self, prompt: str):
        try:
            # Using async version
            response = await self.model.generate_content_async(
                f"Write Python code for the following task or concept: {prompt}. "
                "Return only the Python code block, with comments where necessary. "
                "Do not include any explanatory text before or after the code block."
            )
            # response = self.model.generate_content(...) # Synchronous version
            return response.text
        except Exception as e:
            print(f"Code generation error: {str(e)}")
            try:
                if response and response.prompt_feedback:
                    print(f"Prompt Feedback: {response.prompt_feedback}")
            except Exception:
                pass
            return "Error generating code. Please try again."

    async def analyze_image(self, image_path: str, prompt: str = "Describe this image in detail"):
        try:
            image_path_obj = Path(image_path)
            if not image_path_obj.exists():
                print(f"Image file not found: {image_path}")
                return "Error: Image file not found."

            image = PIL.Image.open(image_path_obj)
            
            # Use the initialized vision model
            # The content can be a list: [text_prompt, image_object, text_prompt_after_image (optional)]
            response = await self.vision_model.generate_content_async([prompt, image]) # Using async version
            # response = self.vision_model.generate_content([prompt, image]) # Synchronous version
            return response.text
        except FileNotFoundError:
            print(f"Image analysis error: File not found at {image_path}")
            return "Error analyzing image: File not found. Please check the file path."
        except Exception as e:
            print(f"Image analysis error: {str(e)}")
            try:
                if response and response.prompt_feedback:
                    print(f"Prompt Feedback: {response.prompt_feedback}")
            except Exception:
                pass
            return "Error analyzing image. Please ensure the file is a valid image."

# --- Example Usage (requires asyncio for the async methods) ---
import asyncio

async def main():
    # IMPORTANT: Replace "YOUR_API_KEY" with your actual Google AI Studio API key
    # It's better to use environment variables for API keys in production.
    api_key = "YOUR_API_KEY" 
    
    if api_key == "YOUR_API_KEY":
        print("Please replace 'YOUR_API_KEY' with your actual API key.")
        return

    try:
        handler = GeminiHandler(api_key=api_key)

        # Test text generation
        print("\n--- Testing Text Generation ---")
        text_prompt = "What is the Geminid meteor shower?"
        response_text = await handler.get_response(text_prompt)
        print(f"Prompt: {text_prompt}\nResponse: {response_text}")

        # Test chat
        print("\n--- Testing Chat ---")
        chat_response1 = await handler.send_chat_message("Hello! What can you do?")
        print(f"User: Hello! What can you do?\nGemini: {chat_response1}")
        chat_response2 = await handler.send_chat_message("Tell me a fun fact about space.")
        print(f"User: Tell me a fun fact about space.\nGemini: {chat_response2}")
        print(f"Chat History Inspect: {handler.chat.history}")


        # Test code generation
        print("\n--- Testing Code Generation ---")
        code_prompt = "a Python function that calculates the factorial of a number"
        generated_code = await handler.generate_code(code_prompt)
        print(f"Code Prompt: {code_prompt}\nGenerated Code:\n{generated_code}")

        # Test image analysis (Make sure you have an image file for this)
        print("\n--- Testing Image Analysis ---")
        # Create a dummy image for testing if you don't have one
        # For this to run, you need Pillow installed: pip install Pillow
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (200, 100), color = 'red')
            d = ImageDraw.Draw(img)
            d.text((10,10), "Hello World", fill=(255,255,0))
            dummy_image_path = "dummy_image.png"
            img.save(dummy_image_path)
            
            image_response = await handler.analyze_image(dummy_image_path, prompt="What do you see in this image?")
            print(f"Image analysis response for {dummy_image_path}:\n{image_response}")
            
            # Clean up dummy image
            if Path(dummy_image_path).exists():
                Path(dummy_image_path).unlink()

        except ImportError:
            print("Pillow library not found. Skipping dummy image creation for image analysis test.")
        except Exception as e:
            print(f"Error during image analysis test: {e}")

    except ValueError as ve: # Catch API key error specifically
        print(f"Configuration error: {ve}")
    except Exception as e:
        print(f"An error occurred in the main execution: {e}")

if __name__ == "__main__":
    # If your script is primarily async, run the main async function
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # This can happen if asyncio.run is called from an already running event loop (e.g. Jupyter)
        # In such cases, you might need 'await main()' if in an async cell.
        print(f"RuntimeError with asyncio: {e}. If in Jupyter, try 'await main()'.")