import os
import warnings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from operator import itemgetter

os.environ['OPENAI_API_KEY'] = ''
os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGCHAIN_API_KEY'] = ''
os.environ[' LANGCHAIN_PROJECT'] = "book-chapter-6"
warnings.filterwarnings('ignore')

llm = ChatOpenAI(temperature=0.0,openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4-1106-preview")

#you are a music fan chatbot

memory = ConversationBufferMemory(return_messages=True)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an events chatbot who likes live music, ask your user for their name and some examples of bands they want to go and see"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

chain_with_memory = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | llm
)

inputs = {"input": "hi"}
response = chain_with_memory.invoke(inputs)


memory.save_context(inputs, {"output": response.content})

inputs = {"input": "My name is Adrian and I like the high flying birds"}
response = chain_with_memory.invoke(inputs)


memory.save_context(inputs, {"output": response.content})

inputs = {"input": "I'm looking for gigs in London this summer"}
response = chain_with_memory.invoke(inputs)


memory.save_context(inputs, {"output": response.content})

memory.load_memory_variables({})