"""
Financial Tools for Portfolio Analysis and Risk Assessment

This module contains LangGraph-compliant financial tools using @tool decorators
and proper invoke() patterns for portfolio analysis, stock information, 
and investment recommendations.
"""

from typing import Union
from langchain_core.tools import tool


@tool  
def calculate_risk(portfolio: str) -> str:
    """
    Calculate portfolio risk score (0-1, where 1 is highest risk).
    
    Args:
        portfolio: Description of the portfolio including asset types
        
    Returns:
        Risk assessment string with score and explanation
        
    Examples:
        - "crypto portfolio with Bitcoin" → "0.8 (HIGH risk)"
        - "government bonds and treasury bills" → "0.2 (LOW risk)"
        - "mixed stocks and bonds" → "0.4 (MODERATE risk)"
    """
    portfolio_lower = portfolio.lower()
    
    if "crypto" in portfolio_lower or "bitcoin" in portfolio_lower or "ethereum" in portfolio_lower:
        return "0.8 (HIGH risk) - Cryptocurrency investments are highly volatile and can experience significant price swings"
    elif "bonds" in portfolio_lower or "treasury" in portfolio_lower or "government" in portfolio_lower:
        return "0.2 (LOW risk) - Government bonds and treasury securities are stable, low-risk investments"
    elif "stocks" in portfolio_lower or "equity" in portfolio_lower or "shares" in portfolio_lower:
        return "0.6 (MODERATE risk) - Stock investments have moderate volatility with potential for good returns"
    elif "mixed" in portfolio_lower or "diversified" in portfolio_lower:
        return "0.4 (MODERATE risk) - Diversified portfolio with balanced risk across asset classes"
    else:
        return "0.4 (MODERATE risk) - Mixed portfolio with balanced risk profile"


@tool
def get_stock_info(symbol: str) -> str:
    """
    Get basic stock information including price, performance, and rating.
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Stock information string with current price, daily change, and rating
        
    Examples:
        - "AAPL" → "Apple Inc. - Current: $150.25, +2.5% today, Strong Buy rating"
        - "INVALID" → "Stock data for INVALID not available in demo database"
    """
    # Demo stock database with realistic-looking data
    stock_database = {
        "AAPL": "Apple Inc. - Current: $150.25, +2.5% today, Strong Buy rating. Tech giant with strong fundamentals",
        "MSFT": "Microsoft Corp. - Current: $300.75, +1.2% today, Buy rating. Cloud computing and software leader", 
        "TSLA": "Tesla Inc. - Current: $200.50, -3.1% today, Hold rating. Electric vehicle and clean energy company",
        "SPY": "S&P 500 ETF - Current: $400.80, +0.8% today. Diversified index fund tracking S&P 500",
        "GOOGL": "Alphabet Inc. - Current: $125.30, +1.8% today, Buy rating. Search and cloud computing giant",
        "AMZN": "Amazon.com Inc. - Current: $135.60, -0.5% today, Buy rating. E-commerce and cloud services leader",
        "NVDA": "NVIDIA Corp. - Current: $450.20, +4.2% today, Strong Buy rating. AI and semiconductor leader",
        "META": "Meta Platforms Inc. - Current: $285.90, +2.1% today, Buy rating. Social media and VR company",
        "BTC": "Bitcoin - Current: $45,200, +3.2% today. Leading cryptocurrency with high volatility",
        "ETH": "Ethereum - Current: $2,850, +2.8% today. Smart contract blockchain platform"
    }
    
    symbol_upper = symbol.upper()
    return stock_database.get(
        symbol_upper, 
        f"Stock data for {symbol_upper} not available in demo database. Try: AAPL, MSFT, TSLA, SPY, GOOGL, AMZN, NVDA, META"
    )


