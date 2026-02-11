// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types
export interface Law {
  id: string;
  numero: string;
  year: number;
  fecha: string;
  epigrafe: string;
  tipo?: string;
  summary?: string;
  ai_analysis?: string;
}

export interface SearchParams {
  query?: string;
  year?: number;
  type?: string;
  limit?: number;
  offset?: number;
}

export interface SearchResponse {
  results: Law[];
  total: number;
  page: number;
  pages: number;
}

export interface ScrapeConfig {
  year: number;
  max_laws?: number;
  use_ai?: boolean;
}

export interface ScrapeResponse {
  task_id: string;
  status: string;
  message: string;
}

export interface HealthResponse {
  status: string;
  database: string;
  ai: string;
}

// API Functions
export const api = {
  // Health check
  health: async (): Promise<HealthResponse> => {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) throw new Error('Health check failed');
    return response.json();
  },

  // Search laws
  search: async (params: SearchParams): Promise<SearchResponse> => {
    const queryParams = new URLSearchParams();
    if (params.query) queryParams.set('query', params.query);
    if (params.year) queryParams.set('year', params.year.toString());
    if (params.type) queryParams.set('type', params.type);
    if (params.limit) queryParams.set('limit', params.limit.toString());
    if (params.offset) queryParams.set('offset', params.offset.toString());

    const response = await fetch(`${API_BASE_URL}/search?${queryParams}`);
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  },

  // Get law by ID
  getLaw: async (id: string): Promise<Law> => {
    const response = await fetch(`${API_BASE_URL}/laws/${id}`);
    if (!response.ok) throw new Error('Failed to get law');
    return response.json();
  },

  // Get laws by year
  getLawsByYear: async (year: number): Promise<Law[]> => {
    const response = await fetch(`${API_BASE_URL}/laws/year/${year}`);
    if (!response.ok) throw new Error('Failed to get laws');
    return response.json();
  },

  // Start scraping
  startScrape: async (config: ScrapeConfig): Promise<ScrapeResponse> => {
    const response = await fetch(`${API_BASE_URL}/scrape`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });
    if (!response.ok) throw new Error('Failed to start scraping');
    return response.json();
  },

  // Get scrape status
  getScrapeStatus: async (taskId: string) => {
    const response = await fetch(`${API_BASE_URL}/scrape/status/${taskId}`);
    if (!response.ok) throw new Error('Failed to get status');
    return response.json();
  },

  // Get statistics
  getStats: async () => {
    const response = await fetch(`${API_BASE_URL}/stats`);
    if (!response.ok) throw new Error('Failed to get stats');
    return response.json();
  },
};

// Utility function for error handling
export const handleApiError = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unknown error occurred';
};
