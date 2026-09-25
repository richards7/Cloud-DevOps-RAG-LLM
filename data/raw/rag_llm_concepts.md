# RAG and LLM Concepts

## Large Language Models (LLMs)
An LLM is trained on large amounts of text to predict the next token (word/sub-word
piece) given the preceding context. This simple objective, trained at massive scale,
produces models capable of answering questions, writing code, and reasoning about
text.

- **Token**: the basic unit an LLM processes — roughly a word or word-piece, not
  exactly a character or a whole word.
- **Context window**: the maximum number of tokens (input + output combined) a model
  can consider at once — exceeding it means older content gets dropped or the request
  fails, depending on the API.
- **Temperature**: controls output randomness — low temperature (near 0) gives more
  deterministic, focused answers; higher temperature gives more varied, creative ones.
- **Hallucination**: when an LLM generates plausible-sounding but factually incorrect
  or fabricated content — a core motivation for RAG, since grounding answers in real
  retrieved documents reduces (but doesn't eliminate) this.

## Prompt engineering
Crafting input prompts to get better, more reliable outputs from an LLM without
changing the model itself.
- **Zero-shot**: asking directly with no examples.
- **Few-shot**: providing a few examples of the desired input/output pattern in the
  prompt itself.
- **System prompt**: a special instruction (separate from the user's message) that
  sets the model's role/behavior/constraints for the whole conversation.
- **Chain-of-thought**: prompting the model to reason step by step before giving a
  final answer, often improving accuracy on multi-step problems.

## Retrieval-Augmented Generation (RAG)
### The problem RAG solves
An LLM's knowledge is frozen at training time and can't be updated without expensive
retraining/fine-tuning — and it has no access to private/proprietary data it wasn't
trained on. RAG lets a model answer using current, specific, or private information by
retrieving relevant documents at query time and including them in the prompt.

### The pipeline, step by step
1. **Chunking**: source documents are split into smaller pieces (paragraphs or
   fixed-size chunks with some overlap, so context isn't cut awkwardly).
2. **Embedding**: each chunk is converted into a vector (a list of numbers) that
   captures its semantic meaning, using an embedding model.
3. **Storage**: these vectors are stored in a vector database (Chroma, Pinecone,
   FAISS, Weaviate) that supports fast similarity search.
4. **Retrieval**: the user's query is also embedded, and the vector database returns
   the most similar (most relevant) chunks.
5. **Augmentation**: the retrieved chunks are inserted into the prompt as context.
6. **Generation**: the LLM generates an answer grounded in that context, rather than
   relying purely on its training data.

### RAG vs fine-tuning
- **RAG**: cheaper, faster to update (just re-index new documents), keeps the model's
  general capabilities intact, and can cite/attribute sources. Best for knowledge that
  changes often or is too large/private to bake into the model.
- **Fine-tuning**: retrains (part of) the model's weights on custom data — better for
  changing the model's style/behavior/format rather than injecting new factual
  knowledge, and is more expensive and slower to iterate on.

### Embeddings and similarity search
An embedding turns text into a point in a high-dimensional space, where semantically
similar text ends up close together. Similarity search (commonly cosine similarity)
finds the nearest points to a query's embedding — this is how "relevant" chunks are
found without exact keyword matching.

## AI Agents
An agent is an LLM given the ability to call tools/functions (search the web, query a
database, call an API) and decide, based on the task, which tools to use and in what
order — moving beyond a single prompt-response into multi-step, tool-using behavior.

## Common errors & fixes (RAG-specific)
- **Irrelevant chunks retrieved**: chunk size may be too large/small, or the embedding
  model doesn't suit the domain — tune chunk size/overlap and consider a
  domain-appropriate embedding model.
- **Answer ignores the retrieved context**: the prompt template may not instruct the
  model clearly enough to prioritize the provided context over its own knowledge.
- **Slow retrieval at scale**: vector search can degrade with very large collections —
  approximate nearest neighbor (ANN) indexes trade a little accuracy for much faster
  lookups.
- **Stale answers despite updating source docs**: the vector store wasn't re-indexed
  after the source documents changed — re-run ingestion after any document update.
