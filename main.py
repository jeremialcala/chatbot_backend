import keyboard
import sys
import llama
from time import sleep
from constants import *
from utils import (timeit, load_env_variables, load_credentials, create_session_session, get_queue,
                   get_sentence_context, send_message, prepare_sentences, generate_response)
from objects import Database

arg_names = ["--file-name", "--use-cuda"]


def get_help():
    """
    This get messages from a SQS, process it using a dictionary for common and known concepts
    for the messages not in the database will complete it with transformers using llama models.

    Args:
        --file-name (str): This is a file with all environment variables for the project.
        --use-cuda: Enables the use of cuda GPU, needs a configuration for pytorch + CUDA.
    Returns:

    """

@timeit
def process_messages(variables, queue, _db, use_cuda=False):

    model = "llama-7b-hf"
    print("creating tokenizer...")
    tokenizer = llama.LLaMATokenizer.from_pretrained(model)
    print("creating model...")
    model = llama.LLaMAForCausalLM.from_pretrained(model)
    if use_cuda:
        model.to("cuda")

    while True:
        for message in queue.receive_messages(MessageAttributeNames=[sender]):
            sender_id = message.message_attributes.get(sender).get(StringValue)
            print(f"This is a new message: '{message.body}' from {sender_id}")
            sentences = prepare_sentences(message.body)

            [send_message(
                variables=variables,
                recipient_id=sender_id,
                message_text=generate_response(
                    variables=variables,
                    model=model,
                    tokenizer=tokenizer,
                    context=get_sentence_context(variables=variables, db=_db, sentence=sentence, sender_id=sender_id),
                    db=_db,
                    use_cuda=use_cuda)

            ) for sentence in sentences]

            message.delete()
            sleep(5)

        if keyboard.is_pressed('q'):
            exit(0)


if __name__ == '__main__':

    if "--help" in sys.argv or len(sys.argv) == 1:
        print(get_help.__doc__)
        sys.exit(0)

    arg_name = [arg for arg in sys.argv if "--" in arg]

    sender = "Sender"
    StringValue = "StringValue"
    use_cuda = False
    if PARAM_FILE_NAME not in sys.argv:
        exit(0)

    if "--use-cuda" in sys.argv:
        use_cuda = True

    variables = load_env_variables(sys.argv[sys.argv.index(PARAM_FILE_NAME) + 1])
    _db = Database(conn=variables[MONGO], schema=variables[SCHEMA])
    session = create_session_session(load_credentials())
    queue = get_queue(session.resource("sqs"), chat_msg)
    process_messages(variables=variables, queue=queue, _db=_db, use_cuda=use_cuda)

