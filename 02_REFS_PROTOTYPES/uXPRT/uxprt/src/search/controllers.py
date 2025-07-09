from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any # Added Dict, Any for mock
# from mcp import use_mcp_tool # Commenting out direct import as it's not available in this env

# Mock use_mcp_tool for local development without live MCP server
async def use_mcp_tool(server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    print(f"[MOCK] MCP Call: Server='{server_name}', Tool='{tool_name}', Args='{arguments}'")
    if server_name == "brave-search" and tool_name == "brave_web_search":
        # Simulate a brave search response structure
        return {
            "results": [
                {"title": f"Mock result for '{arguments.get('query')}' 1", "url": "http://example.com/mock1", "snippet": "This is a mock Brave Search result."},
                {"title": f"Mock result for '{arguments.get('query')}' 2", "url": "http://example.com/mock2", "snippet": "Another mock result."}
            ]
        }
    return {"error": "Mock MCP tool not found or not implemented"}

from supabase import create_client, Client
import os
from uuid import UUID # Import UUID
from dotenv import load_dotenv
# Corrected import for the auth dependency function
from ..auth.controllers import get_current_user
from gotrue.types import User as SupabaseUser # Import User type for dependency


# --- Supabase Client Initialization (Module Level) ---
load_dotenv(override=True)
SUPABASE_URL_ENV = str(os.getenv("SUPABASE_URL", "")).strip()
SUPABASE_KEY_ENV = str(os.getenv("SUPABASE_KEY", "")).strip()

supabase_client: Optional[Client] = None
initialization_error: Optional[str] = None

if SUPABASE_URL_ENV and SUPABASE_KEY_ENV:
    print(f"Initializing Supabase client with URL: '{SUPABASE_URL_ENV}'")
    print(f"Initializing Supabase client with KEY: '{SUPABASE_KEY_ENV}'")
    try:
        supabase_client = create_client(SUPABASE_URL_ENV, SUPABASE_KEY_ENV)
        print("Supabase client initialized successfully at module level.")
    except Exception as e:
        initialization_error = f"Failed to initialize Supabase client at module level: {e}"
        print(initialization_error)
        supabase_client = None # Ensure client is None if init fails
else:
    initialization_error = "Supabase URL or Key not found in environment variables. Client not initialized."
    print(initialization_error)
# --- End Supabase Client Initialization ---


# Removed placeholder get_current_user_id as we use get_current_user dependency now

class SearchRequest(BaseModel):
    query: str
    count: Optional[int] = 10
    offset: Optional[int] = 0

class SearchResultItem(BaseModel):
    # Define a more specific schema for search results based on brave-search output
    # This is a placeholder, adjust based on actual data structure
    title: str
    url: str
    snippet: Optional[str] = None

class SearchResponse(BaseModel):
    status: str
    results: List[SearchResultItem] # Use the specific schema
    query_id: Optional[UUID] = None # Use UUID type for query_id


# Removed get_supabase_client dependency function as client is initialized globally or passed directly

router = APIRouter()


# Changed to sync function, updated decorator and dependencies
@router.post("/", response_model=SearchResponse)
# @token_required # Replaced with correct dependency
async def web_search(
    request: SearchRequest,
    # user_id: UUID = Depends(get_current_user_id), # Replaced with actual user from token
    current_user: SupabaseUser = Depends(get_current_user), # Use correct dependency
    # supabase: Client = Depends(get_supabase_client) # Removed dependency, use module-level client
):
    """
    Performs a web search using the brave-search MCP tool and stores the query and results in Supabase.
    Requires authentication.
    """
    # Use the globally initialized client (or handle error if it failed)
    if supabase_client is None:
         detail_msg = "Supabase client not available."
         if initialization_error:
             detail_msg = f"Supabase client not available: {initialization_error}"
         raise HTTPException(status_code=503, detail=detail_msg)
    supabase = supabase_client # Use the module-level client

    try:
        # Call the brave_web_search MCP tool - Commented out for testing
        mcp_response = await use_mcp_tool(
            server_name="brave-search",
            tool_name="brave_web_search",
            arguments={
                "query": request.query,
                "count": request.count,
                "offset": request.offset
            }
        )

        # Process the response from the MCP tool
        # Assuming the MCP tool returns a structure with a 'results' key
        if mcp_response and 'results' in mcp_response:
            search_results_raw = mcp_response.get('results', [])

            # Map raw results to SearchResultItem model
            search_results = []
            for item in search_results_raw:
                search_results.append(SearchResultItem(
                    title=item.get('title', 'No Title'),
                    url=item.get('url', '#'),
                    snippet=item.get('snippet')
                ))


            # Store the search query and results in Supabase
            # Assuming 'search_queries' table exists with 'user_id', 'query_text', and 'results' columns
            insert_data = {
                "user_id": str(current_user.id), # Use user ID from authenticated user
                "query_text": request.query,
                "results": [res.model_dump() for res in search_results] # Store the results JSONB
            }

            # Raw HTTPX POST block removed.

            response = supabase.table("search_queries").insert(insert_data).execute()

            # Check for database insert errors
            if response.data:
                 # Assuming the insert returns the inserted row with query_id
                query_id = response.data[0].get('query_id')
                return {
                    "status": "Search successful and data stored",
                    "results": search_results,
                    "query_id": UUID(query_id) if query_id else None # Convert query_id to UUID
                }
            else:
                # Attempt to get more specific error info if available
                error_detail = "Unknown database error during insert"
                if hasattr(response, 'error') and response.error:
                    # Try accessing common error attributes, might vary by library version
                    code = getattr(response.error, 'code', 'N/A')
                    message = getattr(response.error, 'message', 'N/A')
                    details = getattr(response.error, 'details', 'N/A')
                    hint = getattr(response.error, 'hint', 'N/A')
                    error_detail = f"Code: {code}, Message: {message}, Details: {details}, Hint: {hint}"
                elif hasattr(response, 'status_code'):
                     error_detail = f"Insert failed with Status Code: {response.status_code}"

                print(f"Supabase insert error details: {error_detail}")
                # Use the more detailed error if available
                raise HTTPException(status_code=500, detail=f"Failed to store search results in database: {error_detail}")

            # Return placeholder results directly, bypassing DB insert - Removed
            # return {
            #     "status": "Search successful (DB bypassed for testing)",
            #     "results": search_results,
            #     "query_id": UUID("11111111-1111-1111-1111-111111111111") # Placeholder query_id
            # }

        else:
            # Handle cases where the MCP tool response is not as expected
            print(f"Unexpected MCP response: {mcp_response}")
            raise HTTPException(status_code=500, detail="Failed to process search results from MCP tool.")

    except Exception as e:
        print(f"Error during search or database operation: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")