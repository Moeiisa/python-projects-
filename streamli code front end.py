import streamlit as st
import random

# Set page configuration
st.set_page_config(
    page_title="Interactive Quiz App",
    page_icon="🧠",
    layout="wide",
)

# Custom CSS for styling (with enhanced visibility for options)
def apply_custom_style():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f8ff;
        color: #2c3e50;
    }
    h1, h2, h3 {
        color: #3498db;
        font-weight: bold;
    }
    .quiz-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stButton button {
        border-radius: 20px;
        font-weight: bold;
    }
    /* Highlight the answer options section */
    .answer-section {
        background-color: #eaf4ff;
        padding: 20px;
        border-radius: 8px;
        border-left: 8px solid #3498db;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    /* Make radio buttons more prominent */
    .stRadio > div {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .st-emotion-cache-q8sbsg p {
        font-size: 20px;
        font-weight: 600;
        color: #2c3e50;
    }
    /* Enhance radio button visibility */
    .st-emotion-cache-1qg05tj {
        transform: scale(1.5);
    }
    /* Add custom style for the option letters */
    div.row-widget.stRadio > div {
        display: flex;
        gap: 15px;
    }
    div.row-widget.stRadio > div label {
        background-color: #3498db;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 18px;
        min-width: 80px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        border: 2px solid transparent;
        transition: all 0.3s;
    }
    div.row-widget.stRadio > div label:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }
    div.row-widget.stRadio > div input:checked + label {
        background-color: #2ecc71;
        border: 2px solid #27ae60;
        transform: scale(1.1);
    }
    /* Make option text appear as separate buttons */
    .option-button {
        background-color: #f8f9fa;
        border: 2px solid #dcdcdc;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 16px;
        display: block;
        position: relative;
        transition: all 0.3s;
    }
    .option-button:hover {
        background-color: #e9ecef;
        border-color: #bdc3c7;
        transform: translateX(5px);
    }
    .option-button strong {
        color: #3498db;
        font-size: 17px;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# Load questions and answers
@st.cache_data
def load_questions_answers():
    try:
        with open("quize.txt", "r", encoding="utf-8") as q_file:
            questions = q_file.read().strip().split("\n\n")
        with open("answers.txt", "r", encoding="utf-8") as a_file:
            answers = a_file.read().strip().split("\n")
        return questions, answers
    except FileNotFoundError:
        st.error("⚠ Quiz files not found!")
        # Sample data for demo
        sample_questions = [
            "What is the output of print(2 + 2)?\nA. 2\nB. 4\nC. 22\nD. Error",
            "Which of these is NOT a Python data type?\nA. Integer\nB. Boolean\nC. Character\nD. Float",
            "What does the 'append()' method do in Python?\nA. Adds an element to the end of a list\nB. Removes an element from a list\nC. Sorts a list\nD. Reverses a list"
        ]
        sample_answers = ["B", "C", "A"]
        return sample_questions, sample_answers

def start_quiz():
    questions, answers = load_questions_answers()
    if not questions:
        return
    
    # Shuffle questions
    combined = list(zip(questions, answers))
    random.shuffle(combined)
    shuffled_questions, shuffled_answers = zip(*combined)
    
    # Set up session state
    st.session_state.update({
        "questions": shuffled_questions,
        "answers": shuffled_answers,
        "index": 0,
        "score": 0,
        "completed": False,
        "feedback": None,
        "user_answers": {i: None for i in range(len(shuffled_questions))},
        "answered_questions": set()
    })
    st.rerun()

def jump_to_question(question_index):
    st.session_state["index"] = question_index
    st.session_state["feedback"] = None
    st.rerun()

def show_question():
    questions = st.session_state["questions"]
    answers = st.session_state["answers"]
    index = st.session_state["index"]
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.python.org/static/community_logos/python-logo-generic.svg", width=200)
        st.title("📋 Question Navigator")
        total_questions = len(questions)
        
        # Question list
        cols = st.columns(4)
        for i in range(total_questions):
            col_index = i % 4
            with cols[col_index]:
                if i in st.session_state["answered_questions"]:
                    is_correct = st.session_state["user_answers"][i] == answers[i]
                    btn_type = "primary" if is_correct else "secondary"
                    emoji = "✅" if is_correct else "❌"
                else:
                    btn_type = "secondary"
                    emoji = "⬜"
                if st.button(f"{emoji} {i+1}", key=f"nav_{i}", use_container_width=True, type=btn_type):
                    jump_to_question(i)
        
        # Progress
        st.markdown("### Quiz Progress")
        answered_count = len(st.session_state["answered_questions"])
        st.progress(answered_count / total_questions)
        st.write(f"Answered: *{answered_count}/{total_questions}*")
        
        if st.button("🏁 Finish Quiz", use_container_width=True, type="primary"):
            st.session_state["completed"] = True
            st.rerun()

    # Main content
    st.title("🧠 Python Quiz Challenge")
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.subheader(f"Question {index + 1} of {len(questions)}")
    
    # Question and options
    question_text = questions[index].split("\n")[0]
    options = questions[index].split("\n")[1:]
    st.markdown(f"### {question_text}")
    
    # Make the answer selection more visible with a highlighted section
    st.markdown('<div class="answer-section">', unsafe_allow_html=True)
    st.markdown("### 👉 Select Your Answer:")
    
    previous_answer = st.session_state["user_answers"].get(index)
    user_answer = st.radio(
        "",  # Removed label since we added it in markdown above
        ["A", "B", "C", "D"],
        index=["A", "B", "C", "D"].index(previous_answer) if previous_answer else None,
        key=f"q{index}",
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feedback
    if st.session_state.get("feedback"):
        if st.session_state["feedback"]["correct"]:
            st.success(st.session_state["feedback"]["message"])
        else:
            st.error(st.session_state["feedback"]["message"])
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ Previous", disabled=(index == 0), use_container_width=True):
            st.session_state["index"] = max(0, index - 1)
            st.session_state["feedback"] = None
            st.rerun()
    
    with col2:
        if st.button("Submit Answer", type="primary", use_container_width=True):
            if user_answer:
                st.session_state["user_answers"][index] = user_answer
                st.session_state["answered_questions"].add(index)
                correct_answer = answers[index]
                
                if user_answer == correct_answer:
                    st.session_state["feedback"] = {"correct": True, "message": "🎉 Correct!"}
                else:
                    st.session_state["feedback"] = {"correct": False, "message": f"❌ Wrong! The correct answer is {correct_answer}"}
                st.rerun()
    
    with col3:
        if st.button("Next ➡", disabled=(index == len(questions) - 1), use_container_width=True):
            st.session_state["index"] = min(len(questions) - 1, index + 1)
            st.session_state["feedback"] = None
            st.rerun()
    
    # Display options with explanations
    st.markdown("### Answer Options:")
    for option in options:
        st.markdown(f'<div class="option-button">{option}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_results():
    questions = st.session_state["questions"]
    answers = st.session_state["answers"]
    user_answers = st.session_state["user_answers"]
    
    # Calculate score
    correct_count = sum(1 for i in range(len(questions)) if user_answers.get(i) == answers[i])
    total_questions = len(questions)
    score_percentage = (correct_count / total_questions) * 100
    
    # Display results
    st.title("🏆 Quiz Results")
    
    # Score message
    emoji = "🥇" if score_percentage >= 80 else "🥈" if score_percentage >= 60 else "🔄"
    message = "Excellent job!" if score_percentage >= 80 else "Good work!" if score_percentage >= 60 else "Keep practicing!"
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h2 style="text-align: center;">{emoji} Score Summary</h2>
                <h1 style="text-align: center; color: #3498db;">{correct_count}/{total_questions}</h1>
                <h3 style="text-align: center;">{score_percentage:.1f}%</h3>
                <p style="text-align: center;">{message}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """<div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h3>Performance Review</h3>""",
            unsafe_allow_html=True
        )
        
        st.write("Correct answers: " + "🟢 " * correct_count)
        st.write("Incorrect answers: " + "🔴 " * (total_questions - correct_count))
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Question review
    st.markdown("## Question Review")
    for i in range(total_questions):
        question_text = questions[i].split('\n')[0]
        options = questions[i].split('\n')[1:] if len(questions[i].split('\n')) > 1 else []
        
        is_correct = user_answers.get(i) == answers[i]
        expander_icon = "✅" if is_correct else "❌"
        
        with st.expander(f"{expander_icon} Question {i+1}: {question_text}"):
            for option in options:
                st.markdown(f'<div class="option-button">{option}</div>', unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f"*Correct Answer: {answers[i]}*")
            user_answer = user_answers.get(i, "Not answered")
            if is_correct:
                st.success(f"Your Answer: {user_answer} ✓")
            else:
                st.error(f"Your Answer: {user_answer} ✗")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Try Again", use_container_width=True):
            start_quiz()
    with col2:
        if st.button("🏠 New Quiz", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    if "questions" not in st.session_state:
        st.title("🧠 Python Quiz Challenge")
        st.markdown(
            """
            <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
                <h1 style="color: #3498db;">Welcome to the Python Quiz!</h1>
                <p style="font-size: 18px;">Test your Python knowledge with our interactive quiz.</p>
                <img src="https://www.python.org/static/community_logos/python-logo-generic.svg" style="width: 250px; margin: 20px 0;">
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### How to Play:")
        st.markdown("""
        1. Click the "Start Quiz" button below
        2. Answer each question by selecting an option
        3. Navigate between questions using the sidebar
        4. Submit your answers and see instant feedback
        5. Review your final score at the end
        """)
        
        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            start_quiz()
    elif st.session_state.get("completed", False):
        show_results()
    else:
        show_question()

if _name_ == "_main_":
    main()