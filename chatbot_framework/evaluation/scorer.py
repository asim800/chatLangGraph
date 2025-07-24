"""
Interaction scoring and evaluation framework for chatbot performance
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import statistics
from dataclasses import dataclass


@dataclass
class EvaluationMetric:
    name: str
    description: str
    weight: float
    score_function: Callable[[Dict[str, Any]], float]


class InteractionScorer:
    def __init__(self):
        self.metrics = self._initialize_default_metrics()
        self.custom_metrics = {}
    
    def _initialize_default_metrics(self) -> Dict[str, EvaluationMetric]:
        """Initialize default engagement and quality metrics"""
        return {
            "conversation_length": EvaluationMetric(
                name="Conversation Length",
                description="Measures the number of exchanges in a conversation",
                weight=0.2,
                score_function=self._score_conversation_length
            ),
            "response_quality": EvaluationMetric(
                name="Response Quality",
                description="Measures response relevance and helpfulness",
                weight=0.3,
                score_function=self._score_response_quality
            ),
            "user_engagement": EvaluationMetric(
                name="User Engagement",
                description="Measures user's active participation",
                weight=0.2,
                score_function=self._score_user_engagement
            ),
            "conversation_flow": EvaluationMetric(
                name="Conversation Flow",
                description="Measures natural conversation progression",
                weight=0.15,
                score_function=self._score_conversation_flow
            ),
            "stickiness": EvaluationMetric(
                name="Stickiness",
                description="Measures user's return behavior and session duration",
                weight=0.15,
                score_function=self._score_stickiness
            )
        }
    
    def _score_conversation_length(self, interaction: Dict[str, Any]) -> float:
        """Score based on conversation length (more exchanges = higher score)"""
        message_count = len(interaction["messages"])
        # Normalize to 0-1 scale, with diminishing returns after 20 messages
        return min(1.0, message_count / 20.0)
    
    def _score_response_quality(self, interaction: Dict[str, Any]) -> float:
        """Score response quality based on length, complexity, and user feedback"""
        ai_messages = [msg for msg in interaction["messages"] if msg["role"] == "assistant"]
        
        if not ai_messages:
            return 0.0
        
        # Average response length (normalized)
        avg_length = statistics.mean(len(msg["content"]) for msg in ai_messages)
        length_score = min(1.0, avg_length / 500.0)  # Normalize to 500 chars
        
        # Check for questions (engagement indicator)
        question_count = sum(1 for msg in ai_messages if "?" in msg["content"])
        question_score = min(1.0, question_count / len(ai_messages))
        
        # Combine scores
        return (length_score * 0.6) + (question_score * 0.4)
    
    def _score_user_engagement(self, interaction: Dict[str, Any]) -> float:
        """Score user engagement based on response patterns"""
        user_messages = [msg for msg in interaction["messages"] if msg["role"] == "user"]
        
        if not user_messages:
            return 0.0
        
        # Average user message length
        avg_length = statistics.mean(len(msg["content"]) for msg in user_messages)
        length_score = min(1.0, avg_length / 100.0)  # Normalize to 100 chars
        
        # Response rate (did user respond to AI questions?)
        ai_questions = sum(1 for msg in interaction["messages"] 
                          if msg["role"] == "assistant" and "?" in msg["content"])
        user_responses = len(user_messages) - 1  # Exclude initial message
        
        response_rate = min(1.0, user_responses / max(1, ai_questions))
        
        return (length_score * 0.4) + (response_rate * 0.6)
    
    def _score_conversation_flow(self, interaction: Dict[str, Any]) -> float:
        """Score natural conversation progression"""
        messages = interaction["messages"]
        
        if len(messages) < 2:
            return 0.0
        
        # Check for alternating user/assistant pattern
        pattern_score = 1.0
        for i in range(1, len(messages)):
            prev_role = messages[i-1]["role"]
            curr_role = messages[i]["role"]
            if prev_role == curr_role:  # Same role speaking twice
                pattern_score -= 0.1
        
        pattern_score = max(0.0, pattern_score)
        
        # Check timing between messages (if available)
        timing_score = 1.0
        for i in range(1, len(messages)):
            if "timestamp" in messages[i] and "timestamp" in messages[i-1]:
                try:
                    curr_time = datetime.fromisoformat(messages[i]["timestamp"])
                    prev_time = datetime.fromisoformat(messages[i-1]["timestamp"])
                    gap = (curr_time - prev_time).total_seconds()
                    
                    # Penalize very long gaps (>10 minutes) or very short gaps (<1 second)
                    if gap > 600 or gap < 1:
                        timing_score -= 0.05
                except:
                    pass
        
        timing_score = max(0.0, timing_score)
        
        return (pattern_score * 0.7) + (timing_score * 0.3)
    
    def _score_stickiness(self, interaction: Dict[str, Any]) -> float:
        """Score conversation stickiness and engagement retention"""
        # Use the engagement_score if available
        engagement_score = interaction.get("engagement_score", 0.0)
        
        # Calculate session duration
        messages = interaction["messages"]
        if len(messages) >= 2 and "timestamp" in messages[0] and "timestamp" in messages[-1]:
            try:
                start_time = datetime.fromisoformat(messages[0]["timestamp"])
                end_time = datetime.fromisoformat(messages[-1]["timestamp"])
                duration_minutes = (end_time - start_time).total_seconds() / 60.0
                
                # Normalize duration score (optimal around 5-15 minutes)
                if duration_minutes <= 15:
                    duration_score = duration_minutes / 15.0
                else:
                    duration_score = max(0.5, 1.0 - (duration_minutes - 15) / 30.0)
            except:
                duration_score = 0.5
        else:
            duration_score = 0.5
        
        return (engagement_score * 0.6) + (duration_score * 0.4)
    
    def add_custom_metric(self, metric: EvaluationMetric):
        """Add a custom evaluation metric"""
        self.custom_metrics[metric.name] = metric
    
    def score_interaction(self, interaction: Dict[str, Any]) -> Dict[str, float]:
        """Score a single interaction across all metrics"""
        scores = {}
        
        # Score default metrics
        for name, metric in self.metrics.items():
            try:
                score = metric.score_function(interaction)
                scores[name] = max(0.0, min(1.0, score))  # Clamp to [0, 1]
            except Exception as e:
                print(f"Error scoring metric {name}: {e}")
                scores[name] = 0.0
        
        # Score custom metrics
        for name, metric in self.custom_metrics.items():
            try:
                score = metric.score_function(interaction)
                scores[name] = max(0.0, min(1.0, score))
            except Exception as e:
                print(f"Error scoring custom metric {name}: {e}")
                scores[name] = 0.0
        
        return scores
    
    def calculate_overall_score(self, metric_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        total_weight = 0.0
        weighted_sum = 0.0
        
        # Default metrics
        for name, metric in self.metrics.items():
            if name in metric_scores:
                weighted_sum += metric_scores[name] * metric.weight
                total_weight += metric.weight
        
        # Custom metrics
        for name, metric in self.custom_metrics.items():
            if name in metric_scores:
                weighted_sum += metric_scores[name] * metric.weight
                total_weight += metric.weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def evaluate_interactions(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate multiple interactions and provide summary statistics"""
        if not interactions:
            return {"error": "No interactions to evaluate"}
        
        all_scores = []
        metric_summaries = {}
        
        # Initialize metric summaries
        for metric_name in list(self.metrics.keys()) + list(self.custom_metrics.keys()):
            metric_summaries[metric_name] = []
        
        # Score each interaction
        for interaction in interactions:
            scores = self.score_interaction(interaction)
            overall_score = self.calculate_overall_score(scores)
            
            scores["overall"] = overall_score
            all_scores.append(scores)
            
            # Collect scores for summaries
            for metric_name, score in scores.items():
                if metric_name in metric_summaries:
                    metric_summaries[metric_name].append(score)
        
        # Calculate summary statistics
        summary = {
            "total_interactions": len(interactions),
            "metric_statistics": {}
        }
        
        for metric_name, scores in metric_summaries.items():
            if scores:
                summary["metric_statistics"][metric_name] = {
                    "mean": statistics.mean(scores),
                    "median": statistics.median(scores),
                    "std_dev": statistics.stdev(scores) if len(scores) > 1 else 0.0,
                    "min": min(scores),
                    "max": max(scores)
                }
        
        # Add overall score if calculated
        if all_scores and "overall" in all_scores[0]:
            overall_scores = [s["overall"] for s in all_scores]
            summary["metric_statistics"]["overall"] = {
                "mean": statistics.mean(overall_scores),
                "median": statistics.median(overall_scores),
                "std_dev": statistics.stdev(overall_scores) if len(overall_scores) > 1 else 0.0,
                "min": min(overall_scores),
                "max": max(overall_scores)
            }
        
        summary["individual_scores"] = all_scores
        return summary
    
    def get_improvement_suggestions(self, evaluation_results: Dict[str, Any]) -> List[str]:
        """Generate suggestions based on evaluation results"""
        suggestions = []
        
        if "metric_statistics" not in evaluation_results:
            return suggestions
        
        stats = evaluation_results["metric_statistics"]
        
        # Check each metric for improvement opportunities
        if "conversation_length" in stats and stats["conversation_length"]["mean"] < 0.5:
            suggestions.append("Consider asking more follow-up questions to extend conversations")
        
        if "response_quality" in stats and stats["response_quality"]["mean"] < 0.6:
            suggestions.append("Improve response quality by providing more detailed and helpful answers")
        
        if "user_engagement" in stats and stats["user_engagement"]["mean"] < 0.5:
            suggestions.append("Encourage more user participation with engaging questions and prompts")
        
        if "conversation_flow" in stats and stats["conversation_flow"]["mean"] < 0.7:
            suggestions.append("Work on maintaining natural conversation flow and timing")
        
        if "stickiness" in stats and stats["stickiness"]["mean"] < 0.5:
            suggestions.append("Focus on building rapport and creating memorable interactions")
        
        return suggestions