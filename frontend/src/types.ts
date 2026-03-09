export interface User {
    id: string;
    name: string;
    email: string;
}

export interface Repository {
    id: string;
    url: string;
    owner_id: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    created_at: string;
}

export interface SourceDocument {
    file_path: string;
    content: string;
    distance: number;
}

export interface QueryResponse {
    answer: string;
    sources: SourceDocument[];
}

export interface QueryHistory {
    id: string;
    user_id: string;
    query: string;
    answer: string;
    sources: SourceDocument[];
    repo_id?: string;
    created_at: string;
}
