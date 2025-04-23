import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI



app = FastAPI();


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an AI that answers questons that imployers ask about a job candadit named mags. Your job is to answer the questions honestly but try to show th ecandadits best qualitys. Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
@app.get("/{question}")
def get_res(question):
    # Create CLI.
    # parser = argparse.ArgumentParser()
    # parser.add_argument("query_text", type=str, help="The query text.")
    # args = parser.parse_args()
    query_text = question # args.query_text
    print(question)
    # Prepare the DB.
    # try: 
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0: # or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI()
    response_text = model.predict(prompt)



    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return {"res": response_text}
    # } except () {
    #     return {"res": "server error"}
    # }
    #
# if __name__ == "__main__":
#     main()

