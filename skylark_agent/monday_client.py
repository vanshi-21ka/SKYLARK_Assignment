import requests
import pandas as pd

class MondayBIConnector:
    def __init__(self, api_token: str, deals_board_id: str = None, work_orders_board_id: str = None):
        self.api_token = api_token
        self.deals_board_id = deals_board_id
        self.work_orders_board_id = work_orders_board_id
        self.api_url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            "API-Version": "2023-10"
        }

    def fetch_board_data(self, board_id: str):
        """
        Fetches items from a specific Monday.com board using GraphQL
        and parses them into a Pandas DataFrame.
        """
        query = f"""
        query {{
            boards (ids: {board_id}) {{
                name
                items_page {{
                    items {{
                        id
                        name
                        column_values {{
                            id
                            text
                            value
                        }}
                    }}
                }}
            }}
        }}
        """

        try:
            response = requests.post(
                self.api_url, 
                json={'query': query}, 
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()

            # 1. Check for GraphQL errors
            if "errors" in data:
                error_msg = data["errors"][0].get("message", str(data["errors"]))
                raise ValueError(f"Monday API returned an error: {error_msg}")

            if "data" not in data or not data["data"]:
                raise ValueError(f"Unexpected response structure from Monday API: {data}")

            boards = data["data"].get("boards")
            if not boards:
                raise ValueError(f"No board found with ID: {board_id}. Check board permissions and ID.")

            # 2. Extract items
            items_page = boards[0].get("items_page", {})
            items = items_page.get("items", [])

            # 3. Parse items into a clean DataFrame structure
            parsed_rows = []
            for item in items:
                row = {"Item Name": item.get("name")}
                for col in item.get("column_values", []):
                    # Use column text/value
                    col_id = col.get("id")
                    col_text = col.get("text")
                    row[col_id] = col_text
                parsed_rows.append(row)

            # Return as a Pandas DataFrame so agent_engine can process it
            return pd.DataFrame(parsed_rows)

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP Request failed: {e}")