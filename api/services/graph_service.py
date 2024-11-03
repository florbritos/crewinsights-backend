from plotly import graph_objs as go
import re
import numpy as np

class GraphService:
    def __init__(self, langchain_service):
        self.langchain_service = langchain_service

    def generate_graph(self, metric):
        local_vars = {}
        metric += " Using Plotly library for visualization."
        response = self.langchain_service.getAnswer(metric)
        graph_code = response.get('answer', "")

        try:
            python_code = re.search(r"```python(.*?)```", graph_code, re.DOTALL)
            python_code = python_code.group(1).strip() if python_code else graph_code
            cleaned_code = self.clean_code(python_code)
            exec(cleaned_code, {"go": go, "np": np}, local_vars)

            fig = local_vars.get('fig')
            if fig and isinstance(fig, go.Figure):
                self.adjust_figure(fig)

        except Exception as e:
            print(f"ERROR: {e}")
            print("No Python code block found in the provided text.")

        return local_vars.get('fig')

    @staticmethod
    def clean_code(code):
        cleaned_lines = [line for line in code.split('\n') if 'fig.show()' not in line]
        return '\n'.join(line.lstrip() for line in cleaned_lines)
    
    @staticmethod
    def adjust_figure(fig):
        fig.update_layout(
            width=500,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
        )

        fig.update_layout(
            title_font_size=16,
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            legend_font_size=12,
        )