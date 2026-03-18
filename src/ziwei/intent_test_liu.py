"""
Intent Recognition Test Module
Author: 刘二明 (Employee ID: 107)
Group: XJ-01 紫微元灵
Task: 意图识别测试
"""

from typing import Dict, List, Any, Optional
import unittest


class IntentTest:
    """Intent Recognition Test Implementation"""
    
    def __init__(self):
        """Initialize the test module."""
        self.test_cases: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0
        
    def add_test_case(self, input_text: str, expected_intent: str) -> None:
        """
        Add a test case.
        
        Args:
            input_text: Input text
            expected_intent: Expected intent
        """
        self.test_cases.append({
            "input": input_text,
            "expected": expected_intent
        })
        
    def run_tests(self, algorithm) -> Dict[str, Any]:
        """
        Run all test cases.
        
        Args:
            algorithm: IntentAlgorithm instance
            
        Returns:
            Test results dictionary
        """
        results = []
        
        for test_case in self.test_cases:
            result = algorithm.recognize(test_case["input"])
            
            if result["intent"] == test_case["expected"]:
                self.passed += 1
                results.append({
                    "input": test_case["input"],
                    "expected": test_case["expected"],
                    "actual": result["intent"],
                    "status": "PASSED"
                })
            else:
                self.failed += 1
                results.append({
                    "input": test_case["input"],
                    "expected": test_case["expected"],
                    "actual": result["intent"],
                    "status": "FAILED"
                })
                
        return {
            "total": len(self.test_cases),
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": self.passed / len(self.test_cases) if self.test_cases else 0,
            "results": results
        }
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "test_cases": len(self.test_cases),
            "passed": self.passed,
            "failed": self.failed
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "IntentTest",
            "version": "1.0.0",
            "status": "ready"
        }
