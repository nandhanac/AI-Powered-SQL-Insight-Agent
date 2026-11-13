
import streamlit as st
import streamlit.components.v1 as components
from agent.query_runner import answer_question


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI SQL Insight Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# 2. CHATGPT-STYLE CSS
# ==================================================

st.markdown(
    """
    <style>
    /* Main application */
    .stApp {
        background-color: #212121;
        color: #ececec;
    }

    [data-testid="stHeader"] {
        background-color: #212121;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #171717;
        border-right: 1px solid #303030;
    }

    [data-testid="stSidebar"] button {
        border-radius: 10px;
        text-align: left;
    }

    /* Main content width */
    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* Title */
    .app-title {
        font-size: 1.5rem;
        font-weight: 650;
        color: #ececec;
        letter-spacing: -0.5px;
    }

    .app-subtitle {
        color: #a3a3a3;
        font-size: 0.95rem;
        margin-top: 0.35rem;
    }

    /* Welcome heading */
    .welcome-title {
        font-size: 1.8rem;
        font-weight: 600;
        text-align: center;
        color: #ececec;
        margin-top: 5rem;
        margin-bottom: 0.5rem;
    }

    .welcome-subtitle {
        text-align: center;
        color: #a3a3a3;
        margin-bottom: 2rem;
    }

    /* Chat message containers */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
        padding: 1rem 0.3rem;
    }

    [data-testid="stChatMessage"] p {
        line-height: 1.7;
    }

    /* Text input */
    [data-testid="stChatInput"] {
        background-color: #303030;
        border: 1px solid #454545;
        border-radius: 24px;
    }

    [data-testid="stChatInput"] textarea {
        color: #ececec;
    }

    /* Buttons */
    .stButton button {
        border-radius: 12px;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #262626;
        border: 1px solid #414141;
        border-radius: 12px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #292929;
        border: 1px solid #404040;
        padding: 15px;
        border-radius: 12px;
    }

    /* Divider */
    hr {
        border-color: #383838;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        color: #777777;
        font-size: 0.8rem;
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 3. SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []


# ==================================================
# 4. CALLBACK FUNCTIONS
# ==================================================

def start_new_chat():
    """Start a new conversation without deleting history."""
    st.session_state.messages = []


def load_previous_chat(index):
    """Restore a previous question and its result."""
    item = st.session_state.history[index]

    st.session_state.messages = [
        {
            "role": "user",
            "content": item["question"],
        },
        {
            "role": "assistant",
            "result": item["result"],
        },
    ]


def clear_all_history():
    """Clear the current conversation and recent history."""
    st.session_state.messages = []
    st.session_state.history = []


# ==================================================
# 5. SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown(
        """
        <div class="app-title">
            ◉ AI SQL Agent
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Your conversational database assistant")

    st.button(
        "＋  New chat",
        key="new_chat_button",
        use_container_width=True,
        on_click=start_new_chat,
    )

    st.divider()

    st.markdown("**Recent chats**")

    if st.session_state.history:
        for index, item in enumerate(
            st.session_state.history
        ):
            label = item["question"]

            if len(label) > 34:
                label = label[:31] + "..."

            st.button(
                f"◷  {label}",
                key=f"history_button_{index}",
                use_container_width=True,
                on_click=load_previous_chat,
                args=(index,),
            )
    else:
        st.caption("Your previous questions will appear here.")

    st.divider()

    with st.expander("About this project"):
        st.write(
            "An AI-powered SQL assistant that converts "
            "natural-language questions into SQL, executes "
            "validated queries, analyzes the results, and "
            "generates insights and charts."
        )

        st.caption(
            "Python · MySQL · Gemini · Pandas · Plotly"
        )

    st.button(
        "Clear chat history",
        key="clear_history_button",
        use_container_width=True,
        on_click=clear_all_history,
    )


# ==================================================
# 6. MAIN HEADER
# ==================================================

header_col, status_col = st.columns([4, 1])

with header_col:
    st.markdown(
        '<div class="app-title">'
        'AI-Powered SQL Insight Agent'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Ask questions. Explore data. Discover insights.'
        '</div>',
        unsafe_allow_html=True,
    )

with status_col:
    st.caption("● AI assistant")


# ==================================================
# 7. WELCOME SCREEN
# ==================================================

if not st.session_state.messages:
    st.markdown(
        '<div class="welcome-title">'
        'What would you like to know?'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'Ask a question about your database in plain English.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("##### Try asking")

    suggestions = [
        (
            "📊 Sales analysis",
            "What are the total sales for each product?",
        ),
        (
            "🏆 Top products",
            "Show the top 5 products by price.",
        ),
        (
            "👥 Customers",
            "How many customers are in the database?",
        ),
        (
            "📦 Order status",
            "Show the number of orders for each order status.",
        ),
    ]

    suggestion_columns = st.columns(2)

    for index, (label, question) in enumerate(suggestions):
        with suggestion_columns[index % 2]:
            st.button(
                label,
                key=f"suggestion_{index}",
                help=question,
                use_container_width=True,
                on_click=lambda q=question: (
                    st.session_state.update(
                        {"pending_question": q}
                    )
                ),
            )


# ==================================================
# 8. RENDER CONVERSATION
# ==================================================

for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])

    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="📊"):

            result = message.get("result")

            if not result:
                st.write("No result is available.")
                continue

            if not result.get("success"):
                st.error(
                    f"Failed at "
                    f"{result.get('stage', 'unknown stage')}: "
                    f"{result.get('error', 'Unknown error')}"
                )
                continue

            st.markdown("### Analysis complete")

            # --------------------------------------
            # Summary metrics
            # --------------------------------------

            metric1, metric2 = st.columns(2)

            with metric1:
                st.metric(
                    "Rows returned",
                    result.get("row_count", 0),
                )

            with metric2:
                st.metric(
                    "Columns returned",
                    len(result.get("columns", [])),
                )

            # --------------------------------------
            # Query results
            # --------------------------------------

            st.markdown("#### Query results")

            rows = result.get("rows", [])

            if rows:
                st.dataframe(
                    rows,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("The query returned no rows.")

            if result.get("truncated"):
                st.warning(
                    "Showing the first 500 rows only."
                )

            # --------------------------------------
            # AI-generated insights
            # --------------------------------------

            st.markdown("#### AI-generated insights")

            if result.get("insight_success"):
                st.markdown(result.get("insights", ""))

            else:
                st.warning(
                    "The SQL query succeeded, but insight "
                    "generation failed."
                )

                st.caption(
                    result.get(
                        "insight_error",
                        "No additional details are available.",
                    )
                )

            # --------------------------------------
            # Interactive chart
            # --------------------------------------

            if result.get("chart_available"):
                chart = result.get("chart")

                if chart is not None:
                    st.markdown("#### Data visualization")

                    st.plotly_chart(
                        chart,
                        use_container_width=True,
                    )

            # --------------------------------------
            # Expandable SQL and analysis
            # --------------------------------------

            with st.expander("View generated SQL"):
                st.code(
                    result.get("query", ""),
                    language="sql",
                )

            with st.expander("View local data analysis"):
                analysis = result.get("analysis", {})

                st.json(
                    analysis.get("summary", {})
                )


# ==================================================
# 9. CHAT INPUT AND WORKFLOW
# ==================================================

# A suggestion button sets pending_question.
# Read it before calling st.chat_input.
pending_question = st.session_state.pop(
    "pending_question",
    None,
)

prompt = st.chat_input(
    "Ask anything about your database...",
    key="chat_input",
)

# A typed prompt takes precedence over a suggestion.
question = prompt or pending_question

if question and question.strip():

    question = question.strip()

    # Add the user message immediately.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Generate SQL, execute it, analyze the data,
    # and generate insights.
    with st.spinner(
        "Analyzing your question and querying the database..."
    ):
        try:
            result = answer_question(question)

        except Exception as error:
            result = {
                "success": False,
                "stage": "application",
                "error": (
                    f"{type(error).__name__}: {error}"
                ),
            }

    # Add the assistant result.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "result": result,
        }
    )

    # Save question and result in recent history.
    st.session_state.history.insert(
        0,
        {
            "question": question,
            "result": result,
        },
    )

    # Keep only the latest 10 entries.
    st.session_state.history = (
        st.session_state.history[:10]
    )

    # Rerun to render both messages in the chat.
    st.rerun()


