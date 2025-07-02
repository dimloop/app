from utils import load_article_from_json
from graph import build_graph, build_graph_single 
from summary_state import State
from nodes import format_article_text, generate_summary, save_to_file
from langgraph.errors import GraphRecursionError
import global_var

def summarize_article_json(article: dict = None, json_path: str = None, output_path: str = None, single: bool = False) -> None:
    print(global_var.ITERATIONS)
    if article is None:
        if json_path is None:
            raise ValueError("Either 'article' or 'json_path' must be provided.")
        article = load_article_from_json(json_path)


    state: State = {
        "article": article,
        "article_text": "",
        "summary": "",
        "summary_7": "",
        "summary_1": "",
        "questions": "",
        "answers": "",
        "feedback": "",
        "evaluation_complete": False,
        "iteration_count": 0,
        "output_path": output_path,
    }

    if single:
        graph = build_graph_single()
        # Image plot #
        #image_data = graph.get_graph().draw_mermaid_png()

        # Save to file
        #with open("graph.png", "wb") as f:
        #    f.write(image_data)
        result = graph.invoke(state)
        #save_to_file(result)
        #print(state)
        

    else:
        graph = build_graph()
        
        # Image plot #
        image_data = graph.get_graph().draw_mermaid_png()

        # Save to file
        with open("graph.png", "wb") as f:
            f.write(image_data)

        result = graph.invoke(state)
        #print("result ", state.get('iteration_count', 'N/A'))
        #print(result)
       
    print("✅ Saved to:", output_path)

if __name__ == "__main__":
   
    #summarize_article_json("articles/economy/article1.json", "summaries/7node/economy/article1.txt")
    #summarize_article_json("articles/economy/article2.json", "summaries/7node/economy/article2.txt")
    #summarize_article_json("articles/greece/article1.json", "summaries/7node/greece/article1.txt")
    #summarize_article_json("articles/greece/article2.json", "summaries/7node/greece/article2.txt")
    #summarize_article_json("articles/politics/article1.json", "summaries/7node/politics/article1.txt")
    #summarize_article_json("articles/politics/article2.json", "summaries/7node/politics/article2.txt")
    #summarize_article_json("articles/world/article1.json", "summaries/7node/world/article1.txt")
    #summarize_article_json("articles/world/article2.json", "summaries/7node/world/article2.txt")
    #summarize_article_json(json_path = "articles/test/article.json", output_path = "summaries/7node/test")
    summarize_article_json(json_path= "articles/test/article.json",output_path= "summaries/1node/test", single=True)
