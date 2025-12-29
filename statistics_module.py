"""
statistics_module.py
File: Basic Statistics Functions for Music Data
Author: [Your Name]
Student ID: [Your ID]
Course: [Course Name]
"""

import math

class Statistics:
    """Class for basic statistical calculations on music data"""
    
    @staticmethod
    def calculate_average(numbers):
        """Calculate the average (mean) of a list of numbers"""
        if not numbers or len(numbers) == 0:
            return 0.0
        
        total = 0
        for num in numbers:
            total += num
        
        return total / len(numbers)
    
    @staticmethod
    def calculate_median(numbers):
        """Find the middle value of a sorted list"""
        if not numbers or len(numbers) == 0:
            return 0.0
        
        sorted_numbers = sorted(numbers.copy())  # Copy to avoid modifying original
        n = len(sorted_numbers)
        
        # Check if odd or even number of elements
        if n % 2 == 1:
            # Odd: return middle element
            middle_index = n // 2
            return sorted_numbers[middle_index]
        else:
            # Even: return average of two middle elements
            middle_index1 = (n // 2) - 1
            middle_index2 = n // 2
            return (sorted_numbers[middle_index1] + sorted_numbers[middle_index2]) / 2
    
    @staticmethod
    def calculate_mode(numbers):
        """Find the most frequent value in a list"""
        if not numbers or len(numbers) == 0:
            return 0.0
        
        # Count occurrences of each number
        frequency_dict = {}
        for num in numbers:
            if num in frequency_dict:
                frequency_dict[num] += 1
            else:
                frequency_dict[num] = 1
        
        # Find maximum frequency
        max_frequency = 0
        for count in frequency_dict.values():
            if count > max_frequency:
                max_frequency = count
        
        # Find numbers with maximum frequency
        most_frequent_numbers = []
        for num, count in frequency_dict.items():
            if count == max_frequency:
                most_frequent_numbers.append(num)
        
        # Return first mode if multiple exist
        if most_frequent_numbers:
            return most_frequent_numbers[0]
        else:
            return 0.0
    
    @staticmethod
    def calculate_standard_deviation(numbers):
        """Calculate how spread out numbers are from the average"""
        if not numbers or len(numbers) < 2:
            return 0.0
        
        # Calculate average
        average = Statistics.calculate_average(numbers)
        
        # Calculate sum of squared differences
        sum_squared_differences = 0
        for num in numbers:
            difference = num - average
            sum_squared_differences += difference * difference
        
        # Calculate variance and standard deviation
        variance = sum_squared_differences / len(numbers)
        std_dev = math.sqrt(variance)
        
        return std_dev
    
    @staticmethod
    def calculate_range(numbers):
        """Calculate the difference between max and min values"""
        if not numbers or len(numbers) == 0:
            return 0.0
        
        min_val = numbers[0]
        max_val = numbers[0]
        
        for num in numbers:
            if num < min_val:
                min_val = num
            if num > max_val:
                max_val = num
        
        return max_val - min_val
    
    @staticmethod
    def calculate_variance(numbers):
        """Calculate variance (average of squared differences from mean)"""
        if not numbers or len(numbers) < 2:
            return 0.0
        
        average = Statistics.calculate_average(numbers)
        
        sum_squared_differences = 0
        for num in numbers:
            difference = num - average
            sum_squared_differences += difference * difference
        
        return sum_squared_differences / len(numbers)

# Simple test function
def test_statistics():
    """Test the statistics functions with sample data"""
    print("Testing Statistics class...")
    
    test_data = [85, 90, 78, 92, 88, 85, 95]
    
    print(f"Test data: {test_data}")
    print(f"Average: {Statistics.calculate_average(test_data):.2f}")
    print(f"Median: {Statistics.calculate_median(test_data):.2f}")
    print(f"Mode: {Statistics.calculate_mode(test_data)}")
    print(f"Standard Deviation: {Statistics.calculate_standard_deviation(test_data):.2f}")
    print(f"Range: {Statistics.calculate_range(test_data)}")
    print(f"Variance: {Statistics.calculate_variance(test_data):.2f}")
    
    print("\nStatistics test completed!")

# Run test if file is executed directly
if __name__ == "__main__":
    test_statistics()