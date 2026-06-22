from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from finance_agent.config import GOOGLE_API_KEY

from finance_agent.prompts import SYSTEM_PROMPT

from finance_agent.tools.news_tool import get_news_sentiment
from finance_agent.tools.indicator_tool import get_indicators
from finance_agent.tools.prediction_tool import predict_return


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)

# --------------------------------------------------
# AI Finance Agent
# --------------------------------------------------

agent = create_agent(
    model=llm,
    tools=[
        get_news_sentiment,
        get_indicators,
        predict_return
    ],
    system_prompt=SYSTEM_PROMPT
)


# --------------------------------------------------
# Banner
# --------------------------------------------------

def print_banner():

    print("=" * 75)
    print("            FinanceGPT - AI Financial Agent")
    print("=" * 75)

    print("\nCapabilities")

    print("-> Financial News (Finnhub)")
    print("-> FinBERT Sentiment Analysis")
    print("-> Technical Indicators")
    print("-> XGBoost Prediction")
    print("-> LLM Reasoning (Gemini)")

    print("\nType 'exit' to quit.\n")


# --------------------------------------------------
# Chat Loop
# --------------------------------------------------

def run():

    print_banner()

    while True:

        query = input("You : ").strip()

        if query.lower() in [
            "exit",
            "quit"
        ]:
            print("\nGoodbye!\n")
            break

        try:

            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                }
            )

            print("\n" + "=" * 75)
            print("FinanceGPT\n")

            answer = response["messages"][-1].content

            if answer:
                print(answer)
            else:
                print("No response generated.")

            print("=" * 75)
            print()

        except KeyboardInterrupt:

            print("\nInterrupted.\n")
            break

        except Exception as e:

            print("\nAn error occurred:\n")
            print(e)
            print()
            

def ask_finance_agent(question: str) -> str:
    """
    Ask FinanceGPT a question and return the response.
    """

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
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


    # Remove markdown formatting
    answer = answer.replace("**", "")
    answer = answer.replace("*", "")

    return answer


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    run()