# ==================================================
# 10. FOOTER
# ==================================================

st.markdown(
    """
    <div class="app-footer">
        AI SQL Insight Agent · Python · MySQL · Gemini
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# 11. FLOATING SCROLL-TO-BOTTOM BUTTON
# ==================================================

components.html(
    """
    <button id="scroll-bottom-button" title="Scroll to latest answer">
        ↓
    </button>

    <style>
        html, body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: transparent;
        }

        #scroll-bottom-button {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            border: 1px solid #555;
            background: #303030;
            color: white;
            font-size: 26px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);
        }

        #scroll-bottom-button:hover {
            background: #454545;
        }
    </style>

    <script>
        const frame = window.frameElement;

        // Keep the button floating above the Streamlit page.
        if (frame) {
            frame.style.position = "fixed";
            frame.style.right = "24px";
            frame.style.bottom = "90px";
            frame.style.width = "52px";
            frame.style.height = "52px";
            frame.style.zIndex = "999999";
            frame.style.border = "0";
            frame.style.background = "transparent";
        }

        document.getElementById("scroll-bottom-button")
            .addEventListener("click", function () {
                try {
                    const doc = window.parent.document;

                    // Find the main Streamlit content area.
                    const main = doc.querySelector(
                        '[data-testid="stMain"]'
                    );

                    const appView = doc.querySelector(
                        '[data-testid="stAppViewContainer"]'
                    );

                    // Try the main content area first.
                    if (main) {
                        main.scrollTo({
                            top: main.scrollHeight,
                            behavior: "smooth"
                        });
                    }

                    // Also scroll the app view if it is scrollable.
                    if (appView) {
                        appView.scrollTo({
                            top: appView.scrollHeight,
                            behavior: "smooth"
                        });
                    }

                    // Scroll the last rendered chat message into view.
                    const messages = doc.querySelectorAll(
                        '[data-testid="stChatMessage"]'
                    );

                    if (messages.length > 0) {
                        messages[messages.length - 1].scrollIntoView({
                            behavior: "smooth",
                            block: "end"
                        });
                    }
                } catch (error) {
                    console.error("Unable to scroll:", error);
                }
            });
    </script>
    """,
    height=60,
    width=60,
)

