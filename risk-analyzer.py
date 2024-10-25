import pandas as pd
import plotly.graph_objects as go

class RiskAnalyzer:
    def __init__(self, risk_data):
        self.risk_data = pd.DataFrame(risk_data)

    def calculate_risk_score(self):
        self.risk_data['risk_score'] = (
            self.risk_data['probability'] * self.risk_data['impact']
        )
        return self.risk_data

    def get_top_risks(self, n=5):
        scored_risks = self.calculate_risk_score()
        return scored_risks.nlargest(n, 'risk_score')[
            ['risk_description', 'probability', 'impact', 'risk_score', 'mitigation_strategy']
        ]

    def create_risk_matrix(self):
        df = self.risk_data

        # Create risk matrix
        fig = go.Figure()

        # Add risks as scatter points
        fig.add_trace(go.Scatter(
            x=df['probability'],
            y=df['impact'],
            mode='markers+text',
            text=df['risk_description'],
            textposition="top center",
            marker=dict(
                size=12,
                color=df['probability'] * df['impact'],
                colorscale='RdYlGn_r',
                showscale=True
            ),
            name='Risks'
        ))

        # Update layout
        fig.update_layout(
            title='Risk Matrix',
            xaxis_title='Probability',
            yaxis_title='Impact',
            showlegend=False
        )

        # Add quadrant lines
        fig.add_hline(y=2.5, line_dash="dash", line_color="gray")
        fig.add_vline(x=2.5, line_dash="dash", line_color="gray")

        return fig

    def get_risk_summary(self):
        scored_risks = self.calculate_risk_score()
        return {
            'total_risks': len(scored_risks),
            'high_risks': len(scored_risks[scored_risks['risk_score'] >= 15]),
            'medium_risks': len(scored_risks[
                (scored_risks['risk_score'] >= 8) & 
                (scored_risks['risk_score'] < 15)
            ]),
            'low_risks': len(scored_risks[scored_risks['risk_score'] < 8])
        }
