import { Outlet, Navigate, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, MessageSquare, LogOut, Code2, Loader2 } from 'lucide-react';

export default function Layout() {
    const { user, logout, isLoading } = useAuth();
    const navigate = useNavigate();

    if (isLoading) {
        return (
            <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Loader2 className="animate-spin" size={48} color="var(--primary)" />
            </div>
        );
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="app-container">
            {/* Sidebar */}
            <div className="sidebar">
                <div style={{ padding: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <Code2 size={24} color="var(--primary)" />
                    <h1 style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0 }}>RAG Assistant</h1>
                </div>

                <div style={{ padding: '1.5rem 1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
                    <Link to="/dashboard" className="btn btn-secondary" style={{ justifyContent: 'flex-start', background: 'transparent', border: 'none' }}>
                        <LayoutDashboard size={18} /> Dashboard
                    </Link>
                    <Link to="/chat" className="btn btn-secondary" style={{ justifyContent: 'flex-start', background: 'transparent', border: 'none' }}>
                        <MessageSquare size={18} /> Chat Copilot
                    </Link>
                </div>

                <div style={{ padding: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                            {user.email}
                        </div>
                        <button onClick={handleLogout} className="btn" style={{ background: 'transparent', color: 'var(--text-muted)', padding: '0.25rem' }}>
                            <LogOut size={16} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="main-content">
                <Outlet />
            </div>
        </div>
    );
}
