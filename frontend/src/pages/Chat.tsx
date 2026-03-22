import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import api from '../lib/api';
import type { QueryResponse, SourceDocument } from '../types';
import { Send, Bot, User, Code, FileText, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: SourceDocument[];
}

export default function Chat() {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState<Message[]>(() => {
        const savedMessages = localStorage.getItem('chatMessages');
        if (savedMessages) {
            try {
                return JSON.parse(savedMessages);
            } catch (e) {
                console.error("Failed to parse chat messages", e);
            }
        }
        return [{ role: 'assistant', content: "Hello! I'm your AI coding assistant. I can answer questions about the repositories you've indexed on the dashboard." }];
    });
    
    useEffect(() => {
        localStorage.setItem('chatMessages', JSON.stringify(messages));
    }, [messages]);

    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        const userMsg = query;
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setQuery('');
        setIsLoading(true);

        try {
            const res = await api.post<QueryResponse>('/query/', { query: userMsg });
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: res.data.answer,
                sources: res.data.sources
            }]);
        } catch (error) {
            toast.error('Failed to get response');
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error while processing your request." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%', maxWidth: '1200px', margin: '0 auto', padding: '1rem' }}>

            {/* Header */}
            <div style={{ padding: '1rem 0', borderBottom: '1px solid var(--border-color)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Bot color="var(--primary)" size={32} />
                <div>
                    <h2 style={{ fontSize: '1.25rem', margin: 0 }}>RAG Copilot</h2>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', margin: 0 }}>Ask questions about your codebase</p>
                </div>
            </div>

            {/* Chat Area */}
            <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1.5rem', padding: '1rem 0', scrollBehavior: 'smooth' }}>
                {messages.map((msg, idx) => (
                    <div key={idx} style={{
                        display: 'flex',
                        gap: '1rem',
                        flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
                    }}>
                        <div style={{
                            width: '40px', height: '40px', borderRadius: '50%',
                            background: msg.role === 'user' ? 'var(--accent)' : 'var(--primary)',
                            display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
                        }}>
                            {msg.role === 'user' ? <User size={20} color="white" /> : <Code size={20} color="white" />}
                        </div>

                        <div style={{ maxWidth: '80%' }}>
                            <div style={{
                                background: msg.role === 'user' ? 'var(--accent)' : 'var(--bg-card)',
                                padding: '1rem 1.25rem',
                                borderRadius: '16px',
                                borderTopRightRadius: msg.role === 'user' ? '4px' : '16px',
                                borderTopLeftRadius: msg.role === 'assistant' ? '4px' : '16px',
                                border: msg.role === 'assistant' ? '1px solid rgba(255,255,255,0.05)' : 'none',
                                lineHeight: 1.6,
                                boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
                            }}>
                                {msg.role === 'assistant' ? (
                                    <div className="markdown-body">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {msg.content}
                                        </ReactMarkdown>
                                    </div>
                                ) : (
                                    msg.content
                                )}
                            </div>

                            {/* Sources */}
                            {msg.sources && msg.sources.length > 0 && (
                                <div style={{ marginTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>SOURCES</div>
                                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                        {msg.sources.map((src, i) => (
                                            <div key={i} title={src.content} style={{
                                                display: 'flex', alignItems: 'center', gap: '0.25rem',
                                                background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
                                                padding: '0.25rem 0.75rem', borderRadius: '4px', fontSize: '0.75rem',
                                                color: 'var(--text-muted)', cursor: 'help'
                                            }}>
                                                <FileText size={12} />
                                                {src.file_path.split('/').pop()}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Loader2 className="animate-spin" size={20} color="white" />
                        </div>
                        <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Generating response...</div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div style={{ padding: '1rem 0', marginTop: 'auto' }}>
                <form onSubmit={handleSend} style={{ display: 'flex', gap: '0.5rem' }}>
                    <input
                        className="input-field"
                        style={{ flex: 1, margin: 0, borderRadius: '24px', paddingLeft: '1.5rem', background: 'var(--bg-card)' }}
                        placeholder="Ask about your codebase..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ borderRadius: '24px', width: '48px', height: '48px', padding: 0 }}
                        disabled={isLoading || !query.trim()}
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>

        </div>
    );
}
