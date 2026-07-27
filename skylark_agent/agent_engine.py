from openai import OpenAI

class BIQueryAgent:
    def __init__(self, monday_connector, api_key: str):
        self.connector = monday_connector
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )

    def answer_query_stream(self, query: str):
        # Fetch live data from Monday.com
        deals_df = self.connector.fetch_board_data(self.connector.deals_board_id)
        deals_summary = deals_df.to_string() if not deals_df.empty else "No deals data found."

        system_prompt = (
            "You are an Executive Business Intelligence Agent for Skylark Drones. "
            "Analyze the provided Monday.com board data and provide a concise, executive summary "
            "answering the user's question clearly. Do not use italics for whole sentences."
        )

        user_content = f"Monday.com Deals Data:\n{deals_summary}\n\nUser Question: {query}"

        # Enable streaming = True
        stream = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            stream=True  # Stream chunks back
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content