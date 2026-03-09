import React, { useState, useEffect } from 'react';
import api from '../lib/api';
import type { Repository } from '../types';
import toast from 'react-hot-toast';
import { Link } from 'react-router-dom';
import { Plus, Github, Loader2, ArrowRight } from 'lucide-react';

export default function Dashboard() {
    const [repos, setRepos] = useState<Repository[]>([]);
    const [url, setUrl] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const fetchRepos = async () => {
        try {
            const res = await api.get('/ingest/repositories');
            setRepos(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchRepos();
        const interval = setInterval(fetchRepos, 5000); // Poll for status updates
        return () => clearInterval(interval);
    }, []);

    const handleIngest = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!url.includes('github.com')) {
            toast.error('Please enter a valid GitHub URL');
            return;
        }

        setIsLoading(true);
        try {
            await api.post('/ingest/ingest_repo', { github_url: url });
            toast.success('Repository ingestion started!');
            setUrl('');
            fetchRepos();
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to start ingestion');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2>Knowledge Base Dashboard</h2>
                <Link to="/chat" className="btn btn-primary" style={{ textDecoration: 'none' }}>
                    Go to Chat <ArrowRight size={16} />
                </Link>
            </div>

            <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                    <Github size={20} /> Add GitHub Repository
                </h3>
                <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
                    Ingest a public repository to make it available for AI querying.
                </p>

                <form onSubmit={handleIngest} style={{ display: 'flex', gap: '1rem' }}>
                    <input
                        className="input-field"
                        style={{ flex: 1, margin: 0 }}
                        placeholder="https://github.com/username/repo"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        required
                    />
                    <button type="submit" className="btn btn-primary" disabled={isLoading}>
                        {isLoading ? <Loader2 className="animate-spin" size={18} /> : <Plus size={18} />}
                        Ingest
                    </button>
                </form>
            </div>

            <div className="glass-panel" style={{ padding: '2rem' }}>
                <h3 style={{ marginBottom: '1rem' }}>Indexed Repositories</h3>
                {repos.length === 0 ? (
                    <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '2rem 0' }}>
                        No repositories added yet.
                    </p>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {repos.map(repo => (
                            <div key={repo.id} style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                padding: '1rem',
                                background: 'rgba(0,0,0,0.2)',
                                borderRadius: '8px',
                                border: '1px solid var(--border-color)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                    <Github size={24} color="var(--text-muted)" />
                                    <div>
                                        <div style={{ fontWeight: 500 }}>{repo.url.replace('https://github.com/', '')}</div>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                                            Added {new Date(repo.created_at).toLocaleDateString()}
                                        </div>
                                    </div>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <span style={{
                                        padding: '0.25rem 0.75rem',
                                        borderRadius: '99px',
                                        fontSize: '0.8rem',
                                        fontWeight: 600,
                                        textTransform: 'uppercase',
                                        background: repo.status === 'completed' ? 'rgba(16, 185, 129, 0.2)' :
                                            repo.status === 'failed' ? 'rgba(239, 68, 68, 0.2)' :
                                                'rgba(59, 130, 246, 0.2)',
                                        color: repo.status === 'completed' ? 'var(--success)' :
                                            repo.status === 'failed' ? 'var(--danger)' :
                                                'var(--primary)'
                                    }}>
                                        {repo.status}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
