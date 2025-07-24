import { useState, useCallback, useRef, useEffect } from 'react';
import axios from 'axios';

const CHAT_API_URL = process.env.NEXT_PUBLIC_CHAT_API_URL || 'http://localhost:8000';

export const useChat = (initialPrompt = 'finchat_prompt') => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [currentPrompt, setCurrentPrompt] = useState(initialPrompt);
  const [availablePrompts, setAvailablePrompts] = useState([]);
  const [error, setError] = useState(null);
  
  // Message history for arrow key navigation
  const [messageHistory, setMessageHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  
  const abortControllerRef = useRef(null);

  // Load available prompts on mount
  useEffect(() => {
    loadAvailablePrompts();
  }, []);

  const loadAvailablePrompts = async () => {
    try {
      const response = await axios.get(`${CHAT_API_URL}/api/prompts`);
      setAvailablePrompts(response.data);
    } catch (error) {
      console.error('Failed to load prompts:', error);
    }
  };

  const sendMessage = useCallback(async (message, userId = 'web_user') => {
    if (!message.trim() || isLoading) return;

    // Add to message history for navigation
    setMessageHistory(prev => {
      const newHistory = [message, ...prev.filter(m => m !== message)];
      return newHistory.slice(0, 50); // Limit to 50 messages
    });
    setHistoryIndex(-1);

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      sender: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    // Cancel any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    abortControllerRef.current = new AbortController();

    try {
      const response = await axios.post(
        `${CHAT_API_URL}/api/chat`,
        {
          message,
          user_id: userId,
          session_id: sessionId,
          prompt_name: currentPrompt
        },
        {
          signal: abortControllerRef.current.signal,
          timeout: 30000 // 30 second timeout
        }
      );

      const { response: botResponse, session_id, engagement_score } = response.data;

      // Update session ID if this is a new session
      if (!sessionId) {
        setSessionId(session_id);
      }

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        content: botResponse,
        timestamp: new Date().toISOString(),
        engagementScore: engagement_score,
        isReactPattern: currentPrompt === 'react_prompt' && 
          (botResponse.includes('Thought:') || botResponse.includes('Action:'))
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      if (error.name === 'AbortError') return; // Request was cancelled
      
      console.error('Chat error:', error);
      setError(error.response?.data?.detail || 'Failed to send message');
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'system',
        content: 'Sorry, there was an error processing your message. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, currentPrompt, isLoading]);

  const changePrompt = useCallback((newPrompt) => {
    if (newPrompt !== currentPrompt) {
      setCurrentPrompt(newPrompt);
      setSessionId(null); // Start new session
      setMessages([{
        id: Date.now(),
        sender: 'system',
        content: `Switched to ${newPrompt.replace('_', ' ')} mode. ${
          newPrompt === 'react_prompt' 
            ? 'I will show my thinking process step by step.' 
            : 'How can I help you?'
        }`,
        timestamp: new Date().toISOString()
      }]);
      setMessageHistory([]); // Reset history
      setHistoryIndex(-1);
    }
  }, [currentPrompt]);

  const navigateHistory = useCallback((direction) => {
    if (messageHistory.length === 0) return null;

    let newIndex = historyIndex;
    
    if (direction === 'up') {
      newIndex = Math.min(historyIndex + 1, messageHistory.length - 1);
    } else if (direction === 'down') {
      newIndex = Math.max(historyIndex - 1, -1);
    }
    
    setHistoryIndex(newIndex);
    return newIndex >= 0 ? messageHistory[newIndex] : '';
  }, [messageHistory, historyIndex]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    setError(null);
  }, []);

  const getStats = useCallback(async () => {
    try {
      const response = await axios.get(`${CHAT_API_URL}/api/stats`);
      return response.data;
    } catch (error) {
      console.error('Failed to get stats:', error);
      return null;
    }
  }, []);

  const getChatHistory = useCallback(async (userId = 'web_user', limit = 50) => {
    if (!sessionId) return null;
    
    try {
      const response = await axios.get(
        `${CHAT_API_URL}/api/sessions/${sessionId}/history`,
        { params: { user_id: userId, limit } }
      );
      return response.data;
    } catch (error) {
      console.error('Failed to get chat history:', error);
      return null;
    }
  }, [sessionId]);

  return {
    // State
    messages,
    isLoading,
    sessionId,
    currentPrompt,
    availablePrompts,
    error,
    messageHistory,
    
    // Actions
    sendMessage,
    changePrompt,
    navigateHistory,
    clearChat,
    
    // API methods
    getStats,
    getChatHistory,
    loadAvailablePrompts
  };
};