/** Function to perform requests. */
export type Fetcher = typeof fetch;

/** HTTP methods. */
export type Method = 'GET' | 'POST' | 'PUT' | 'DELETE';

/**
 * Join URL parts with a slash.
 */
export const join = (...parts: string[]) => {
    let full = '';
    for (const part of parts) {
      if (full) {
        if (!full.endsWith('/')) {
          full += '/';
        }
        full += part.replace(/^\/+/, '');
      } else {
        full = part;
      }
    }
    return full;
};
  
/**
 * Get full API route.
 */
export const fullPath = (path: string) => {
    return join('/api/v1/', path);
};

/**
 * Common fetch method.
 */
const _fetch = async (
f: Fetcher,
method: Method,
path: string,
headers?: Record<string, string>,
body?: string | FormData
) => {
    const full = fullPath(path);
    return f(full, {
        method,
        headers,
        body,
        credentials: 'include',
        mode: 'cors'
    });
};

export interface Trivium {
    id: number;
    season: number;
    question: string;
    answer: string;
    category: string;
    score: number;
}

export const getRandomQuestion = async (f: Fetcher) => {
    const response = await _fetch(f, 'GET', 'questions/random');
    if (!response.ok) {
        throw new Error('Failed to fetch question');
    }
    const data = await response.json();
    return data as Trivium;
}

export interface Explanation {
    trivium: Trivium;
    summary: {
      content: string;
    };
}

export const getExplanation = async (f: Fetcher, id: string) => {
    const response = await _fetch(f, 'GET', `questions/${id}/explain`);
    if (!response.ok) {
        throw new Error('Failed to fetch explanation');
    }
    const data = await response.json();
    return data as Explanation;
}