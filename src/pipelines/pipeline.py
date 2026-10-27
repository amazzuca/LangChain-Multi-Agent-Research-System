from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state = {}
    #search agent working
    print("\n"+" ="*50)
    print("step 1 - search agent is working...")
    print("="*50)

    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about the topic: {topic}")]
    })

    state['search_results'] = search_results['messages'][-1].content

    print("\n search results: \n", state['search_results'])


    #step 2 - reader agent working
    print("\n"+" ="*50)
    print("step 2 - reader agent is scraping top resources...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages": [("user",
                      f"Based on the following search results about '{topic}',"
                      f"pick the most relevant URL and scrape it for deeper content. \n\n"
                      f"Search Results: \n{state['search_results'][:800]}"
                      )]
    })

    state['scraped_content'] = reader_results['messages'][-1].content
    print("\n scraped content: \n", state['scraped_content'])

    #step 3 - writer chain working
    print("\n"+" ="*50)
    print("step 3 - writer chain is generating the research report...")
    print("="*50)   

    research_combined = (
        f"Search Results: \n{state['search_results'][:800]}\n\n"
        f"Detailed Scraped Content: \n{state['scraped_content'][:800]}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\n Final report: \n", state['report'])

    #step 4 - critic chain working
    print("\n"+" ="*50)
    print("step 4 - critic chain is evaluating the research report...")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })
    print("\n critic report: \n", state['feedback'])

    return state
