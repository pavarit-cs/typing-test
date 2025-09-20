import json
import langdetect

# โหลดไฟล์ JSON
with open(r'D:\projectPY\Typing-Test-CLI\src\typing_test\data\prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

valid_prompts = []
invalid_prompts = []

for prompt in data['prompts']:
    text = prompt.get('text', '')
    
    # ตรวจสอบความยาว
    if len(text) < 40:
        invalid_prompts.append(prompt)
        continue

    # ตรวจสอบภาษา
    try:
        lang = langdetect.detect(text)
        if lang == 'en':
            valid_prompts.append(prompt)
        else:
            invalid_prompts.append(prompt)
    except:
        invalid_prompts.append(prompt)

# บันทึกผลลัพธ์เป็นไฟล์ใหม่ (ถ้าต้องการ)
with open('valid_prompts.json', 'w', encoding='utf-8') as f:
    json.dump({"prompts": valid_prompts}, f, indent=2, ensure_ascii=False)

with open('invalid_prompts.json', 'w', encoding='utf-8') as f:
    json.dump({"prompts": invalid_prompts}, f, indent=2, ensure_ascii=False)

print(f"✅ Valid: {len(valid_prompts)}")
print(f"❌ Invalid: {len(invalid_prompts)}")
