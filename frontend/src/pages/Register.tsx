import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../lib/api';
import { UserPlus, Github } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Register() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.post('/auth/register', { name, email, password });
            toast.success('Registration successful! Please login.');
            navigate('/login');
        } catch (error: any) {
            const msg = error.response?.data?.detail;
            toast.error(typeof msg === 'string' ? msg : 'Registration failed');
        }
    };

    return (
        <div className="auth-container">
            <div className="glass-panel auth-card">
                <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1rem' }}>
                    <Github size={48} color="var(--primary)" />
                </div>
                <h2 className="auth-title">Create Account</h2>
                <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Join to start querying your repositories</p>

                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <input
                            className="input-field"
                            type="text"
                            placeholder="Full Name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                            minLength={2}
                        />
                    </div>
                    <div className="input-group">
                        <input
                            className="input-field"
                            type="email"
                            placeholder="Email address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <input
                            className="input-field"
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            minLength={6}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '1rem' }}>
                        <UserPlus size={18} /> Register
                    </button>
                </form>

                <p style={{ marginTop: '2rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    Already have an account? <Link to="/login" style={{ color: 'var(--primary)', textDecoration: 'none' }}>Sign in</Link>
                </p>
            </div>
        </div>
    );
}
