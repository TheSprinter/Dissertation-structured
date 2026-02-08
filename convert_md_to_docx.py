"""
Convert Markdown file to Microsoft Word Document (DOCX)
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import re
import os

def parse_markdown_to_docx(md_file, output_file):
    """Convert markdown file to Word document with formatting"""
    
    # Create a new Document
    doc = Document()
    
    # Set document margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    print(f"Reading markdown file: {md_file}")
    
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Processing {len(lines)} lines...")
    
    i = 0
    in_code_block = False
    code_block_content = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Handle code blocks
        if line.startswith('```'):
            if in_code_block:
                # End of code block
                code_text = '\n'.join(code_block_content)
                p = doc.add_paragraph(code_text)
                p.style = 'Normal'
                # Make code monospace and gray background
                for run in p.runs:
                    run.font.name = 'Courier New'
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0, 0, 0)
                # Add spacing
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.left_indent = Inches(0.5)
                
                in_code_block = False
                code_block_content = []
            else:
                # Start of code block
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue
        
        # Skip empty lines
        if not line.strip():
            doc.add_paragraph()
            i += 1
            continue
        
        # Handle headings
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            heading_text = line.lstrip('#').strip()
            
            if level == 1:
                # Title
                p = doc.add_heading(heading_text, level=0)
                p.runs[0].font.size = Pt(24)
                p.runs[0].font.color.rgb = RGBColor(0, 51, 102)  # Dark blue
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif level == 2:
                # Main section
                p = doc.add_heading(heading_text, level=1)
                p.runs[0].font.size = Pt(18)
                p.runs[0].font.color.rgb = RGBColor(31, 78, 120)  # Blue
            elif level == 3:
                # Subsection
                p = doc.add_heading(heading_text, level=2)
                p.runs[0].font.size = Pt(14)
                p.runs[0].font.color.rgb = RGBColor(59, 130, 246)  # Lighter blue
            else:
                # Smaller heading
                p = doc.add_heading(heading_text, level=3)
                p.runs[0].font.size = Pt(12)
                p.runs[0].font.bold = True
            
            i += 1
            continue
        
        # Handle horizontal rules
        if line.strip() in ['---', '___', '***']:
            doc.add_paragraph('_' * 80)
            i += 1
            continue
        
        # Handle bullet lists
        if line.strip().startswith(('- ', '* ', '+ ')):
            text = line.strip()[2:]
            text = format_inline_markdown(text)
            p = doc.add_paragraph(text, style='List Bullet')
            apply_inline_formatting(p)
            i += 1
            continue
        
        # Handle numbered lists
        if re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            text = format_inline_markdown(text)
            p = doc.add_paragraph(text, style='List Number')
            apply_inline_formatting(p)
            i += 1
            continue
        
        # Handle blockquotes or special formatting
        if line.strip().startswith('>'):
            text = line.strip()[1:].strip()
            p = doc.add_paragraph(text)
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.right_indent = Inches(0.5)
            for run in p.runs:
                run.italic = True
                run.font.color.rgb = RGBColor(100, 100, 100)
            i += 1
            continue
        
        # Regular paragraph
        text = format_inline_markdown(line.strip())
        p = doc.add_paragraph(text)
        apply_inline_formatting(p)
        
        i += 1
    
    # Save the document
    print(f"Saving Word document: {output_file}")
    doc.save(output_file)
    print(f"✓ Successfully created: {output_file}")
    
    # Get file size
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    print(f"  File size: {file_size_mb:.2f} MB")

def format_inline_markdown(text):
    """Format inline markdown elements like bold, italic, code"""
    # Preserve backticks for code
    text = re.sub(r'`([^`]+)`', r'⟪CODE⟫\1⟪/CODE⟫', text)
    
    # Bold (**text** or __text__)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'⟪BOLD⟫\1⟪/BOLD⟫', text)
    text = re.sub(r'__([^_]+)__', r'⟪BOLD⟫\1⟪/BOLD⟫', text)
    
    # Italic (*text* or _text_)
    text = re.sub(r'\*([^\*]+)\*', r'⟪ITALIC⟫\1⟪/ITALIC⟫', text)
    text = re.sub(r'_([^_]+)_', r'⟪ITALIC⟫\1⟪/ITALIC⟫', text)
    
    return text

def apply_inline_formatting(paragraph):
    """Apply formatting to inline elements"""
    text = paragraph.text
    paragraph.clear()
    
    # Split by formatting markers
    parts = re.split(r'(⟪BOLD⟫|⟪/BOLD⟫|⟪ITALIC⟫|⟪/ITALIC⟫|⟪CODE⟫|⟪/CODE⟫)', text)
    
    bold = False
    italic = False
    code = False
    
    for part in parts:
        if part == '⟪BOLD⟫':
            bold = True
        elif part == '⟪/BOLD⟫':
            bold = False
        elif part == '⟪ITALIC⟫':
            italic = True
        elif part == '⟪/ITALIC⟫':
            italic = False
        elif part == '⟪CODE⟫':
            code = True
        elif part == '⟪/CODE⟫':
            code = False
        elif part:
            run = paragraph.add_run(part)
            if bold:
                run.bold = True
            if italic:
                run.italic = True
            if code:
                run.font.name = 'Courier New'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(200, 0, 0)  # Red for inline code

def main():
    # Input and output files
    input_file = 'VIVA_QUESTIONS_ANSWERS.md'
    output_file = 'VIVA_QUESTIONS_ANSWERS_v2.1.docx'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    print("=" * 60)
    print("MARKDOWN TO WORD CONVERTER")
    print("=" * 60)
    
    try:
        parse_markdown_to_docx(input_file, output_file)
        print("=" * 60)
        print("✓ CONVERSION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
