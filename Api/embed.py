from transformers import AutoTokenizer
from transformers import AutoModel
import os
from dotenv import load_dotenv
load_dotenv()
tokenizer = AutoTokenizer.from_pretrained("mixedbread-ai/mxbai-embed-large-v1",use_auth_token=os.getenv("HUGGINGFACE_TOKEN"))
model = AutoModel.from_pretrained("mixedbread-ai/mxbai-embed-large-v1").cuda()
import torch 
def tokenize_and_generate_embeddings(text, tokenizer, model,max_tokens=500):
    # Tokenize the text into token IDs
    tokens = tokenizer.encode(text, add_special_tokens=True)
    
    # Split into chunks of max_tokens (500 by default)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    
    # Generate embeddings for each chunk
    embeddings = []
    with torch.no_grad():
        for chunk in chunks:
            # Convert the chunk to a tensor
            input_ids = torch.tensor([chunk]).cuda()
            # Get the embeddings from the model
            outputs = model(input_ids)
            embeddings.append([outputs.last_hidden_state.mean(dim=1),tokenizer.decode(chunk)])   # Use mean of all token embeddings    
    return embeddings