from typing import Dict, Any
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import math

class SimulationService:
    
    @staticmethod
    def calculate_goal_projection(
        target_amount: float,
        monthly_contribution: float,
        target_date: date,
        current_savings: float = 0,
        expected_return: float = 0.07,
        inflation_rate: float = 0.03
    ) -> Dict[str, Any]:
        
        today = datetime.now().date()
        months_remaining = (target_date.year - today.year) * 12 + (target_date.month - today.month)
        
        if months_remaining <= 0:
            return {
                "is_achievable": False,
                "shortage": target_amount - current_savings,
                "message": "Target date has passed",
                "months_remaining": 0
            }
        
        monthly_rate = expected_return / 12
        future_value_current = current_savings * math.pow(1 + monthly_rate, months_remaining)
        
        if monthly_rate > 0:
            future_value_contributions = monthly_contribution * ((math.pow(1 + monthly_rate, months_remaining) - 1) / monthly_rate)
        else:
            future_value_contributions = monthly_contribution * months_remaining
        
        total_future_value = future_value_current + future_value_contributions
        inflation_adjusted_target = target_amount * math.pow(1 + inflation_rate, months_remaining / 12)
        is_achievable = total_future_value >= target_amount
        
        required_monthly = monthly_contribution
        if not is_achievable and months_remaining > 0:
            remaining_needed = target_amount - future_value_current
            if remaining_needed > 0 and monthly_rate > 0:
                required_monthly = remaining_needed / ((math.pow(1 + monthly_rate, months_remaining) - 1) / monthly_rate)
            elif remaining_needed > 0:
                required_monthly = remaining_needed / months_remaining
        
        return {
            "is_achievable": is_achievable,
            "projected_value": round(total_future_value, 2),
            "target_amount": target_amount,
            "inflation_adjusted_target": round(inflation_adjusted_target, 2),
            "surplus_or_shortage": round(total_future_value - target_amount, 2),
            "months_remaining": months_remaining,
            "current_monthly": monthly_contribution,
            "required_monthly": round(required_monthly, 2),
            "total_contributions": round(monthly_contribution * months_remaining, 2),
            "investment_gains": round(total_future_value - current_savings - (monthly_contribution * months_remaining), 2),
            "assumptions": {
                "expected_annual_return": f"{expected_return * 100}%",
                "inflation_rate": f"{inflation_rate * 100}%"
            }
        }
    
    @staticmethod
    def run_what_if_scenario(base_assumptions: Dict[str, Any], variations: Dict[str, Any]) -> Dict[str, Any]:
        scenario_assumptions = {**base_assumptions, **variations}
        result = SimulationService.calculate_goal_projection(
            target_amount=scenario_assumptions.get('target_amount', 0),
            monthly_contribution=scenario_assumptions.get('monthly_contribution', 0),
            target_date=scenario_assumptions.get('target_date', date.today()),
            current_savings=scenario_assumptions.get('current_savings', 0),
            expected_return=scenario_assumptions.get('expected_return', 0.07),
            inflation_rate=scenario_assumptions.get('inflation_rate', 0.03)
        )
        return {"scenario_assumptions": scenario_assumptions, "results": result}
    
    @staticmethod
    def generate_allocation_recommendation(risk_profile: str, age: int = 35) -> Dict[str, Any]:
        allocations = {
            "conservative": {"stocks": 30, "bonds": 50, "cash": 20, "description": "Focus on capital preservation"},
            "moderate": {"stocks": 60, "bonds": 30, "cash": 10, "description": "Balanced approach"},
            "aggressive": {"stocks": 80, "bonds": 15, "cash": 5, "description": "Growth-focused"}
        }
        allocation = allocations.get(risk_profile.lower(), allocations["moderate"])
        
        if age:
            suggested_bonds = min(age, 70)
            suggested_stocks = 100 - suggested_bonds - 10
            allocation["age_adjusted"] = {
                "stocks": max(suggested_stocks, 20),
                "bonds": min(suggested_bonds, 60),
                "cash": 10,
                "note": f"Adjusted for age {age}"
            }
        
        return allocation

simulation_service = SimulationService()