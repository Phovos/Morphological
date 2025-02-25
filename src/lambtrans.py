#!/usr/bin/env python3
"""
Lambda Function Transformer

This module provides functionality to parse, analyze, modify and transform
lambda functions using Python's abstract syntax tree (AST) module.
"""

import ast
from enum import Enum, auto
from typing import Optional, Union, Dict


class TransformOperation(Enum):
    """Enumeration of supported transformation operations."""
    MULTIPLY = auto()
    DIVIDE = auto()
    ADD = auto()
    SUBTRACT = auto()
    POWER = auto()
    MODULO = auto()


class LambdaTransformer:
    """
    A class for parsing and transforming lambda functions using AST manipulation.
    
    This class provides methods to parse lambda function source code, display its
    AST representation, and apply various transformations to the lambda body.
    """
    
    def __init__(self, source_code: str = None):
        """
        Initialize the LambdaTransformer with optional source code.
        
        Args:
            source_code: String representation of a lambda function
        """
        self.source_code = source_code
        self.tree = None
        if source_code:
            self.parse()
    
    def parse(self, source_code: Optional[str] = None) -> ast.AST:
        """
        Parse the source code into an AST.
        
        Args:
            source_code: Optional new source code to parse
            
        Returns:
            The AST representation of the source code
            
        Raises:
            SyntaxError: If source code is not valid Python
            ValueError: If source code is not provided and not set earlier
        """
        if source_code:
            self.source_code = source_code
        
        if not self.source_code:
            raise ValueError("No source code provided to parse")
        
        self.tree = ast.parse(self.source_code, mode='eval')
        return self.tree
    
    def dump_ast(self) -> str:
        """
        Return a string representation of the AST.
        
        Returns:
            String representation of the AST with annotated fields
            
        Raises:
            ValueError: If no AST is available (parse must be called first)
        """
        if not self.tree:
            raise ValueError("No AST available. Call parse() first.")
        
        return ast.dump(self.tree, annotate_fields=True)
    
    def transform(self, operation: Union[TransformOperation, str], value: Union[int, float] = 2) -> str:
        """
        Transform the lambda function according to the specified operation.
        
        Args:
            operation: The operation to apply (TransformOperation enum or string name)
            value: The numeric value to use in the transformation
            
        Returns:
            The modified lambda function as a string
            
        Raises:
            ValueError: If no AST is available or operation is not supported
        """
        if not self.tree:
            raise ValueError("No AST available. Call parse() first.")
        
        # Convert string operation to enum if needed
        if isinstance(operation, str):
            try:
                operation = TransformOperation[operation.upper()]
            except KeyError:
                raise ValueError(f"Unsupported operation: {operation}")
        
        # Create and apply the transformer
        transformer = self._create_transformer(operation, value)
        modified_tree = transformer.visit(ast.copy_location(ast.fix_missing_locations(self.tree), self.tree))
        
        # Generate the modified source code
        return ast.unparse(modified_tree)
    
    def _create_transformer(self, operation: TransformOperation, value: Union[int, float]) -> ast.NodeTransformer:
        """
        Create a NodeTransformer for the specific operation.
        
        Args:
            operation: The transformation operation
            value: The numeric value for the operation
            
        Returns:
            An instance of a NodeTransformer subclass
        """
        return _LambdaOperationTransformer(operation, value)


class _LambdaOperationTransformer(ast.NodeTransformer):
    """
    AST NodeTransformer that modifies lambda functions.
    
    This is an internal class used by LambdaTransformer.
    """
    
    # Mapping of operations to AST operator nodes
    _OP_MAP = {
        TransformOperation.MULTIPLY: ast.Mult,
        TransformOperation.DIVIDE: ast.Div,
        TransformOperation.ADD: ast.Add,
        TransformOperation.SUBTRACT: ast.Sub,
        TransformOperation.POWER: ast.Pow,
        TransformOperation.MODULO: ast.Mod
    }
    
    def __init__(self, operation: TransformOperation, value: Union[int, float]):
        """
        Initialize the transformer with an operation and value.
        
        Args:
            operation: The transformation operation to apply
            value: The numeric value to use in the transformation
        """
        self.operation = operation
        self.value = value
    
    def visit_Lambda(self, node: ast.Lambda) -> ast.Lambda:
        """
        Visit and transform a Lambda node in the AST.
        
        Args:
            node: The Lambda node to transform
            
        Returns:
            The transformed Lambda node
        """
        # Make a copy of the original node to avoid modifying the input
        new_node = ast.Lambda(
            args=node.args,
            body=self._transform_body(node.body)
        )
        return ast.copy_location(new_node, node)
    
    def _transform_body(self, body: ast.expr) -> ast.expr:
        """
        Transform the body of a lambda function.
        
        Args:
            body: The original body expression
            
        Returns:
            The transformed body expression
        """
        op_class = self._OP_MAP.get(self.operation)
        if not op_class:
            raise ValueError(f"Operation {self.operation} not implemented")
        
        # Create the new operation
        return ast.BinOp(
            left=body,
            op=op_class(),
            right=ast.Constant(value=self.value)
        )


def main():
    """Demonstrate the LambdaTransformer functionality."""
    # Example lambda function
    source_code = "lambda x: x + 2"
    
    # Create a transformer
    transformer = LambdaTransformer(source_code)
    
    # Print the original AST representation
    print(f"Original Lambda: {source_code}")
    print(f"AST Structure:\n{transformer.dump_ast()}\n")
    
    # Demonstrate transformations with different operations
    operations = [
        (TransformOperation.MULTIPLY, 2),
        (TransformOperation.DIVIDE, 2),
        (TransformOperation.ADD, 5),
        (TransformOperation.SUBTRACT, 1),
        (TransformOperation.POWER, 2),
        (TransformOperation.MODULO, 3)
    ]
    
    print("Transformations:")
    for op, value in operations:
        modified_code = transformer.transform(op, value)
        print(f"  {op.name} by {value}: {modified_code}")
    
    # Demonstrate using string operation names
    print("\nUsing string operation names:")
    for op_name in ["multiply", "divide", "add"]:
        modified_code = transformer.transform(op_name, 3)
        print(f"  {op_name.upper()} by 3: {modified_code}")
    
    # Demonstrate chaining transformations
    print("\nChaining transformations:")
    transformer.parse("lambda x: x * 2")
    modified_code = transformer.transform(TransformOperation.ADD, 1)
    print(f"  First transformation: {modified_code}")
    
    # Parse the modified code and apply another transformation
    transformer.parse(modified_code)
    final_code = transformer.transform(TransformOperation.POWER, 2)
    print(f"  Second transformation: {final_code}")


if __name__ == "__main__":
    main()