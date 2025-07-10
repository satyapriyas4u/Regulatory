GSPR_GENERATOR_PROMPT = """
You are a regulatory affairs expert specializing in medical device documentation.
Using the following five user-provided inputs, generate a complete, well-structured, and regulation-compliant document
according to EU MDR, US FDA, and Indian MDR standards (if applicable).
 
The document must follow global safety and performance regulatory expectations and use
realistic, applicable ISO, ASTM, and IEC standards.

Use the following device information to generate content for General Safety and Performance Requirements (GSPR):

=== Device Metadata ===
• Device Type: {device_type}
• Intended Purpose: {intended_purpose}
• Intended Use: {intended_use}
• Region Classifications:{region_classifications}


=== Task ===
Generate GSPR documentation for:
• Component: {component}
• GSPR Number: {gspr}
• Applicability: Applicable

=== Response Format ===
Provide the output strictly in this JSON format (without markdown or additional commentary):

{{
  "design_input": "...",
  "justification": "...",
  "requirement": "...",
  "standard": "..."
}}
"""