@tool
def portfolio_analyzer(holdings: str) -> str:
    """
    Analyze portfolio diversification and provide investment recommendations.
    
    Args:
        holdings: Description of portfolio holdings, asset allocation, or investment list
        
    Returns:
        Detailed portfolio analysis with diversification assessment, risk level, 
        expected returns, and specific recommendations
        
    Examples:
        - "AAPL, MSFT, Treasury bonds" → Full analysis with recommendations
        - "100% crypto" → Analysis highlighting concentration risk
    """
    holdings_lower = holdings.lower()
    
    # Analyze portfolio composition
    has_stocks = any(term in holdings_lower for term in ["aapl", "msft", "googl", "stocks", "equity", "shares"])
    has_bonds = any(term in holdings_lower for term in ["bonds", "treasury", "government"])
    has_crypto = any(term in holdings_lower for term in ["crypto", "bitcoin", "btc", "ethereum", "eth"])
    has_international = any(term in holdings_lower for term in ["international", "global", "foreign", "emerging"])
    
    # Count different asset types
    asset_types = sum([has_stocks, has_bonds, has_crypto, has_international])
    
    # Determine diversification level
    if asset_types >= 3:
        diversification = "Excellent diversification across multiple asset classes"
        risk_level = "Moderate (0.45/1.0)"
        expected_return = "8-12% annually"
    elif asset_types == 2:
        diversification = "Good diversification with room for improvement"
        risk_level = "Moderate (0.55/1.0)"
        expected_return = "6-10% annually"
    elif has_crypto and asset_types == 1:
        diversification = "Poor diversification - concentrated in high-risk crypto"
        risk_level = "High (0.85/1.0)"
        expected_return = "Highly volatile, -50% to +200% possible"
    elif has_bonds and asset_types == 1:
        diversification = "Conservative but under-diversified"
        risk_level = "Low (0.25/1.0)"
        expected_return = "3-5% annually"
    else:
        diversification = "Limited diversification"
        risk_level = "Moderate (0.50/1.0)"
        expected_return = "5-8% annually"
    
    # Generate specific recommendations
    recommendations = []
    if not has_international:
        recommendations.append("Add 10-15% international exposure for global diversification")
    if not has_bonds and not ("conservative" in holdings_lower):
        recommendations.append("Consider 20-30% bonds for stability and income")
    if has_crypto and "crypto" in holdings_lower and not has_stocks:
        recommendations.append("Reduce crypto concentration, add traditional assets")
    if asset_types < 2:
        recommendations.append("Diversify across multiple asset classes to reduce risk")
    
    recommendations.append("Maintain 6 months emergency fund in high-yield savings")
    recommendations.append("Rebalance quarterly to maintain target allocations")
    
    # Format the analysis
    analysis = f"""Portfolio Analysis for: {holdings}

✅ Diversification Assessment: {diversification}
📊 Risk Level: {risk_level}  
💰 Expected Return: {expected_return}
🎯 Asset Types Identified: {asset_types}/4 major categories

Key Insights:
- Portfolio shows {'strong' if asset_types >= 3 else 'moderate' if asset_types == 2 else 'weak'} diversification
- Risk profile is {'well-balanced' if 2 <= asset_types <= 3 else 'concentrated'}
- {'Good foundation' if asset_types >= 2 else 'Needs broader diversification'} for long-term growth

📋 Recommendations:
{chr(10).join(f'• {rec}' for rec in recommendations)}

⚠️  Disclaimer: This is a demo analysis. Consult licensed financial advisors for personalized advice."""
    
    return analysis.strip()


def get_financial_tools():
    """
    Get all available financial tools for use in chatbot configurations.
    
    Returns:
        List of financial tools with @tool decorators and proper invoke() support
        
    Usage:
        tools = get_financial_tools()
        config = ChatbotConfig(tools=tools, ...)
    """
    return [calculate_risk, get_stock_info, portfolio_analyzer]


# Tool metadata for introspection and documentation
FINANCIAL_TOOLS_INFO = {
    "calculate_risk": {
        "name": "Portfolio Risk Calculator",
        "description": "Calculates risk scores for different portfolio types",
        "category": "risk_assessment",
        "input_type": "portfolio_description"
    },
    "get_stock_info": {
        "name": "Stock Information Lookup", 
        "description": "Retrieves current stock prices and ratings",
        "category": "market_data",
        "input_type": "stock_symbol"
    },
    "portfolio_analyzer": {
        "name": "Portfolio Diversification Analyzer",
        "description": "Analyzes portfolio composition and provides recommendations", 
        "category": "portfolio_analysis",
        "input_type": "holdings_description"
    }
}


def get_tool_info(tool_name: str = None):
    """
    Get information about available financial tools.
    
    Args:
        tool_name: Optional specific tool name, returns all if None
        
    Returns:
        Tool information dictionary or all tools info
    """
    if tool_name:
        return FINANCIAL_TOOLS_INFO.get(tool_name)
    return FINANCIAL_TOOLS_INFO