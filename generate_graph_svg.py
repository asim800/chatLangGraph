#!/usr/bin/env python3
"""
Generate SVG visualization of the chatbot agent graph structure
"""

def generate_chatbot_graph_svg():
    """Generate SVG representation of the chatbot graph"""
    
    # Graph structure from _build_graph method
    nodes = [
        {"id": "process_input", "label": "Process Input", "x": 150, "y": 50},
        {"id": "generate_response", "label": "Generate Response", "x": 150, "y": 150},
        {"id": "update_engagement", "label": "Update Engagement", "x": 150, "y": 250},
        {"id": "store_interaction", "label": "Store Interaction", "x": 150, "y": 350},
        {"id": "END", "label": "END", "x": 150, "y": 450}
    ]
    
    edges = [
        ("process_input", "generate_response"),
        ("generate_response", "update_engagement"),
        ("update_engagement", "store_interaction"),
        ("store_interaction", "END")
    ]
    
    # SVG dimensions
    width = 300
    height = 500
    
    # Start SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" 
            refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
    </marker>
    <style>
      .node {{
        fill: #e1f5fe;
        stroke: #0277bd;
        stroke-width: 2;
        rx: 8;
      }}
      .node-text {{
        font-family: Arial, sans-serif;
        font-size: 12px;
        text-anchor: middle;
        dominant-baseline: middle;
        fill: #01579b;
      }}
      .edge {{
        stroke: #333;
        stroke-width: 2;
        marker-end: url(#arrowhead);
      }}
      .start-node {{
        fill: #c8e6c9;
        stroke: #2e7d32;
      }}
      .end-node {{
        fill: #ffcdd2;
        stroke: #c62828;
      }}
      .title {{
        font-family: Arial, sans-serif;
        font-size: 16px;
        font-weight: bold;
        text-anchor: middle;
        fill: #333;
      }}
    </style>
  </defs>
  
  <!-- Title -->
  <text x="{width//2}" y="25" class="title">Chatbot Agent Graph Flow</text>
  
'''
    
    # Create node lookup for positioning
    node_positions = {node["id"]: (node["x"], node["y"]) for node in nodes}
    
    # Draw edges first (so they appear behind nodes)
    for source, target in edges:
        source_x, source_y = node_positions[source]
        target_x, target_y = node_positions[target]
        
        # Adjust start and end points to connect to node edges
        if source_y < target_y:  # Vertical flow downward
            start_y = source_y + 25
            end_y = target_y - 25
        else:
            start_y = source_y - 25
            end_y = target_y + 25
            
        svg_content += f'  <line x1="{source_x}" y1="{start_y}" x2="{target_x}" y2="{end_y}" class="edge" />\n'
    
    # Draw nodes
    for node in nodes:
        node_class = "node"
        if node["id"] == "process_input":
            node_class += " start-node"
        elif node["id"] == "END":
            node_class += " end-node"
            
        # Node rectangle
        svg_content += f'  <rect x="{node["x"] - 60}" y="{node["y"] - 25}" width="120" height="50" class="{node_class}" />\n'
        
        # Node text
        svg_content += f'  <text x="{node["x"]}" y="{node["y"]}" class="node-text">{node["label"]}</text>\n'
    
    # Close SVG
    svg_content += '</svg>'
    
    return svg_content

if __name__ == "__main__":
    svg_content = generate_chatbot_graph_svg()
    
    # Save to file
    with open("chatbot_graph.svg", "w") as f:
        f.write(svg_content)
    
    print("Generated chatbot_graph.svg successfully!")