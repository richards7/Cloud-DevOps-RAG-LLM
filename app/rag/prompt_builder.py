"""
Builds the final prompt sent to the LLM: retrieved context + user query.
"""


def build_prompt(query: str, retrieved_chunks: list) -> str:
    if retrieved_chunks:
        context = "\n\n".join(
            f"[Source: {c['source']}]\n{c['text']}" for c in retrieved_chunks
        )
    else:
        context = "(no relevant context found in the knowledge base)"

    prompt = f"""You are a helpful assistant that answers questions about \
cloud computing and DevOps, using the provided context.

Rules:
- Answer using ONLY the context below where possible.
- If the context doesn't contain enough information, say so clearly \
instead of guessing.
- Keep the answer concise and technically accurate.

Context:
{context}

Question: {query}

Answer:"""
    return prompt
