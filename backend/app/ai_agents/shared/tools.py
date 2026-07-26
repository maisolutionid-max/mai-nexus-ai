class AgentTools:

    @staticmethod
    def summarize(data):
        return {
            "total_records": len(data)
        }

    @staticmethod
    def average(values):
        if not values:
            return 0

        return sum(values) / len(values)

    @staticmethod
    def maximum(values):
        if not values:
            return 0

        return max(values)

    @staticmethod
    def minimum(values):
        if not values:
            return 0

        return min(values)
