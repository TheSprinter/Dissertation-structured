# WILP Report Generator - Update Summary

## Overview
The `generate_report.py` script has been successfully updated to comply with **BITS Pilani WILP (Work Integrated Learning Programme) Guidelines for Project Report Preparation**.

## Changes Implemented

### 1. **Cover Page (NEW)**
- Added as per WILP Appendix-A format
- Includes:
  - Report title in capital letters
  - Student name and ID number
  - Organization name and location
  - University name (BITS Pilani)
  - Submission date

### 2. **Title Page (UPDATED)**
- Reformatted to match WILP Appendix-B format
- Now includes:
  - Project title
  - Student details (Name, ID, Discipline)
  - Course fulfillment statement ("WILP Dissertation Course")
  - Organization details
  - University name
  - Submission date

### 3. **Acknowledgements (NEW)**
- Added comprehensive acknowledgements section
- Follows recommended order:
  - Head of organization
  - Supervisor and Additional Examiner
  - Professional Expert/Project In-charge
  - Faculty mentor from BITS Pilani
  - Colleagues and team members
  - Family and friends
  - BITS Pilani WILP program
- Includes signature line

### 4. **Abstract (UPDATED)**
- Reformatted to match WILP Appendix-C format
- Now includes all required fields:
  - Organization name and location
  - Project duration
  - Project title
  - Student ID and name
  - Supervisor and Additional Examiner details
  - Faculty mentor name
  - **Key Words** (9 relevant keywords)
  - **Project Areas** (5 areas: ML, AI, Data Science, FinTech, Cybersecurity)
  - Abstract text (condensed to ~200 words as per guidelines)
  - Signature fields for student and supervisor

### 5. **Glossary (NEW)**
- Added comprehensive glossary section
- Includes 23 technical terms with definitions
- Covers AI/ML, fraud detection, and technical terminology
- Alphabetically organized with bold terms

### 6. **Document Formatting (UPDATED)**
- **Page Size**: Changed to 9" x 11" (Quarto size) as per WILP guidelines
- **Margins**: Set to 1" on all four sides
- **Font**: Times New Roman, 12pt
- **Spacing**: Double spacing throughout
- **Page Numbering**: Structured for:
  - Roman numerals (i, ii, iii) for preliminary pages
  - Arabic numerals (1, 2, 3) from Introduction onwards

### 7. **Report Structure (UPDATED)**
Now follows proper WILP order:
1. Cover Page
2. Title Page
3. Acknowledgements
4. Abstract Sheet
5. Table of Contents
6. Introduction (Chapter 1)
7. Literature Review (Chapter 2)
8. System Design and Architecture (Chapter 3)
9. Implementation (Chapter 4)
10. Algorithms and Methodology (Chapter 5)
11. Results and Analysis (Chapter 6)
12. Conclusion and Future Work (Chapter 7)
13. References
14. Appendices
15. Glossary

## WILP Compliance Checklist

✅ Cover Page (Appendix-A format)
✅ Title Page (Appendix-B format)
✅ Acknowledgements
✅ Abstract Sheet (Appendix-C format)
✅ Table of Contents with proper numbering
✅ Introduction with required subsections
✅ Main Text with proper chapters
✅ Conclusions and Recommendations
✅ References (properly cited)
✅ Appendices with supplementary material
✅ Glossary of technical terms
✅ Page size: 9" x 11" (Quarto)
✅ Margins: 1" on all sides
✅ Font: Times New Roman, 12pt
✅ Double spacing

## Generated File
**Filename**: `WILP_Dissertation_Report_Simit_Das_2023AA05807_20260201.docx`

## Manual Updates Required

Before submission, please update the following placeholders in the generated document:

### Required Information:
1. **Organization Details**
   - Organization name
   - Location (City, State)
   - Project duration (Start date - End date)

2. **Personnel Details**
   - Supervisor name and designation
   - Additional Examiner name and designation
   - Faculty Mentor name

3. **Signatures**
   - Sign the Abstract page
   - Get supervisor's signature on Abstract page
   - Scan only these signature pages as images

### Pre-Submission Requirements:

1. **Convert to PDF**
   - Save the Word document as PDF format
   - File size must be ≤ 10 MB
   - Page count must be ≤ 400 pages

2. **Plagiarism Check**
   - Run through plagiarism detection tool
   - Ensure originality of content

3. **Text Format Verification**
   - Copy entire document content to Notepad
   - Verify that text pastes successfully (except scanned signatures)
   - Only signature pages should be images
   - All other content must be text

4. **Page Numbering** (Manual adjustment in Word)
   - Preliminary pages (Cover to TOC): Roman numerals (i, ii, iii, iv, v)
   - Main content (Introduction onwards): Arabic numerals (1, 2, 3...)

## Important Notes

### From WILP Guidelines:
- Report is a **formal document** requiring careful presentation
- Written in **impartial and objective** manner
- Should be **easy to understand** for any reader
- All illustrations must have numbers and titles
- References should be properly formatted
- Maintain **parallel grammatical construction** in headings

### Best Practices:
- Review all content for accuracy
- Ensure consistent formatting throughout
- Check all cross-references
- Verify all tables, figures, and charts are numbered
- Proofread for spelling and grammar errors
- Have supervisor review before final submission

## Technical Details

### Dependencies Used:
- `python-docx` (1.2.0) - For Word document generation
- Python 3.12.7

### How to Regenerate:
```bash
# Navigate to project directory
cd C:\Project\Dissertation-structured

# Run the report generator
python generate_report.py
```

### Customization:
To customize the report, edit the following functions in `generate_report.py`:
- `create_cover_page()` - Cover page content
- `create_title_page()` - Title page details
- `create_acknowledgements()` - Acknowledgement text
- `create_abstract()` - Abstract content
- Individual chapter functions for content updates

## References

**WILP Guidelines Document**: 
`C:\Project\Dissertation-structured\Guidelines for preparation of a WILP Project Report-1.doc`

**Key Guidelines Applied**:
- Section 1.1: Introduction to report writing
- Section 1.2: Appearance (size, margins, spacing)
- Section 1.3: Elements (inner matter structure)
- Appendix-A: Cover page format
- Appendix-B: Title page format
- Appendix-C: Abstract sheet format

---

**Generated**: February 1, 2026
**Student**: Simit Das (2023AA05807)
**Program**: BITS Pilani WILP - M.Tech Software Engineering
