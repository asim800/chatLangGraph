"""
File-based interaction storage system for chatbot conversations
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid


class InteractionStore:
    def __init__(self, storage_path: str = "interactions"):
        self.storage_path = storage_path
        self.conversations_path = os.path.join(storage_path, "conversations")
        self.interactions_path = os.path.join(storage_path, "interactions")
        self.system_prompts_path = os.path.join(storage_path, "system_prompts")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create storage directories if they don't exist"""
        os.makedirs(self.conversations_path, exist_ok=True)
        os.makedirs(self.interactions_path, exist_ok=True)
        os.makedirs(self.system_prompts_path, exist_ok=True)
    
    def store_interaction(self, interaction_data: Dict[str, Any]) -> str:
        """Store a single interaction"""
        interaction_id = str(uuid.uuid4())
        interaction_data["interaction_id"] = interaction_id
        
        # Store individual interaction
        interaction_file = os.path.join(
            self.interactions_path, 
            f"{interaction_data['user_id']}_{interaction_data['session_id']}_{interaction_id}.json"
        )
        
        with open(interaction_file, 'w') as f:
            json.dump(interaction_data, f, indent=2, default=str)
        
        # Update conversation file
        self._update_conversation(interaction_data)
        
        return interaction_id
    
    def _update_conversation(self, interaction_data: Dict[str, Any]):
        """Update the ongoing conversation file"""
        conversation_file = os.path.join(
            self.conversations_path,
            f"{interaction_data['user_id']}_{interaction_data['session_id']}.json"
        )
        
        conversation_data = {
            "user_id": interaction_data["user_id"],
            "session_id": interaction_data["session_id"],
            "messages": interaction_data["messages"],
            "context": interaction_data.get("context", {}),
            "last_engagement_score": interaction_data.get("engagement_score", 0.0),
            "last_updated": interaction_data["timestamp"],
            "message_count": len(interaction_data["messages"])
        }
        
        with open(conversation_file, 'w') as f:
            json.dump(conversation_data, f, indent=2, default=str)
    
    def get_conversation(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an existing conversation"""
        conversation_file = os.path.join(
            self.conversations_path,
            f"{user_id}_{session_id}.json"
        )
        
        if os.path.exists(conversation_file):
            with open(conversation_file, 'r') as f:
                return json.load(f)
        
        return None
    
    def store_system_prompt(self, system_prompt: str, session_id: str = None) -> str:
        """Store a system prompt for the current session"""
        prompt_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        prompt_data = {
            "prompt_id": prompt_id,
            "system_prompt": system_prompt,
            "session_id": session_id,
            "timestamp": timestamp
        }
        
        # Store system prompt
        prompt_file = os.path.join(
            self.system_prompts_path,
            f"{session_id or 'default'}_{prompt_id}.json"
        )
        
        with open(prompt_file, 'w') as f:
            json.dump(prompt_data, f, indent=2, default=str)
        
        return prompt_id
    
    def get_system_prompt(self, session_id: str = None) -> Optional[str]:
        """Retrieve the most recent system prompt for a session"""
        prompts = []
        
        for filename in os.listdir(self.system_prompts_path):
            if filename.endswith(".json"):
                if session_id and not filename.startswith(f"{session_id}_"):
                    continue
                
                with open(os.path.join(self.system_prompts_path, filename), 'r') as f:
                    prompt_data = json.load(f)
                    prompts.append(prompt_data)
        
        if prompts:
            # Return the most recent prompt
            prompts.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return prompts[0]["system_prompt"]
        
        return None
    
    def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all conversations for a specific user"""
        conversations = []
        
        for filename in os.listdir(self.conversations_path):
            if filename.startswith(f"{user_id}_") and filename.endswith(".json"):
                with open(os.path.join(self.conversations_path, filename), 'r') as f:
                    conversations.append(json.load(f))
        
        # Sort by last updated
        conversations.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
        return conversations
    
    def get_interactions_for_evaluation(self, 
                                       start_date: Optional[datetime] = None,
                                       end_date: Optional[datetime] = None,
                                       user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get interactions for evaluation and scoring"""
        interactions = []
        
        for filename in os.listdir(self.interactions_path):
            if filename.endswith(".json"):
                # Parse user_id from filename if filtering by user
                if user_id and not filename.startswith(f"{user_id}_"):
                    continue
                
                with open(os.path.join(self.interactions_path, filename), 'r') as f:
                    interaction = json.load(f)
                    
                    # Filter by date if specified
                    if start_date or end_date:
                        interaction_date = datetime.fromisoformat(interaction["timestamp"])
                        if start_date and interaction_date < start_date:
                            continue
                        if end_date and interaction_date > end_date:
                            continue
                    
                    interactions.append(interaction)
        
        return interactions
    
    def get_engagement_metrics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Calculate engagement metrics from stored interactions"""
        interactions = self.get_interactions_for_evaluation(user_id=user_id)
        
        if not interactions:
            return {"total_interactions": 0}
        
        total_interactions = len(interactions)
        avg_engagement_score = sum(i.get("engagement_score", 0) for i in interactions) / total_interactions
        
        # Count unique users and sessions
        unique_users = len(set(i["user_id"] for i in interactions))
        unique_sessions = len(set(i["session_id"] for i in interactions))
        
        # Calculate message statistics
        total_messages = sum(len(i["messages"]) for i in interactions)
        avg_messages_per_session = total_messages / unique_sessions if unique_sessions > 0 else 0
        
        return {
            "total_interactions": total_interactions,
            "unique_users": unique_users,
            "unique_sessions": unique_sessions,
            "avg_engagement_score": avg_engagement_score,
            "total_messages": total_messages,
            "avg_messages_per_session": avg_messages_per_session
        }
    
    def export_interactions(self, 
                           output_file: str,
                           format_type: str = "json",
                           user_id: Optional[str] = None) -> str:
        """Export interactions to file for analysis"""
        interactions = self.get_interactions_for_evaluation(user_id=user_id)
        
        if format_type == "json":
            with open(output_file, 'w') as f:
                json.dump(interactions, f, indent=2, default=str)
        elif format_type == "csv":
            import pandas as pd
            
            # Flatten interactions for CSV
            flattened = []
            for interaction in interactions:
                base_data = {
                    "interaction_id": interaction.get("interaction_id"),
                    "user_id": interaction["user_id"],
                    "session_id": interaction["session_id"],
                    "timestamp": interaction["timestamp"],
                    "engagement_score": interaction.get("engagement_score", 0),
                    "message_count": len(interaction["messages"])
                }
                
                # Add each message as a separate row
                for i, msg in enumerate(interaction["messages"]):
                    row = base_data.copy()
                    row.update({
                        "message_index": i,
                        "message_role": msg["role"],
                        "message_content": msg["content"],
                        "message_timestamp": msg.get("timestamp", ""),
                        "message_id": msg.get("message_id", "")
                    })
                    flattened.append(row)
            
            df = pd.DataFrame(flattened)
            df.to_csv(output_file, index=False)
        
        return output_file