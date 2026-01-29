"""
Generate Architecture Diagram as JPG
====================================

Creates a visual architecture diagram of the Fraud Management System
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(22, 28))
ax.set_xlim(0, 10)
ax.set_ylim(0, 28)
ax.axis('off')

# Color scheme
color_ui = '#E3F2FD'  # Light blue
color_orchestration = '#FFF3E0'  # Light orange
color_modules = '#E8F5E9'  # Light green
color_data = '#F3E5F5'  # Light purple
color_border = '#1976D2'  # Dark blue
color_text = '#212121'  # Dark gray

# Title
ax.text(5, 27.5, 'FRAUD MANAGEMENT SYSTEM', 
        fontsize=28, fontweight='bold', ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#1976D2', edgecolor='black', linewidth=2),
        color='white')
ax.text(5, 26.5, 'Complete Architecture Diagram', 
        fontsize=16, ha='center', va='top', style='italic', color=color_text)

# ==================== LAYER 1: USER INTERFACES ====================
y_pos = 25

# Layer title
ax.text(5, y_pos, '1. USER INTERFACE LAYER', 
        fontsize=14, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=color_border, alpha=0.8),
        color='white')

# Streamlit Web App
rect1 = FancyBboxPatch((0.5, y_pos-3), 4, 2.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=color_ui, edgecolor=color_border, linewidth=2)
ax.add_patch(rect1)
ax.text(2.5, y_pos-0.8, 'Streamlit Web App\n(app.py)', 
        fontsize=12, fontweight='bold', ha='center', va='top')
ax.text(2.5, y_pos-1.8, '• Dashboard\n• Data Upload\n• Real-time Predictions\n• Visualizations', 
        fontsize=9, ha='center', va='top')

# CLI Interface
rect2 = FancyBboxPatch((5.5, y_pos-3), 4, 2.5, 
                        boxstyle="round,pad=0.1", 
                        facecolor=color_ui, edgecolor=color_border, linewidth=2)
ax.add_patch(rect2)
ax.text(7.5, y_pos-0.8, 'CLI Interface\n(main.py)', 
        fontsize=12, fontweight='bold', ha='center', va='top')
ax.text(7.5, y_pos-1.8, '• Batch Processing\n• Automated Runs\n• Script Execution', 
        fontsize=9, ha='center', va='top')

# Arrows from UI to Orchestration
arrow1 = FancyArrowPatch((2.5, y_pos-3), (5, y_pos-4),
                        arrowstyle='->', mutation_scale=30, 
                        linewidth=2, color=color_border)
ax.add_patch(arrow1)
arrow2 = FancyArrowPatch((7.5, y_pos-3), (5, y_pos-4),
                        arrowstyle='->', mutation_scale=30, 
                        linewidth=2, color=color_border)
ax.add_patch(arrow2)

# ==================== LAYER 2: ORCHESTRATION ====================
y_pos = 20

# Layer title
ax.text(5, y_pos, '2. ORCHESTRATION LAYER', 
        fontsize=14, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=color_border, alpha=0.8),
        color='white')

# Main orchestrator
rect_orch = FancyBboxPatch((0.8, y_pos-2.8), 8.4, 2.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=color_orchestration, edgecolor=color_border, linewidth=3)
ax.add_patch(rect_orch)
ax.text(5, y_pos-0.7, 'AMLComplianceSystem (aml_system.py)', 
        fontsize=13, fontweight='bold', ha='center', va='top')
ax.text(5, y_pos-1.3, 'Main System Orchestrator', 
        fontsize=10, ha='center', va='top', style='italic')
ax.text(5, y_pos-2.0, '• load_data()  • run_complete_analysis()  • predict_risk()  • get_analysis_results()', 
        fontsize=8, ha='center', va='top')

# ==================== LAYER 3: PROCESSING MODULES ====================
y_pos = 15.5

# Layer title
ax.text(5, y_pos, '3. PROCESSING MODULES LAYER', 
        fontsize=14, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=color_border, alpha=0.8),
        color='white')

# Module 1: Data Manager
rect_m1 = FancyBboxPatch((0.3, y_pos-4), 1.8, 3.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_modules, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_m1)
ax.text(1.2, y_pos-0.7, 'DATA\nMANAGER', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(1.2, y_pos-1.6, 'data_manager.py', 
        fontsize=8, ha='center', va='top', style='italic')
ax.text(1.2, y_pos-2.2, '• Load CSV\n• Validate\n• Generate\n  synthetic\n• Clean data', 
        fontsize=7, ha='center', va='top')

# Module 2: Customer Profiler
rect_m2 = FancyBboxPatch((2.3, y_pos-4), 1.8, 3.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_modules, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_m2)
ax.text(3.2, y_pos-0.7, 'CUSTOMER\nPROFILER', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(3.2, y_pos-1.6, 'customer_profiler.py', 
        fontsize=8, ha='center', va='top', style='italic')
ax.text(3.2, y_pos-2.2, '• Analyze\n• Create\n  profiles\n• Risk scores\n• Classify', 
        fontsize=7, ha='center', va='top')

# Module 3: Anomaly Detector
rect_m3 = FancyBboxPatch((4.3, y_pos-4), 1.8, 3.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_modules, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_m3)
ax.text(5.2, y_pos-0.7, 'ANOMALY\nDETECTOR', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(5.2, y_pos-1.6, 'anomaly_detector.py', 
        fontsize=8, ha='center', va='top', style='italic')
ax.text(5.2, y_pos-2.2, '• Features\n• Isolation\n  Forest\n• Statistical\n• Scoring', 
        fontsize=7, ha='center', va='top')

# Module 4: ML Predictor
rect_m4 = FancyBboxPatch((6.3, y_pos-4), 1.8, 3.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_modules, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_m4)
ax.text(7.2, y_pos-0.7, 'ML\nPREDICTOR', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(7.2, y_pos-1.6, 'ml_predictor.py', 
        fontsize=8, ha='center', va='top', style='italic')
ax.text(7.2, y_pos-2.2, '• Train\n• Random\n  Forest\n• Gradient\n  Boosting\n• Predict', 
        fontsize=7, ha='center', va='top')

# Module 5: Visualizer (wider, below others)
rect_m5 = FancyBboxPatch((1.5, y_pos-6.2), 7, 1.8, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_modules, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_m5)
ax.text(5, y_pos-5, 'VISUALIZER (visualizer.py)', 
        fontsize=11, fontweight='bold', ha='center', va='top')
ax.text(5, y_pos-5.7, '• Comprehensive Reports  • Heatmaps  • Network Graphs  • Time Series  • Feature Importance', 
        fontsize=8, ha='center', va='top')

# Arrows from orchestration to modules
for x in [1.2, 3.2, 5.2, 7.2]:
    arrow = FancyArrowPatch((5, 17.2), (x, y_pos),
                           arrowstyle='->', mutation_scale=20, 
                           linewidth=1.5, color=color_border)
    ax.add_patch(arrow)

# Arrows from modules to visualizer
for x in [1.2, 3.2, 5.2, 7.2]:
    arrow = FancyArrowPatch((x, y_pos-4), (5, y_pos-4.4),
                           arrowstyle='->', mutation_scale=15, 
                           linewidth=1, color=color_border, alpha=0.5)
    ax.add_patch(arrow)

# ==================== LAYER 4: DATA STORAGE ====================
y_pos = 8

# Layer title
ax.text(5, y_pos, '4. DATA STORAGE LAYER', 
        fontsize=14, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=color_border, alpha=0.8),
        color='white')

# Input Data
rect_d1 = FancyBboxPatch((0.5, y_pos-3), 2, 2.8, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_data, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_d1)
ax.text(1.5, y_pos-0.6, 'INPUT DATA', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(1.5, y_pos-1.3, '• CSV files\n• Google Drive\n• Direct uploads\n• Synthetic data', 
        fontsize=8, ha='center', va='top')

# Output Files
rect_d2 = FancyBboxPatch((2.8, y_pos-3), 2, 2.8, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_data, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_d2)
ax.text(3.8, y_pos-0.6, 'OUTPUT FILES', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(3.8, y_pos-1.3, '• customer_\n  profiles.csv\n• detected_\n  anomalies.csv\n• visualizations', 
        fontsize=8, ha='center', va='top')

# Models Folder
rect_d3 = FancyBboxPatch((5.2, y_pos-3), 2, 2.8, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_data, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_d3)
ax.text(6.2, y_pos-0.6, 'MODELS', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(6.2, y_pos-1.3, '• ml_model.pkl\n• scaler.pkl\n• encoders.pkl\n(Pickle format)', 
        fontsize=8, ha='center', va='top')

# Config Files
rect_d4 = FancyBboxPatch((7.5, y_pos-3), 2, 2.8, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_data, edgecolor=color_border, linewidth=2)
ax.add_patch(rect_d4)
ax.text(8.5, y_pos-0.6, 'CONFIG', 
        fontsize=10, fontweight='bold', ha='center', va='top')
ax.text(8.5, y_pos-1.3, '• config.py\n• Paths\n• Thresholds\n• Parameters', 
        fontsize=8, ha='center', va='top')

# Arrow from modules to data storage
arrow_data = FancyArrowPatch((5, 9.5), (5, y_pos),
                            arrowstyle='<->', mutation_scale=25, 
                            linewidth=2, color=color_border)
ax.add_patch(arrow_data)

# ==================== DATA FLOW SECTION ====================
y_pos = 3

ax.text(5, y_pos, 'DATA FLOW PIPELINE', 
        fontsize=13, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FF6F00', alpha=0.8),
        color='white')

# Data flow boxes
flow_boxes = [
    (0.5, 'Data\nIngestion'),
    (2, 'Customer\nProfiling'),
    (3.5, 'Anomaly\nDetection'),
    (5, 'ML\nPrediction'),
    (6.5, 'Visualiza-\ntion'),
    (8, 'Output &\nResults')
]

for i, (x, label) in enumerate(flow_boxes):
    rect = FancyBboxPatch((x, 0.5), 1.2, 1.2, 
                          boxstyle="round,pad=0.05", 
                          facecolor='#FFE082', edgecolor='#FF6F00', linewidth=2)
    ax.add_patch(rect)
    ax.text(x+0.6, 1.1, label, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrow to next box
    if i < len(flow_boxes) - 1:
        arrow = FancyArrowPatch((x+1.2, 1.1), (flow_boxes[i+1][0], 1.1),
                               arrowstyle='->', mutation_scale=15, 
                               linewidth=2, color='#FF6F00')
        ax.add_patch(arrow)

# ==================== LEGEND ====================
legend_elements = [
    mpatches.Patch(facecolor=color_ui, edgecolor=color_border, label='User Interface'),
    mpatches.Patch(facecolor=color_orchestration, edgecolor=color_border, label='Orchestration'),
    mpatches.Patch(facecolor=color_modules, edgecolor=color_border, label='Processing Modules'),
    mpatches.Patch(facecolor=color_data, edgecolor=color_border, label='Data Storage'),
    mlines.Line2D([], [], color=color_border, marker='>', markersize=10, label='Data Flow', linewidth=2)
]

ax.legend(handles=legend_elements, loc='lower center', ncol=5, 
          fontsize=9, frameon=True, fancybox=True, shadow=True)

# Save as JPG
plt.tight_layout()
plt.savefig('ARCHITECTURE_DIAGRAM.jpg', format='jpg', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("✓ Architecture diagram saved as 'ARCHITECTURE_DIAGRAM.jpg'")
print(f"  Resolution: 300 DPI")
print(f"  Format: JPG")
print(f"  Size: ~6000 x 7200 pixels")

# Also save as PNG for better quality
plt.savefig('ARCHITECTURE_DIAGRAM.png', format='png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("\n✓ High-quality version also saved as 'ARCHITECTURE_DIAGRAM.png'")

plt.show()
