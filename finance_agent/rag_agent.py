from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from finance_agent.config import GOOGLE_API_KEY
from finance_agent.tools.rag_tool import search_financial_documents
from finance_agent.rag_prompt import RAG_SYSTEM_PROMPT

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)

rag_agent = create_agent(

    model=llm,

    tools=[
        search_financial_documents
    ],

    system_prompt=RAG_SYSTEM_PROMPT

)


def ask_documents(question: str):

    response = rag_agent.invoke(

        {

            "messages":[

                {

                    "role":"user",

                    "content":question

                }

            ]

        }

    )

    message = response["messages"][-1]
    content = message.content

    if isinstance(content, list):
        answer = "".join(
            item["text"] if isinstance(item, dict) else str(item)
            for item in content
        )
    else:
        answer = content

    return answer.replace("*", "")

# --------------------------------------------------
# Banner
# --------------------------------------------------

def print_banner():

    print("=" * 75)
    print("      FinanceGPT - Financial Documents RAG")
    print("=" * 75)

    print("\nCapabilities")

    print("-> Financial Report Search")
    print("-> Annual Reports")
    print("-> SEC Filings")
    print("-> Earnings Reports")
    print("-> Gemini + FAISS RAG")

    print("\nType 'exit' to quit.\n")


# --------------------------------------------------
# Chat Loop
# --------------------------------------------------

def run():

    print_banner()

    while True:

        query = input("You : ").strip()

        if query.lower() in ["exit", "quit"]:

            print("\nGoodbye!\n")

            break

        try:

            answer = ask_documents(query)

            print("\n" + "=" * 75)
            print("FinanceGPT\n")
            print(answer)
            print("=" * 75)
            print()

        except KeyboardInterrupt:

            print("\nInterrupted.\n")

            break

        except Exception as e:

            print("\nAn error occurred:\n")

            print(e)

            print()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    run()