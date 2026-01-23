#!/usr/bin/env python3
"""
Convert Graph-Toucan message format to Toucan message format
"""
import json
import argparse
from pathlib import Path


def convert_graph_toucan_to_toucan_messages(graph_toucan_messages):
    """
    Convert Graph-Toucan message format to Toucan format

    Graph-Toucan format:
    - Assistant messages may have 'tool_calls' field
    - Tool responses have role 'tool' with 'tool_call_id'

    Toucan format:
    - Tool calls are separate messages with role 'tool_call'
    - Tool responses have role 'tool_response' (no tool_call_id)

    Args:
        graph_toucan_messages: List of messages in Graph-Toucan format

    Returns:
        List of messages in Toucan format
    """
    toucan_messages = []

    for msg in graph_toucan_messages:
        role = msg.get('role')

        if role == 'system':
            # Skip system messages (they are not included in Toucan format)
            continue

        elif role == 'assistant':
            # Check if this assistant message has tool calls
            tool_calls = msg.get('tool_calls', [])
            content = msg.get('content', '')

            # Add assistant message only if content is not empty
            if content:
                assistant_msg = {
                    'role': 'assistant',
                    'content': content
                }
                toucan_messages.append(assistant_msg)

            # Add separate tool_call messages for each tool call
            if tool_calls:
                for tool_call in tool_calls:
                    tool_call_msg = {
                        'role': 'tool_call',
                        'content': json.dumps({
                            'name': tool_call['function']['name'],
                            'arguments': tool_call['function']['arguments']
                        })
                    }
                    toucan_messages.append(tool_call_msg)

        elif role == 'tool':
            # Convert tool message to tool_response
            tool_response_msg = {
                'role': 'tool_response',
                'content': msg.get('content', '')
            }
            toucan_messages.append(tool_response_msg)

        elif role == 'user':
            # User messages stay the same
            toucan_messages.append({
                'role': 'user',
                'content': msg.get('content', '')
            })
        else:
            # Unknown role, keep as is
            toucan_messages.append(msg)

    return toucan_messages


def process_jsonl_entry(entry):
    """
    Process a single JSONL entry and convert its conversation_history

    Args:
        entry: Dictionary containing the JSONL entry

    Returns:
        Dictionary with converted conversation_history
    """
    if 'conversation_history' in entry:
        entry['conversation_history'] = convert_graph_toucan_to_toucan_messages(
            entry['conversation_history']
        )
    return entry


def convert_jsonl_file(input_path, output_path):
    """
    Convert a JSONL file from Graph-Toucan to Toucan format

    Args:
        input_path: Path to input JSONL file
        output_path: Path to output JSONL file
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}")

    line_count = 0
    converted_count = 0

    with input_file.open('r', encoding='utf-8') as infile, \
         output_file.open('w', encoding='utf-8') as outfile:

        for line_num, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                continue

            try:
                # Parse the JSON entry
                entry = json.loads(line)
                line_count += 1

                # Convert the conversation_history
                converted_entry = process_jsonl_entry(entry)
                converted_count += 1

                # Write to output file
                outfile.write(json.dumps(converted_entry, ensure_ascii=False) + '\n')

                if line_count % 100 == 0:
                    print(f"Processed {line_count} lines...")

            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON at line {line_num}: {e}")
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
                raise

    print(f"\nConversion complete!")
    print(f"Total lines processed: {line_count}")
    print(f"Successfully converted: {converted_count}")


def test_conversion():
    """Test the conversion with sample data"""
    # Sample Graph-Toucan format
    graph_toucan = [
        {
            "role": "system",
            "content": "You are an AI assistant."
        },
        {
            "role": "user",
            "content": "Check train tickets from Beijing to Shanghai"
        },
        {
            "role": "assistant",
            "content": "I'll search for train tickets.",
            "tool_calls": [
                {
                    "id": "call_123",
                    "type": "function",
                    "function": {
                        "name": "search_train",
                        "arguments": '{"from": "Beijing", "to": "Shanghai"}'
                    }
                }
            ]
        },
        {
            "role": "tool",
            "tool_call_id": "call_123",
            "content": '{"trains": ["G1", "G2"]}'
        },
        {
            "role": "assistant",
            "content": "I found 2 trains: G1 and G2."
        }
    ]

    toucan = convert_graph_toucan_to_toucan_messages(graph_toucan)

    print("=== Converted to Toucan format ===")
    for i, msg in enumerate(toucan):
        print(f"\nMessage {i}:")
        print(f"  Role: {msg['role']}")
        print(f"  Content: {msg['content'][:100]}...")

    return toucan


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert Graph-Toucan message format to Toucan format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert a JSONL file
  python message_format_convert.py -i distill_v3.jsonl -o distill_v3_toucan.jsonl

  # Run test conversion
  python message_format_convert.py --test
        """
    )
    parser.add_argument('-i', '--input', help='Input JSONL file path')
    parser.add_argument('-o', '--output', help='Output JSONL file path')
    parser.add_argument('--test', action='store_true', help='Run test conversion')

    args = parser.parse_args()

    if args.test:
        print("Running test conversion...")
        test_conversion()
    elif args.input and args.output:
        try:
            convert_jsonl_file(args.input, args.output)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
    else:
        parser.print_help()

