from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("bigscience/mt0-small")

checkpoint = "bigscience/mt0-small"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)


# 3. Tokenize your input
input_text = " translate into ENGLISH: bonne année 2026 "
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs)
# 5. Decode the output
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded_output)



