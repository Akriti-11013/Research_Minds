#!/usr/bin/env python
"""Test script to verify the ResearchMind workflow works end-to-end."""

from app.graph.workflow import workflow

# Test the workflow with a sample research query
result = workflow.invoke({
    'topic': 'Impact of Generative AI on software development',
    'depth': 'quick'
})

print('✅ Workflow executed successfully!')
print(f'Topic: {result["topic"]}')
print(f'Research Plan: {len(result["research_plan"])} items')
print(f'Sources Found: {len(result["sources"])}')
print(f'Analysis: {len(result["source_analysis"])} analyses')
print(f'Fact Checks: {len(result["fact_checks"])} checks')
print(f'Report Generated: {bool(result["report"])}')
print(f'Markdown Generated: {len(result["markdown"])} chars')
print()
print('📄 Sample Markdown Output (first 500 chars):')
print(result['markdown'][:500])
print()
print('=' * 80)
print('Full Markdown Output:')
print('=' * 80)
print(result['markdown'])
