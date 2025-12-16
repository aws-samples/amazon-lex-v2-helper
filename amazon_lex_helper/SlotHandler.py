"""
 Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 SPDX-License-Identifier: MIT-0

 Permission is hereby granted, free of charge, to any person obtaining a copy of this
 software and associated documentation files (the "Software"), to deal in the Software
 without restriction, including without limitation the rights to use, copy, modify,
 merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

"""
Enhanced slot handling utilities for Amazon Lex V2.
Provides support for multi-valued slots, slot validation, and elicitation styles.
"""

from typing import Dict, List, Optional, Any, Union
from amazon_lex_helper.LexEvent import LexEvent


class SlotHandler:
    """Utility class for enhanced slot handling in Lex V2."""
    
    @staticmethod
    def create_scalar_slot(original_value: str, interpreted_value: str = None, 
                          resolved_values: List[str] = None) -> Dict:
        """
        Create a scalar slot value structure.
        
        Args:
            original_value: The original value as provided by user
            interpreted_value: The interpreted value (defaults to original_value)
            resolved_values: List of resolved values (defaults to [interpreted_value])
        """
        if interpreted_value is None:
            interpreted_value = original_value
        if resolved_values is None:
            resolved_values = [interpreted_value]
            
        return {
            'shape': 'Scalar',
            'value': {
                'originalValue': original_value,
                'interpretedValue': interpreted_value,
                'resolvedValues': resolved_values
            }
        }
    
    @staticmethod
    def create_list_slot(values: List[Dict]) -> Dict:
        """
        Create a list slot value structure for multi-valued slots.
        
        Args:
            values: List of value dictionaries with originalValue, interpretedValue, resolvedValues
        """
        slot_values = []
        for value in values:
            slot_values.append({
                'value': {
                    'originalValue': value.get('originalValue'),
                    'interpretedValue': value.get('interpretedValue'),
                    'resolvedValues': value.get('resolvedValues', [value.get('interpretedValue')])
                }
            })
        
        return {
            'shape': 'List',
            'values': slot_values
        }
    
    @staticmethod
    def add_value_to_list_slot(existing_slot: Dict, new_value: Dict) -> Dict:
        """
        Add a new value to an existing list slot.
        
        Args:
            existing_slot: Existing list slot structure
            new_value: New value to add with originalValue, interpretedValue, resolvedValues
        """
        if existing_slot.get('shape') != 'List':
            raise ValueError("Slot must be of shape 'List'")
        
        new_slot_value = {
            'value': {
                'originalValue': new_value.get('originalValue'),
                'interpretedValue': new_value.get('interpretedValue'),
                'resolvedValues': new_value.get('resolvedValues', [new_value.get('interpretedValue')])
            }
        }
        
        existing_slot['values'].append(new_slot_value)
        return existing_slot
    
    @staticmethod
    def validate_slot_value(slot_value: str, valid_values: List[str], 
                           case_sensitive: bool = False) -> bool:
        """
        Validate a slot value against a list of valid values.
        
        Args:
            slot_value: The slot value to validate
            valid_values: List of valid values
            case_sensitive: Whether validation should be case sensitive
        """
        if not case_sensitive:
            slot_value = slot_value.lower()
            valid_values = [v.lower() for v in valid_values]
        
        return slot_value in valid_values
    
    @staticmethod
    def validate_slot_pattern(slot_value: str, pattern: str) -> bool:
        """
        Validate a slot value against a regex pattern.
        
        Args:
            slot_value: The slot value to validate
            pattern: Regex pattern to match against
        """
        import re
        return bool(re.match(pattern, slot_value))
    
    @staticmethod
    def get_slot_validation_error_count(req: LexEvent, slot_name: str) -> int:
        """
        Get the number of validation errors for a specific slot.
        
        Args:
            req: LexEvent object
            slot_name: Name of the slot
        """
        attrs = req.get_session_attrs()
        error_key = f'validation_errors_{slot_name.lower()}'
        return int(attrs.get(error_key, 0))
    
    @staticmethod
    def increment_slot_validation_error(req: LexEvent, slot_name: str) -> int:
        """
        Increment the validation error count for a specific slot.
        
        Args:
            req: LexEvent object
            slot_name: Name of the slot
            
        Returns:
            New error count
        """
        attrs = req.get_session_attrs()
        error_key = f'validation_errors_{slot_name.lower()}'
        current_count = int(attrs.get(error_key, 0))
        new_count = current_count + 1
        attrs[error_key] = str(new_count)
        return new_count
    
    @staticmethod
    def reset_slot_validation_errors(req: LexEvent, slot_name: str):
        """
        Reset validation error count for a specific slot.
        
        Args:
            req: LexEvent object
            slot_name: Name of the slot
        """
        attrs = req.get_session_attrs()
        error_key = f'validation_errors_{slot_name.lower()}'
        if error_key in attrs:
            del attrs[error_key]
    
    @staticmethod
    def create_elicitation_style_config(style: str = "Default", 
                                       spell_by_letter: bool = False,
                                       spell_by_word: bool = False) -> Dict:
        """
        Create slot elicitation style configuration.
        
        Args:
            style: Elicitation style ("Default", "SpellByLetter", "SpellByWord")
            spell_by_letter: Enable spell by letter mode
            spell_by_word: Enable spell by word mode
        """
        if spell_by_letter:
            style = "SpellByLetter"
        elif spell_by_word:
            style = "SpellByWord"
        
        return {
            "slotElicitationStyle": style
        }
    
    @staticmethod
    def extract_slot_values_from_list(list_slot: Dict) -> List[str]:
        """
        Extract interpreted values from a list slot.
        
        Args:
            list_slot: List slot structure
            
        Returns:
            List of interpreted values
        """
        if list_slot.get('shape') != 'List':
            return []
        
        values = []
        for slot_value in list_slot.get('values', []):
            if 'value' in slot_value:
                interpreted_value = slot_value['value'].get('interpretedValue')
                if interpreted_value:
                    values.append(interpreted_value)
        
        return values
    
    @staticmethod
    def merge_slot_values(slot1: Dict, slot2: Dict) -> Dict:
        """
        Merge two slot values. If both are lists, combine them.
        If one is scalar and other is list, convert scalar to list and combine.
        
        Args:
            slot1: First slot
            slot2: Second slot
            
        Returns:
            Merged slot
        """
        if not slot1:
            return slot2
        if not slot2:
            return slot1
        
        # If both are lists, combine them
        if (slot1.get('shape') == 'List' and slot2.get('shape') == 'List'):
            combined_values = slot1.get('values', []) + slot2.get('values', [])
            return {
                'shape': 'List',
                'values': combined_values
            }
        
        # If one is list and other is scalar, convert scalar to list and combine
        elif slot1.get('shape') == 'List' and slot2.get('shape') == 'Scalar':
            new_value = {'value': slot2['value']}
            slot1['values'].append(new_value)
            return slot1
        
        elif slot1.get('shape') == 'Scalar' and slot2.get('shape') == 'List':
            new_value = {'value': slot1['value']}
            slot2['values'].insert(0, new_value)
            return slot2
        
        # If both are scalar, return the second one (override)
        else:
            return slot2


class SlotValidator:
    """Utility class for slot validation with common validation patterns."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Validate phone number format (US format)."""
        import re
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        # Check if it's 10 or 11 digits (with or without country code)
        return len(digits_only) in [10, 11]
    
    @staticmethod
    def validate_date_format(date_str: str, format_pattern: str = r'^\d{4}-\d{2}-\d{2}$') -> bool:
        """Validate date format (default: YYYY-MM-DD)."""
        import re
        return bool(re.match(format_pattern, date_str))
    
    @staticmethod
    def validate_numeric_range(value: str, min_val: float = None, max_val: float = None) -> bool:
        """Validate numeric value within a range."""
        try:
            num_value = float(value)
            if min_val is not None and num_value < min_val:
                return False
            if max_val is not None and num_value > max_val:
                return False
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_string_length(value: str, min_length: int = None, max_length: int = None) -> bool:
        """Validate string length."""
        length = len(value)
        if min_length is not None and length < min_length:
            return False
        if max_length is not None and length > max_length:
            return False
        return True
    
    @staticmethod
    def validate_choice(value: str, choices: List[str], case_sensitive: bool = False) -> bool:
        """Validate value is one of the allowed choices."""
        if not case_sensitive:
            value = value.lower()
            choices = [choice.lower() for choice in choices]
        return value in choices
