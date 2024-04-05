from constants import *
from app import *
from upload import get_doc_ans


# What function call to invoke, depending on input filters


def get_response(filters, prompt):
    (
        fromURL,
        fromDoc,
        mode,
        subject,
    ) = filters.values()
    if mode == chat:
        return retrieval_answer(prompt)
    elif fromURL or fromDoc:
        return get_transcript_ans(prompt)
    elif mode == learn and subject == PR:
        return get_from_pinecone(prompt, subcode="pr")
    elif mode == learn and subject == ME:
        return get_from_pinecone(prompt, subcode="me")
    else:
        return InProgress
