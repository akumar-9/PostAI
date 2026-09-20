import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

// Initialize Supabase (Replace with your actual keys)
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

// Your Render API URL
const API_URL = "https://your-render-app.onrender.com/generate";

export default function App() {
  const [session, setSession] = useState(null);
  const [history, setHistory] = useState([]);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      if (session) fetchHistory(session.user.id);
    });

    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session) fetchHistory(session.user.id);
    });
  }, []);

  const signInWithGoogle = async () => {
    await supabase.auth.signInWithOAuth({ provider: 'google' });
  };

  const fetchHistory = async (userId) => {
    const { data, error } = await supabase
      .from('history')
      .select('*')
      .order('created_at', { ascending: false });
    if (!error) setHistory(data);
  };

  const generateAndSave = async () => {
    if (!content) return;
    setLoading(true);

    try {
      // 1. Call your Render API
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, tone: "Professional", audience: "General" })
      });
      const generatedPosts = await response.json();

      // 2. Save to Supabase if logged in
      if (session) {
        await supabase.from('history').insert([{
          user_id: session.user.id,
          original_content: content,
          tone: "Professional",
          audience: "General",
          generated_posts: generatedPosts
        }]);
        fetchHistory(session.user.id); // Refresh history UI
      }
    } catch (error) {
      console.error("Error generating posts:", error);
    } finally {
      setLoading(false);
    }
  };

  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-6">Social Media Generator</h1>
          <button 
            onClick={signInWithGoogle}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition"
          >
            Continue with Google
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 font-sans">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <button onClick={() => supabase.auth.signOut()} className="text-gray-500 hover:text-gray-800">
          Sign Out
        </button>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border mb-8">
        <h2 className="text-lg font-semibold mb-2">Create New Campaign</h2>
        <textarea 
          className="w-full border rounded-lg p-3 mb-4"
          rows="3"
          placeholder="What are we posting about today?"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <button 
          onClick={generateAndSave}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium"
        >
          {loading ? 'Generating...' : 'Generate Posts'}
        </button>
      </div>

      <div>
        <h2 className="text-xl font-bold mb-4">Your History</h2>
        <div className="space-y-4">
          {history.map((item) => (
            <div key={item.id} className="bg-gray-50 p-4 rounded-lg border">
              <p className="text-sm text-gray-500 mb-2">{new Date(item.created_at).toLocaleDateString()}</p>
              <p className="font-medium mb-3">"{item.original_content}"</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(item.generated_posts).map(([platform, text]) => (
                  <div key={platform} className="bg-white p-3 rounded border text-sm">
                    <span className="font-bold capitalize text-blue-600 block mb-1">{platform}</span>
                    {text}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
