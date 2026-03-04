import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Load your CSV file
# Expected CSV columns: id, req_time, resp_time
# You can export this from MySQL Workbench or via CLI
file_path = 'chat_records.csv' 

try:
    df = pd.read_csv(file_path)

    # 2. Pre-processing: Convert strings to actual Datetime objects
    # Handle both formats: "2026-03-03 18:00:28" and "2026-03-03 18:09:32.582"
    # Use format='mixed' to handle different formats in the same column
    df['req_time'] = pd.to_datetime(df['req_time'], format='mixed')
    df['resp_time'] = pd.to_datetime(df['resp_time'], format='mixed')
    
    # Round to seconds for display (remove milliseconds)
    df['req_time_display'] = df['req_time'].dt.floor('s')
    df['resp_time_display'] = df['resp_time'].dt.floor('s')

    # 3. Calculate Duration (Optional, but helps with tooltips)
    df['duration_ms'] = (df['resp_time'] - df['req_time']).dt.total_seconds() * 1000

    # 4. Calculate Concurrency Over Time
    # Create a list of all time events (start and end of each task)
    events = []
    for _, row in df.iterrows():
        events.append({'time': row['req_time'], 'type': 'start'})
        events.append({'time': row['resp_time'], 'type': 'end'})
    
    # Sort events by time
    events_df = pd.DataFrame(events).sort_values('time')
    
    # Calculate concurrency at each time point
    concurrency_timeline = []
    current_concurrency = 0
    
    for _, event in events_df.iterrows():
        if event['type'] == 'start':
            current_concurrency += 1
        else:
            current_concurrency -= 1
        concurrency_timeline.append({
            'time': event['time'],
            'concurrency': current_concurrency
        })
    
    concurrency_df = pd.DataFrame(concurrency_timeline)

    # 5. Create subplot with two rows
    fig = make_subplots(
        rows=2, cols=1,
        # 第一个图占92%，第二个图占8%
        row_heights=[0.92, 0.08],
        subplot_titles=("任务甘特图 (Task Gantt Chart)", "并发任务数 (Concurrent Tasks)"),
        vertical_spacing=0.05
    )

    # 6. Add Gantt Chart (Timeline) to first subplot
    # Create a mapping of task IDs to Y positions
    unique_ids = sorted(df['id'].unique())
    id_to_y = {task_id: idx for idx, task_id in enumerate(unique_ids)}
    
    colors = px.colors.qualitative.Plotly
    bar_height = 0.25  # 设置条形的高度，减小以避免Y轴标签重叠
    
    for idx, row in df.iterrows():
        y_center = id_to_y[row['id']]
        y_bottom = y_center - bar_height
        y_top = y_center + bar_height
        
        fig.add_trace(
            go.Scatter(
                x=[row['req_time_display'], row['resp_time_display'], row['resp_time_display'], row['req_time_display'], row['req_time_display']],
                y=[y_bottom, y_bottom, y_top, y_top, y_bottom],
                fill='toself',
                fillcolor=colors[idx % len(colors)],
                line=dict(color=colors[idx % len(colors)], width=1),
                mode='lines',
                name=str(row['id']),
                text=f"ID: {row['id']}<br> {row['req_time_display'].strftime('%H:%M:%S')}--{row['resp_time_display'].strftime('%H:%M:%S')}<br> 耗时: {row['duration_ms']:.2f}ms",
                hoverinfo='text',
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Update Y-axis to show task IDs at correct positions
    fig.update_yaxes(
        tickmode='array',
        tickvals=[id_to_y[task_id] for task_id in unique_ids],
        ticktext=[str(task_id) for task_id in unique_ids],
        row=1, col=1
    )

    # 7. Add Concurrency Line Chart to second subplot
    fig.add_trace(
        go.Scatter(
            x=concurrency_df['time'],
            y=concurrency_df['concurrency'],
            mode='lines',
            name='并发数',
            line=dict(color='rgb(31, 119, 180)', width=1),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.3)',
            hovertemplate='<b>时间</b>: %{x}<br><b>并发数</b>: %{y}<extra></extra>'
        ),
        row=2, col=1
    )

    # 8. Update Layout
    fig.update_xaxes(
        title_text="时间 (Time)", 
        tickformat='%H:%M:%S',  # 只显示到秒
        row=1, col=1
    )
    fig.update_yaxes(title_text="请求 ID", row=1, col=1)
    fig.update_xaxes(
        title_text="时间轴 (Timeline)", 
        tickformat='%H:%M:%S',  # 只显示到秒
        row=2, col=1
    )
    fig.update_yaxes(title_text="并发任务数", row=2, col=1)
    
    # Generate dynamic title with time range from data
    start_time = df['req_time_display'].min().strftime('%Y-%m-%d %H:%M:%S')
    end_time = df['resp_time_display'].max().strftime('%Y-%m-%d %H:%M:%S')
    
    fig.update_layout(
        height=1400,  # 增加整体高度，让甘特图有更多空间
        title_text=f"并发分析 {start_time} - {end_time}",
        showlegend=False,
        hovermode='x unified'
    )

    # 9. Open in Browser
    fig.show()

except Exception as e:
    print(f"Error: {e}")
