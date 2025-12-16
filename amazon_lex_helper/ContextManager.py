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
Context management utilities for Amazon Lex V2.
Provides utilities for managing active contexts and their attributes.
"""

from typing import Dict, List, Optional, Any
from amazon_lex_helper.LexEvent import LexEvent


class ContextManager:
    """Utility class for managing Lex V2 contexts."""
    
    @staticmethod
    def create_context(name: str, attributes: Dict[str, str] = None, 
                      time_to_live_seconds: int = 600, turns_to_live: int = 1) -> Dict:
        """
        Create a context structure.
        
        Args:
            name: Context name
            attributes: Context attributes dictionary
            time_to_live_seconds: Time to live in seconds (default 600)
            turns_to_live: Number of turns to live (default 1)
        """
        return {
            'name': name,
            'contextAttributes': attributes or {},
            'timeToLive': {
                'timeToLiveInSeconds': time_to_live_seconds,
                'turnsToLive': turns_to_live
            }
        }
    
    @staticmethod
    def get_context_by_name(contexts: List[Dict], context_name: str) -> Optional[Dict]:
        """
        Find a context by name in the contexts list.
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context to find
            
        Returns:
            Context dictionary or None if not found
        """
        for context in contexts:
            if context.get('name') == context_name:
                return context
        return None
    
    @staticmethod
    def update_context_attributes(contexts: List[Dict], context_name: str, 
                                 attributes: Dict[str, str]) -> List[Dict]:
        """
        Update attributes for a specific context.
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context to update
            attributes: New attributes to set
            
        Returns:
            Updated contexts list
        """
        for context in contexts:
            if context.get('name') == context_name:
                context['contextAttributes'].update(attributes)
                break
        return contexts
    
    @staticmethod
    def add_context(contexts: List[Dict], name: str, attributes: Dict[str, str] = None,
                   time_to_live_seconds: int = 600, turns_to_live: int = 1) -> List[Dict]:
        """
        Add a new context to the contexts list.
        
        Args:
            contexts: Existing contexts list
            name: Context name
            attributes: Context attributes
            time_to_live_seconds: Time to live in seconds
            turns_to_live: Number of turns to live
            
        Returns:
            Updated contexts list
        """
        new_context = ContextManager.create_context(
            name, attributes, time_to_live_seconds, turns_to_live
        )
        
        # Remove existing context with same name if it exists
        contexts = [ctx for ctx in contexts if ctx.get('name') != name]
        contexts.append(new_context)
        
        return contexts
    
    @staticmethod
    def remove_context(contexts: List[Dict], context_name: str) -> List[Dict]:
        """
        Remove a context from the contexts list.
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context to remove
            
        Returns:
            Updated contexts list
        """
        return [ctx for ctx in contexts if ctx.get('name') != context_name]
    
    @staticmethod
    def extend_context_ttl(contexts: List[Dict], context_name: str, 
                          additional_seconds: int = 300, additional_turns: int = 1) -> List[Dict]:
        """
        Extend the time-to-live for a specific context.
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context to extend
            additional_seconds: Additional seconds to add
            additional_turns: Additional turns to add
            
        Returns:
            Updated contexts list
        """
        for context in contexts:
            if context.get('name') == context_name:
                ttl = context.get('timeToLive', {})
                current_seconds = ttl.get('timeToLiveInSeconds', 0)
                current_turns = ttl.get('turnsToLive', 0)
                
                context['timeToLive'] = {
                    'timeToLiveInSeconds': current_seconds + additional_seconds,
                    'turnsToLive': current_turns + additional_turns
                }
                break
        
        return contexts
    
    @staticmethod
    def get_context_attribute(contexts: List[Dict], context_name: str, 
                             attribute_name: str) -> Optional[str]:
        """
        Get a specific attribute from a context.
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context
            attribute_name: Name of attribute
            
        Returns:
            Attribute value or None if not found
        """
        context = ContextManager.get_context_by_name(contexts, context_name)
        if context:
            return context.get('contextAttributes', {}).get(attribute_name)
        return None
    
    @staticmethod
    def set_context_attribute(contexts: List[Dict], context_name: str, 
                             attribute_name: str, attribute_value: str) -> List[Dict]:
        """
        Set a specific attribute in a context.
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context
            attribute_name: Name of attribute
            attribute_value: Value to set
            
        Returns:
            Updated contexts list
        """
        for context in contexts:
            if context.get('name') == context_name:
                if 'contextAttributes' not in context:
                    context['contextAttributes'] = {}
                context['contextAttributes'][attribute_name] = attribute_value
                break
        
        return contexts
    
    @staticmethod
    def clear_context_attributes(contexts: List[Dict], context_name: str) -> List[Dict]:
        """
        Clear all attributes from a specific context.
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context
            
        Returns:
            Updated contexts list
        """
        for context in contexts:
            if context.get('name') == context_name:
                context['contextAttributes'] = {}
                break
        
        return contexts
    
    @staticmethod
    def is_context_active(contexts: List[Dict], context_name: str) -> bool:
        """
        Check if a context is active (exists in the contexts list).
        
        Args:
            contexts: List of context dictionaries
            context_name: Name of context to check
            
        Returns:
            True if context is active
        """
        return ContextManager.get_context_by_name(contexts, context_name) is not None
    
    @staticmethod
    def get_all_context_names(contexts: List[Dict]) -> List[str]:
        """
        Get names of all active contexts.
        
        Args:
            contexts: List of context dictionaries
            
        Returns:
            List of context names
        """
        return [ctx.get('name') for ctx in contexts if ctx.get('name')]
    
    @staticmethod
    def merge_contexts(contexts1: List[Dict], contexts2: List[Dict]) -> List[Dict]:
        """
        Merge two context lists, with contexts2 taking precedence for duplicates.
        
        Args:
            contexts1: First contexts list
            contexts2: Second contexts list (takes precedence)
            
        Returns:
            Merged contexts list
        """
        merged = contexts1.copy()
        
        for ctx2 in contexts2:
            ctx2_name = ctx2.get('name')
            if ctx2_name:
                # Remove any existing context with the same name
                merged = [ctx for ctx in merged if ctx.get('name') != ctx2_name]
                # Add the new context
                merged.append(ctx2)
        
        return merged


class ConversationState:
    """Utility class for managing conversation state using contexts."""
    
    def __init__(self, context_name: str = 'conversationState'):
        self.context_name = context_name
    
    def get_state(self, contexts: List[Dict]) -> Dict[str, str]:
        """
        Get the current conversation state.
        
        Args:
            contexts: List of context dictionaries
            
        Returns:
            State attributes dictionary
        """
        context = ContextManager.get_context_by_name(contexts, self.context_name)
        if context:
            return context.get('contextAttributes', {})
        return {}
    
    def set_state(self, contexts: List[Dict], state: Dict[str, str], 
                 time_to_live_seconds: int = 3600, turns_to_live: int = 10) -> List[Dict]:
        """
        Set the conversation state.
        
        Args:
            contexts: List of context dictionaries
            state: State attributes to set
            time_to_live_seconds: Time to live in seconds
            turns_to_live: Number of turns to live
            
        Returns:
            Updated contexts list
        """
        return ContextManager.add_context(
            contexts, self.context_name, state, time_to_live_seconds, turns_to_live
        )
    
    def update_state(self, contexts: List[Dict], updates: Dict[str, str]) -> List[Dict]:
        """
        Update specific state attributes.
        
        Args:
            contexts: List of context dictionaries
            updates: State updates to apply
            
        Returns:
            Updated contexts list
        """
        return ContextManager.update_context_attributes(contexts, self.context_name, updates)
    
    def get_state_value(self, contexts: List[Dict], key: str) -> Optional[str]:
        """
        Get a specific state value.
        
        Args:
            contexts: List of context dictionaries
            key: State key
            
        Returns:
            State value or None
        """
        return ContextManager.get_context_attribute(contexts, self.context_name, key)
    
    def set_state_value(self, contexts: List[Dict], key: str, value: str) -> List[Dict]:
        """
        Set a specific state value.
        
        Args:
            contexts: List of context dictionaries
            key: State key
            value: State value
            
        Returns:
            Updated contexts list
        """
        return ContextManager.set_context_attribute(contexts, self.context_name, key, value)
    
    def clear_state(self, contexts: List[Dict]) -> List[Dict]:
        """
        Clear all conversation state.
        
        Args:
            contexts: List of context dictionaries
            
        Returns:
            Updated contexts list
        """
        return ContextManager.remove_context(contexts, self.context_name)
    
    def is_state_active(self, contexts: List[Dict]) -> bool:
        """
        Check if conversation state context is active.
        
        Args:
            contexts: List of context dictionaries
            
        Returns:
            True if state is active
        """
        return ContextManager.is_context_active(contexts, self.context_name)
