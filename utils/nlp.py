import types
import re
from constants import *
from objects import Database, Context
from .general import timeit
from .fb_utils import send_message, send_products, send_attachment, get_user_info


@timeit
def prepare_sentences(body: str):
    sentences = re.split(pattern, body)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


@timeit
def get_speech(speech_type: str, _db=Database()):
    text = ""
    speech = _db.get_schema().speeches.find({"type": speech_type})
    try:
        for elem in speech:
            text = elem["messages"][0]
    except Exception as e:
        print(e.__str__())
    finally:
        return text


@timeit
def get_concept(word: str, _db=Database()):
    concept = _db.get_schema().dictionary.find_one({"words": str.lower(word)})
    return concept["concept"] if concept is not None else ""


@timeit
def get_sentence_context(variables, sentence: str, db=Database(), sender_id=""):
    cns = [get_concept(word=word, _db=db) for word in sentence.split()]

    while "" in cns:
        cns.remove("")

    if len(cns) > 0:
        return Context(sentence, cns, sender_id, get_user_info(variables, sender_id))
    else:
        return Context(sentence, None, sender_id, get_user_info(variables, sender_id))


@timeit
def generate_response(variables, context: Context, model, tokenizer, db=Database(), use_cuda=False):
    response = ""
    if context.concepts is not None:
        concepts = iter(context.concepts)

        while True:
            try:
                concept = next(concepts)
                if concept == "buy":
                    send_products(variables=variables, _sender_id=context.sender_id, _db=db)
                else:
                    cursor = db.get_schema().speeches.find_one({"type": concept})
                    if type(cursor) is not types.NoneType:
                        response += cursor["messages"][-1].format(context.user["first_name"]) + " "

            except StopIteration:
                break
        return response
    else:
        return generate_answer(context.sentence, model, tokenizer, use_cuda)


@timeit
def generate_answer(_prompt, _model, _tokenizer, use_cuda=False):
    # TODO: improve generator parameter configuration

    if use_cuda:
        t_prompt = _tokenizer(_prompt, return_tensors="pt").input_ids.cuda()
    else:
        t_prompt = _tokenizer(_prompt, return_tensors="pt").input_ids

    generated = _model.generate(
        t_prompt,
        do_sample=True,
        top_k=50,
        max_length=200,
        top_p=0.8,
        temperature=0.7)[0]

    return _tokenizer.decode(generated)
