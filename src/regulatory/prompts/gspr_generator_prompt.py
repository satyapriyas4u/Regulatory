GSPR_GENERATOR_PROMPT = """
You are a regulatory affairs expert specializing in medical device documentation.
Using the provided device and component details, generate a complete, well-structured,
regulation-compliant GSPR record according to EU MDR, US FDA, and Indian MDR standards (if applicable).

Ensure realistic and applicable ISO, ASTM, and IEC standards are used.

=== Device Metadata ===
• Device Type: {device_type}
• Intended Purpose: {intended_purpose}
• Intended Use: {intended_use}
• Region Classifications: {region_classifications}

=== Task ===
For the given component and GSPR section, generate detailed content.

• Component: {component}
• GSPR Number: {gspr}
• Applicability: Applicable

=== Strict JSON Response Format ===
Return ONLY a JSON object in this exact format, without any explanation, markdown, or extra text:

{
  "component": "<component>",
  "gspr": <integer>,
  "design_input": "<string>",
  "applicability": "Applicable",
  "justification": "<string>",
  "requirement": "<string>",
  "standard": "<string>"
}
"""
