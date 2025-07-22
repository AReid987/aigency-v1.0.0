// Search Service Implementation
import axios from 'axios';

const API_KEY = process.env.GOOGLE_PSE_API_KEY;
const SEARCH_ENGINE_ID = process.env.GOOGLE_PSE_ENGINE_ID;

interface SearchItem {
  title: string;
  link: string;
  snippet: string;
}

const searchService = {
  async search(query: string) {
    try {
      const response = await axios.get('https://www.googleapis.com/customsearch/v1', {
        params: {
          key: API_KEY,
          cx: SEARCH_ENGINE_ID,
          q: query
        }
      });

      return response.data.items.map((item: SearchItem) => ({
        title: item.title,
        link: item.link,
        snippet: item.snippet
      }));
    } catch (error) {
      console.error('Search API error:', error);
      throw new Error('Failed to perform search');
    }
  }
};

export default searchService;