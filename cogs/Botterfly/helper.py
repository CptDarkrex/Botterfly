from transformers import AutoTokenizer, AutoModelForCausalLM

# Setup of the bot
pygmalion = "PygmalionAI/pygmalion-6b"
tokenizer = AutoTokenizer.from_pretrained(pygmalion)
model = AutoModelForCausalLM.from_pretrained(pygmalion)


class Botterfly_Core:

    def bot_call(self, prompt: str) -> str:
        # Setting up the input
        inputs = tokenizer([prompt], return_tensors="pt")

        # Implementation of the above setup
        reply_ids = model.generate(**inputs, max_new_tokens=5)  # return_dict_in_generate=True, output_scores=True
        outputs = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
        print(outputs)

        return outputs
