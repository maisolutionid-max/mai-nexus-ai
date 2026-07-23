"""
Dashboard Service
"""

class DashboardService:

    def get_dashboard(self):
        return {
            "today_orders": 0,
            "today_income": 0,
            "customers": 0,
            "machines": 0
        }
