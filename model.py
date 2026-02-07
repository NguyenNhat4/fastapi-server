from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 1. Load the translation model and tokenizer
model_name = "vinai/vinai-translate-vi2en"
tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang="vi_VN")
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 2. Your Vietnamese input (Word segmentation is still recommended!)
vietnamese_text = "Chúng_tôi là những nghiên_cứu_viên ."

# 3. Tokenize and Generate
input_ids = tokenizer(vietnamese_text, return_tensors="pt")

output_ids = model.generate(
    **input_ids, 
    decoder_start_token_id=tokenizer.lang_code_to_id["en_XX"],
    max_length=100
)

# 4. Decode the result
english_text = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
print(english_text[0]) 
# Expected Output: "We are researchers."