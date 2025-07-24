import React, { useState, useRef, useEffect } from 'react';
import { useChat } from '../hooks/useChat';

const ReactPatternStep = ({ step }) => {
  const getStepStyle = (type) => {
    const baseStyle = "mb-2 p-3 border-l-4 rounded-r-md";
    
    switch (type) {
      case 'question':
        return `${baseStyle} border-blue-500 bg-blue-50 text-blue-900`;
      case 'thought':
        return `${baseStyle} border-purple-500 bg-purple-50 text-purple-900`;
      case 'action':
        return `${baseStyle} border-yellow-500 bg-yellow-50 text-yellow-900`;
      case 'action_input':
        return `${baseStyle} border-green-500 bg-green-50 text-green-900`;
      case 'observation':
        return `${baseStyle} border-cyan-500 bg-cyan-50 text-cyan-900`;
      case 'final_answer':
        return `${baseStyle} border-red-500 bg-red-50 text-red-900 font-medium mt-4 p-4`;
      default:
        return `${baseStyle} border-gray-300 bg-gray-50`;
    }
  };

  const getStepIcon = (type) => {
    switch (type) {
      case 'question': return '❓';
      case 'thought': return '🤔';
      case 'action': return '⚡';
      case 'action_input': return '📥';
      case 'observation': return '👁️';
      case 'final_answer': return '✅';
      default: return '•';
    }
  };

  const getStepLabel = (type) => {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  return (
    <div className={getStepStyle(step.type)}>
      <span className="font-bold">
        {getStepIcon(step.type)} {getStepLabel(step.type)}:
      </span>
      <span className="ml-2 whitespace-pre-wrap">{step.content}</span>
    </div>
  );
};

const Message = ({ message }) => {
  const parseReactPattern = (content) => {
    const steps = [];
    const lines = content.split('\n');
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      if (line.startsWith('Question:')) {
        steps.push({ type: 'question', content: line.substring(9).trim() });
      } else if (line.startsWith('Thought:')) {
        steps.push({ type: 'thought', content: line.substring(8).trim() });
      } else if (line.startsWith('Action:')) {
        steps.push({ type: 'action', content: line.substring(7).trim() });
      } else if (line.startsWith('Action Input:')) {
        let actionInput = line.substring(13).trim();
        // Handle multiline action input
        for (let j = i + 1; j < lines.length; j++) {
          const nextLine = lines[j].trim();
          if (nextLine.startsWith('Observation:') || nextLine.startsWith('Thought:') || 
              nextLine.startsWith('Action:') || nextLine.startsWith('Final Answer:')) {
            break;
          }
          if (nextLine) {
            actionInput += '\n' + nextLine;
            i = j;
          }
        }
        steps.push({ type: 'action_input', content: actionInput });
      } else if (line.startsWith('Observation:')) {
        steps.push({ type: 'observation', content: line.substring(12).trim() });
      } else if (line.startsWith('Final Answer:')) {
        let finalAnswer = line.substring(13).trim();
        // Handle multiline final answer
        for (let j = i + 1; j < lines.length; j++) {
          const nextLine = lines[j].trim();
          if (nextLine) {
            finalAnswer += '\n' + nextLine;
            i = j;
          }
        }
        steps.push({ type: 'final_answer', content: finalAnswer });
      }
    }
    
    return steps;
  };

  const isReactPattern = message.isReactPattern || 
    (message.sender === 'bot' && 
     (message.content.includes('Thought:') || message.content.includes('Action:')));

  return (
    <div className={`mb-4 ${
      message.sender === 'user' ? 'text-right' : 'text-left'
    }`}>
      <div className={`inline-block max-w-3xl p-3 rounded-lg ${
        message.sender === 'user' 
          ? 'bg-blue-500 text-white ml-auto' 
          : message.sender === 'system'
          ? 'bg-gray-200 text-gray-700'
          : 'bg-white border border-gray-200 text-gray-900'
      } ${message.isError ? 'bg-red-100 border-red-300 text-red-700' : ''}`}>
        
        <div className="font-semibold text-sm mb-2">
          {message.sender === 'user' ? 'You' : 
           message.sender === 'system' ? 'System' : 'AI Assistant'}
        </div>
        
        {isReactPattern ? (
          <div className="react-pattern">
            {parseReactPattern(message.content).map((step, index) => (
              <ReactPatternStep key={index} step={step} />
            ))}
          </div>
        ) : (
          <div className="whitespace-pre-wrap">{message.content}</div>
        )}
        
        {message.engagementScore && (
          <div className="text-xs text-gray-500 mt-2">
            💯 Engagement: {message.engagementScore.toFixed(2)}
          </div>
        )}
        
        <div className="text-xs text-gray-400 mt-1">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

const ChatInterface = ({ className = '', userId = 'web_user' }) => {
  const {
    messages,
    isLoading,
    sessionId,
    currentPrompt,
    availablePrompts,
    error,
    sendMessage,
    changePrompt,
    navigateHistory,
    clearChat
  } = useChat();

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-resize textarea
  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = 
        Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      sendMessage(inputValue.trim(), userId);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        // Allow new line with Shift+Enter
        return;
      } else {
        // Send message with Enter
        e.preventDefault();
        handleSubmit(e);
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const historyMessage = navigateHistory('up');
      if (historyMessage !== null) {
        setInputValue(historyMessage);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      const historyMessage = navigateHistory('down');
      if (historyMessage !== null) {
        setInputValue(historyMessage);
      }
    }
  };

  return (
    <div className={`flex flex-col h-full max-w-4xl mx-auto ${className}`}>
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 rounded-t-lg">
        <h1 className="text-xl font-bold">🤖 AI Chat Assistant</h1>
        <div className="flex items-center gap-4 mt-2 text-sm">
          <span>Session: {sessionId ? sessionId.slice(0, 8) + '...' : 'New'}</span>
          <select
            value={currentPrompt}
            onChange={(e) => changePrompt(e.target.value)}
            className="bg-blue-500 text-white border border-blue-400 rounded px-2 py-1"
          >
            {availablePrompts.map(prompt => (
              <option key={prompt} value={prompt}>
                {prompt.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </option>
            ))}
          </select>
          <button
            onClick={clearChat}
            className="bg-blue-500 hover:bg-blue-400 px-3 py-1 rounded text-sm"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 min-h-0">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p>Welcome! Start a conversation by typing a message below.</p>
            {currentPrompt === 'react_prompt' && (
              <p className="mt-2 text-sm">
                React Pattern mode will show step-by-step AI reasoning.
              </p>
            )}
          </div>
        )}
        
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="text-center text-gray-500">
            <div className="inline-flex items-center gap-2">
              <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
              🤔 Thinking...
            </div>
          </div>
        )}
        
        {error && (
          <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded mb-4">
            Error: {error}
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 bg-white border-t">
        <div className="flex gap-2">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message... (Enter to send, Shift+Enter for new line, ↑↓ for history)"
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none min-h-[44px] max-h-[120px]"
            rows={1}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed whitespace-nowrap"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;