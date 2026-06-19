from backend.retriever import retrieve
from backend.rag_chain import generate_answer

query = input("Ask a question: ")

results = retrieve(query)

context = "\n".join(results["documents"][0])

answer = generate_answer(query, context)

print("\nAnswer:\n")
print(answer)