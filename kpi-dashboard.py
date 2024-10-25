import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class KPIDashboard:
    def __init__(self, product_data, milestone_data):
        self.product_data = pd.DataFrame(product_data)
        self.milestone_data = pd.DataFrame(milestone_data)

    def get_total_products(self):
        return len(self.product_data)

    def get_ontrack_launches(self):
        return len(self.product_data[self.product_data['status'] == 'On Track'])

    def get_completion_rate(self):
        completed = self.product_data[['sku_setup_complete', 'marketing_ready', 'inventory_ready']].mean().mean()
        return round(completed * 100, 1)

    def create_timeline_chart(self):
        df = self.product_data.copy()
        df['launch_date'] = pd.to_datetime(df['launch_date'])
        
        fig = px.timeline(
            df,
            x_start='launch_date',
            y='product_name',
            color='status',
            title='Product Launch Timeline'
        )
        
        return fig

    def get_milestone_summary(self):
        return self.milestone_data.groupby('status').size().to_dict()

    def create_milestone_chart(self):
        summary = self.get_milestone_summary()
        
        fig = go.Figure(data=[
            go.Pie(labels=list(summary.keys()),
                  values=list(summary.values()),
                  hole=.3)
        ])
        
        fig.update_layout(title='Milestone Completion Status')
        return fig
