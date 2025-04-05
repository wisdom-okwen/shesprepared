from docx import Document

files_path = '/playpen-ssd/wokwen/projects/shesprepared/utility'
examples_file = 'example_responses_to_sensitive_prompts.docx'
mental_health_file = 'Mental_Health_and_Domestic_Violence_Resource_List'

def docx_to_txt(docx_path, txt_path):
    doc = Document(docx_path)
    
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    text = '\n'.join(full_text)
    
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


if __name__ == '__main__':
    docx_to_txt(f"{files_path}/{examples_file}", 'output.txt')
