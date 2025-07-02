from langgraph.graph import StateGraph, END
from summary_state import State
from nodes import *
import global_var

def loop_or_exit(state: State) -> str:
    if state.get("evaluation_complete") or state.get("iteration_count")>= global_var.ITERATIONS:
        return "save"
    else:
        return "answer"


def build_graph():
    builder = StateGraph(State)
    builder.add_node("read", format_article_text)
    builder.add_node("explain", explain_terms)
    builder.add_node("summarize", generate_summary)
    builder.add_node("ask", generate_questions)
    builder.add_node("answer", answer_questions)
    builder.add_node("evaluate", evaluate_answers)
    builder.add_node("revise", improve_summary)
    builder.add_node("save", save_to_file)

    builder.set_entry_point("read")
    builder.add_edge("read", "explain")  # Ή "summarize" → "explain" αν το θες μετά
    builder.add_edge("explain", "save")
    builder.add_edge("read", "summarize")
    builder.add_edge("read", "ask")
    builder.add_edge("summarize", "answer")
    builder.add_edge("ask", "answer")
    builder.add_edge("answer", "evaluate")
    builder.add_edge("evaluate", "revise")
    builder.add_conditional_edges("revise", loop_or_exit, ["answer", "save"])
    builder.add_edge("save", END)
   
    return builder.compile()

def build_graph_8():
    builder = StateGraph(State)
    builder.add_node("read", format_article_text)
    builder.add_node("explain", explain_terms)
    builder.add_node("summarize", generate_summary)
    builder.add_node("ask", generate_questions)
    builder.add_node("answer", answer_questions)
    builder.add_node("evaluate", evaluate_answers)
    builder.add_node("revise", improve_summary)
    builder.add_node("save", save_to_file)

    builder.set_entry_point("read")
    builder.add_edge("read", "explain")  # Ή "summarize" → "explain" αν το θες μετά
    builder.add_edge("explain", "save")
    builder.add_edge("read", "summarize")
    builder.add_edge("read", "ask")
    builder.add_edge("summarize", "answer")
    builder.add_edge("ask", "answer")
    builder.add_edge("answer", "evaluate")
    builder.add_edge("evaluate", "revise")
    builder.add_conditional_edges("revise", loop_or_exit, ["answer", "save"])
    builder.add_edge("save", END)
   
    return builder.compile()

def build_graph_single():
    builder = StateGraph(State)
    builder.add_node("read", format_article_text)
    builder.add_node("explain", explain_terms)

    builder.add_node("summarize", generate_summary)
    
    builder.add_node("save", save_to_file)

    builder.set_entry_point("read")
    builder.add_edge("read", "explain")  # Ή "summarize" → "explain" αν το θες μετά

    builder.add_edge("read", "summarize")
    builder.add_edge("explain", "save")
    builder.add_edge("summarize", "save")
    builder.add_edge("save", END)

    return builder.compile()