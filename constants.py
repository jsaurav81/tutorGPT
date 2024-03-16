from langchain.llms import OpenAI
from langchain_openai import OpenAIEmbeddings
import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "89754e31-b3db-495d-8bd2-812a18b1b458"

# App modes
learn = "Learning mode :book:"
practice = "Practice mode :writing_hand:"
chat = "Chat mode :bulb:"

# Subject modes
DL = "Deep Learning"
MLTS = "ML in Time Series"
PR = "Pattern recognition"
VC = "Visual computing"

InProgress = "This mode is under progress. Stay Tuned!"

# LLM
model = OpenAI(model_name="gpt-3.5-turbo-instruct")
embeddings = OpenAIEmbeddings()

# Pinecone
index_name = "tutorgpt"

source_dir = "uploaded_files"
