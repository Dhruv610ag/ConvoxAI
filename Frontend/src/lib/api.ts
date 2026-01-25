import axios, { AxiosError } from 'axios';
import type { APIResponse, SummaryResponse, ModelTestRequest, ErrorResponse } from '@/types/api';

// Get API base URL from environment variable or use default
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Health check endpoint
 */
export async function checkHealth(): Promise<{ message: string; version: string; docs: string; model: string }> {
  try {
    const response = await apiClient.get('/');
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

/**
 * Test LLM model endpoint
 */
export async function testModel(request: ModelTestRequest): Promise<APIResponse> {
  try {
    const response = await apiClient.post('/models', request);
    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

/**
 * Summarize audio file endpoint
 */
export async function summarizeAudio(file: File): Promise<SummaryResponse> {
  try {
    const formData = new FormData();
    formData.append('audio_file', file);

    const response = await apiClient.post('/summarize', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    throw handleApiError(error);
  }
}

/**
 * Handle API errors and convert to user-friendly messages
 */
function handleApiError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ErrorResponse>;
    
    if (axiosError.response) {
      // Server responded with error
      const errorData = axiosError.response.data;
      const message = errorData?.error || axiosError.message || 'An error occurred';
      return new Error(message);
    } else if (axiosError.request) {
      // Request made but no response
      return new Error('Unable to connect to the server. Please ensure the backend is running.');
    }
  }
  
  // Generic error
  return new Error('An unexpected error occurred');
}

export { API_BASE_URL };
