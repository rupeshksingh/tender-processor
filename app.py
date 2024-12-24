import streamlit as st
from pathlib import Path
import tempfile
import os
from excel import ExcelProcessor
from processors import TenderProcessor
from config import Settings

def initialize_session_state():
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'excel_processor' not in st.session_state:
        st.session_state.excel_processor = None
    if 'questions' not in st.session_state:
        st.session_state.questions = None
    if 'answers' not in st.session_state:
        st.session_state.answers = None
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = None
    if 'working_file_path' not in st.session_state:
        st.session_state.working_file_path = None

def reset_state():
    # Cleanup Excel processor if it exists
    if st.session_state.excel_processor:
        st.session_state.excel_processor.cleanup()
    
    # Reset all state variables
    st.session_state.step = 1
    st.session_state.excel_processor = None
    st.session_state.questions = None
    st.session_state.answers = None
    st.session_state.system_prompt = None
    st.session_state.working_file_path = None

def main():
    st.title("Advanced Tender Processor")
    
    initialize_session_state()
    settings = Settings()
    processor = TenderProcessor(settings)
    
    # Step 1: File Upload
    if st.session_state.step == 1:
        st.subheader("Step 1: Upload Excel File")
        uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx'])
        
        if uploaded_file is not None:
            try:
                # Save uploaded file to temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    original_path = tmp_file.name
                
                # Initialize Excel processor
                excel_processor = ExcelProcessor(original_path)
                working_path = excel_processor.create_working_copy()
                
                # Load Excel file
                sheet_names = excel_processor.load_excel()
                
                # Store in session state
                st.session_state.excel_processor = excel_processor
                st.session_state.working_file_path = working_path
                st.session_state.step = 2
                st.rerun()
            
            except Exception as e:
                st.error(f"Error processing file: {e}")
                reset_state()
    
    # Step 2: Sheet Selection
    elif st.session_state.step == 2:
        st.subheader("Step 2: Select Sheets")
        excel_processor = st.session_state.excel_processor
        
        col1, col2 = st.columns(2)
        with col1:
            instruction_sheet = st.selectbox(
                "Select Instruction Sheet",
                options=excel_processor.sheet_names
            )
        with col2:
            content_sheet = st.selectbox(
                "Select Content Sheet",
                options=excel_processor.sheet_names
            )
        
        if st.button("Process Selected Sheets"):
            try:
                with st.spinner("Processing sheets..."):
                    # Load selected sheets
                    instruction_df, content_df = excel_processor.load_sheets(
                        instruction_sheet,
                        content_sheet
                    )
                    
                    # Process data
                    st.session_state.questions = processor.extract_questions(content_df)
                    st.session_state.system_prompt = processor.process_instructions(instruction_df)
                    st.session_state.content_sheet = content_sheet
                    st.session_state.step = 3
                    st.rerun()
            except Exception as e:
                st.error(f"Error processing sheets: {e}")
    
    # Step 3: Review Questions and Configure Answer Column
    elif st.session_state.step == 3:
        st.subheader("Step 3: Review Questions")
        excel_processor = st.session_state.excel_processor
        
        for i, q in enumerate(st.session_state.questions, 1):
            with st.expander(f"Question {i}"):
                st.text(q.context)
        
        st.subheader("Configure Answer Column")
        has_answer_column = st.radio(
            "Does the content sheet have an existing answer column?",
            ("Yes", "No")
        )
        
        if has_answer_column == "Yes":
            answer_column = st.selectbox(
                "Select the answer column",
                options=excel_processor.content_df.columns
            )
        else:
            answer_column = "AI_Generated_Answer"
        
        start_row = st.number_input(
            "Enter the starting row number for answers",
            min_value=0,
            value=6
        )
        
        if st.button("Generate Answers"):
            with st.spinner("Generating answers..."):
                try:
                    answers = processor.generate_answers(
                        st.session_state.questions,
                        st.session_state.system_prompt
                    )
                    st.session_state.answers = answers
                    st.session_state.answer_column = answer_column
                    st.session_state.start_row = start_row
                    st.session_state.step = 4
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating answers: {e}")
    
    # Step 4: Review and Save
    elif st.session_state.step == 4:
        st.subheader("Step 4: Review and Save")
        excel_processor = st.session_state.excel_processor
        
        # Display answers for review
        st.write("Generated Answers:")
        for i, answer in enumerate(st.session_state.answers, 1):
            with st.expander(f"Answer {i}"):
                st.write(answer)
        
        if st.button("Save Changes"):
            with st.spinner("Saving changes..."):
                try:
                    # Update answers in the working copy
                    excel_processor.update_answers(
                        st.session_state.answers,
                        st.session_state.answer_column,
                        st.session_state.start_row
                    )
                    
                    # Save changes to the working file
                    excel_processor.save_changes(st.session_state.content_sheet)
                    
                    # Provide download link for the processed file
                    with open(st.session_state.working_file_path, 'rb') as file:
                        st.download_button(
                            label="Download Processed Excel",
                            data=file,
                            file_name=f"processed_tender.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                except Exception as e:
                    st.error(f"Error saving changes: {e}")
        
        if st.button("Start Over"):
            reset_state()
            st.rerun()
    
    # Sidebar progress indicator
    with st.sidebar:
        st.subheader("Progress")
        st.progress(st.session_state.step / 4)
        
        if st.session_state.step > 1 and st.button("Reset Process"):
            reset_state()
            st.rerun()

if __name__ == "__main__":
    main()